"""
The purpose of the BigImage class is to provide a method to manage and display a very Big Image
without having to worry too much about the memory restrictions. The image is constructed
by placing blocks of pixels at their positions (i.e. the top corner of the block). 
The class BigImage will return a preview decimated (i.e. reduced) by 'factor' (an integer) to make it manageable
and possible to display reasonably well.  It makes it possible to work with an image that would be several GB without 
sacrificing speed: for instance, and image of 1 GB made of 17x17x2048x2048 images can be displayed in less than a second.

"""

import unittest
import tempfile
import time

from enum import Enum

from pathlib import Path
from multiprocessing import Pool

import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import tifffile

from bliqtools.testing import Progress, MemoryMonitor, TimeIt
from bliqtools.nirvana import FilePath


class Method(Enum):
    """
    When reducing the size of a block, 3 methods can be used.
    NUMPY: a slice every "factor" points is used.  This is very fast and the default.
    SCIPY: will use the decimate() function
    PIL: uses a thumbnail method from the PIL library (needs to load image)
    """

    NUMPY = "numpy-slice"
    SCIPY = "scipy-decimate"
    PIL = "pil-thumbnail"


class BlockEntry:
    """Class for keeping track of an image block, either on disk or in memory.
    An image block is a section of the image (i.e. a numpy array) with its top corner.
    The entry will have its data either in the data property, or on disk, not both.
    """

    reduction = Method.NUMPY

    def __init__(self, coords, data, image_filepath=None):
        """
        Initialize the entry with the corner coords and the data or the image filepath.
        If we have the data immediately, then we compute previews with a group of useful
        factors since it is not expensive to do so.
        """
        self.coords = coords
        self._data = data
        self.image_filepath = image_filepath
        self._saved_filepath = None
        self.last_access = None
        self.previews = {}

        self._shape = None
        if data is not None:
            self._shape = data.shape

        if self._data is not None:
            for factor in [16, 32, 64, 128]:
                preview = self.get_preview(factor=factor)
                self.previews[factor] = preview

    @property
    def is_purged(self):
        """
        True if the data is not in memory
        """
        return self._data is None

    @property
    def data(self):
        """
        Return the numpy data of the entry. If it is not already loaded,
        obtain it from the _saved_filepath if it has been set, or from
        the image_filepath that was passed on init.
        """
        if self.is_purged:
            if self._saved_filepath is not None:
                self._data = np.load(self._saved_filepath)
            else:
                self._data = np.asarray(Image.open(self.image_filepath))

            self._saved_filepath = None

        return self._data

    @property
    def shape(self):
        """
        Return the shape of the block.  Tries to avoid loading the image data if possible:
        if we had access to the data block before, we saved the shape into _shape.
        If not, we load the data and get the shape from there.
        """
        if self._shape is None:
            self._shape = self.data.shape

        return self._shape

    def index_slices(self, factor=1):
        """
        Return the slices (x_min:x_max, y_min:y_max) needed to insert this block into the BigImage
        with the given factor
        """
        return (slice(self.coords[0] // factor, (self.coords[0] + self.shape[0]) // factor),
                slice(self.coords[1] // factor, (self.coords[1] + self.shape[1]) // factor))

    def get_preview(self, factor: int):
        """
        Return a version of the block that is 'factor' smaller
        """
        if factor in self.previews.keys():
            return self.previews[factor]

        original_data = self.data
        x, y = self.data.shape

        preview = None
        match BlockEntry.reduction:
            case Method.SCIPY:
                from scipy.signal import decimate
                data_axis0_reduced = decimate(original_data, q=factor, axis=0)
                preview = decimate(data_axis0_reduced, q=factor, axis=1)
            case Method.NUMPY:
                preview = original_data[0:x:factor, 0:y:factor]
            case Method.PIL:
                if self.image_filepath is not None:
                    with Image.open(self.image_filepath) as im:
                        preview = im.thumbnail((x // factor, y // factor))

        return preview

    def purge(self, directory):
        """
        Delete from memory the arrays after having saved them in the provided directory.

        """
        if not self.is_purged:
            i, j = self.coords
            _saved_filepath = Path(directory, f"Tile@{i}-{j}.npy")
            np.save(_saved_filepath, self._data)

            self._saved_filepath = _saved_filepath
            self._data = None
            self.last_access = time.time()


class BigImage:
    """
    A class for extremely large images that manages memory efficiently to preview a lower resolution version quickly
    """

    def __init__(self, size=None):
        """
        Create BigImage with an expected size. If the size is None, it will be computed
        from the entries when needed in get_preview.  If the provided size is too small
        to accomodate all the images, an error will occur.
        """
        self.size = size
        self.data = None
        self.other_resolutions = []
        self.entries = []
        self._work_dir = tempfile.TemporaryDirectory()

    def __del__(self):
        """
        To avoid warnings, we explicitly cleanup the temporary directory
        """
        self._work_dir.cleanup()

    def add_block(self, coords, data=None, image_filepath=None):
        """
        The data from the numpy array 'data' goes to pixel "coords" in the large image

        BlockEntries are kept in a simple list that is used to reconstruct the low resolution version
        """
        if data is None and image_filepath is None:
            raise ValueError("You must provide either the numpy data or an image file")

        self.entries.append(
            BlockEntry(coords=coords, data=data, image_filepath=image_filepath)
        )

    def add_entry(self, entry):
        """
        Adds an entry to the entries.  It could be an already-loaded image or a filepath, we do not
        concern ourselves with the details.
        """
        self.entries.append(entry)

    def purge(self):
        """
        Purges arrays from memory and save everything to disk
        """
        for entry in self.entries:
            entry.purge(directory=self._work_dir.name)

    def calculate_full_size(self):
        """
        Calculate the full size of the image considering the tiles present
        """

        max_x = max([entry.coords[0] for entry in self.entries])
        max_y = max([entry.coords[1] for entry in self.entries])
        some_entry = self.entries[0]
        block_width, block_height = some_entry.data.shape
        return max_x + block_width, max_y + block_height

    def get_reduced_resolution_preview(self, factor=16, progress=None):
        """
        Put together all blocks in a reduced version of the final image.
        Nothing fancy for overlap: just overwrite the data. If a size
        was provided, it must be large enough to contain the blocks
        """
        full_width, full_height = self.calculate_full_size()
        if self.size is not None:
            full_width = max(full_width, self.size[0])
            full_height = max(full_height, self.size[1])

        small_width = full_width // factor
        small_height = full_height // factor
        preview = np.zeros(shape=(small_width, small_height), dtype=np.uint8)

        with Progress(
            total=len(self.entries), show_every=10, delay_before_showing=1
        ) as p:
            for entry in self.entries:
                slice0, slice1 = entry.index_slices(factor=factor)
                small_block = entry.get_preview(factor=factor)
                preview[slice0, slice1] = small_block
                entry.purge(directory=self._work_dir.name)
                p.next()

        return preview

    def get_reduced_resolution_block(self, coords, factor=None):
        """
        Get a reduced preview for a block at given coordinates if available
        """
        for entry in self.entries:
            if entry.coords == coords:
                return entry.get_preview(factor)
        return None


class TestBigImage(unittest.TestCase):
    """
    Several tests for BigImage and understanding its details
    """

    def test_01_init(self):
        """
        We can create a BigImage object
        """
        img = BigImage()
        self.assertIsNotNone(img)

    def test_02_add_block(self):
        """
        We can add a block to a BigImage object
        """
        img = BigImage()
        small_block = np.ones(shape=(10, 10), dtype=np.uint8)
        img.add_block(coords=(0, 0), data=small_block)
        self.assertEqual(len(img.entries), 1)

    def test_03_tempdir(self):
        """
        Understanding how tempfile.TemporaryDirectory() works.
        We need to keep the reference to the object, will
        not use it for now.
        """
        tdir = tempfile.TemporaryDirectory()
        tdir.cleanup()

    def test_04_add_many_blocks(self):
        """
        We can add a block to a BigImage object
        """

        img = BigImage()
        with MemoryMonitor():
            with Progress(total=100, description="Block", show_every=10) as p:
                for i in range(10):
                    for j in range(10):
                        small_block = np.random.randint(
                            0, 255, size=(10_00, 10_00), dtype=np.uint8
                        )
                        img.add_block(coords=(i, j), data=small_block)
                        p.next()

        self.assertEqual(len(img.entries), 100)

    def test_05_purge_actually_clears_memory(self):
        """
        We can add a block to a BigImage object
        """

        img = BigImage()
        small_block = np.random.randint(0, 255, size=(10_00, 10_00), dtype=np.uint8)
        img.add_block(coords=(0, 0), data=small_block)

        self.assertFalse(img.entries[0].is_purged)

        img.purge()

        self.assertTrue(img.entries[0].is_purged)

    @unittest.skip("Long")
    def test_06_add_many_blocks_with_purge(self):
        """
        We can add a block to a BigImage object
        """

        img = BigImage()
        with MemoryMonitor():
            with Progress(total=100, description="Tile", show_every=10) as p:
                for i in range(10):
                    for j in range(10):
                        small_block = np.random.randint(
                            0, 255, size=(10_000, 10_000), dtype=np.uint8
                        )
                        img.add_block(coords=(i * 10_000, j * 10_000), data=small_block)
                        p.next()
                    img.purge()

        self.assertEqual(len(img.entries), 100)

    def test_07_add_block_get_reduced_version(self):
        """
        Can we get a reduced version of a block?

        """

        img = BigImage()
        small_block = np.random.randint(0, 255, size=(10_000, 10_000), dtype=np.uint8)
        img.add_block(coords=(0, 0), data=small_block)
        reduced_block = img.get_reduced_resolution_block((0, 0), factor=10)
        self.assertEqual(reduced_block.shape, (1000, 1000))

    @unittest.skip("Lengthy")
    def test_08_get_reduced_preview(self):
        """
        Extract a reduced dimension preview from the BigImage
        """

        img = BigImage()
        with MemoryMonitor():
            with Progress(total=100, description="Tile", show_every=10) as p:
                for i in range(10):
                    for j in range(10):
                        small_block = np.random.randint(
                            0, 255, size=(1_000, 1_000), dtype=np.uint8
                        )
                        img.add_block(coords=(i * 1_000, j * 1_000), data=small_block)
                        p.next()

        preview = img.get_reduced_resolution_preview(factor=20)
        self.assertEqual(preview.shape, (500, 500))
        plt.imshow(preview, interpolation="nearest")
        plt.show()

    @unittest.skip("No graph")
    def test_09_get_reduced_preview_missing_blocks(self):
        """
        Extract a reduced dimension preview from the BigImage
        """

        img = BigImage()
        with MemoryMonitor():
            with Progress(total=100, description="Tile", show_every=10) as p:
                for i in range(0, 10, 2):
                    for j in range(10):
                        small_block = np.random.randint(
                            0, 255, size=(1_000, 1_000), dtype=np.uint8
                        )
                        img.add_block(coords=(i * 1_000, j * 1_000), data=small_block)
                        p.next()

        preview = img.get_reduced_resolution_preview(factor=20)
        self.assertEqual(preview.shape, (500, 500))
        plt.imshow(preview, interpolation="nearest")
        plt.show()

    def cheap_tile_loader_knock_off(self, filepaths):
        """
        This function mimicks the behaviour of TileLoader because I do not want to import it
        for testing here.

        Returns the number of tiles in i,j,k
        """
        i = set()
        j = set()
        k = set()
        for filepath in filepaths:
            i.add(filepath.i)
            j.add(filepath.j)
            k.add(filepath.k)

        some_filepath = filepaths[0]
        some_entry = BlockEntry(coords=(0, 0), data=None, image_filepath=some_filepath)
        w, h = some_entry.data.shape

        return len(i), len(j), len(k), w, h

    def test_10_from_real_dataset_attempt(self):
        """
        This assumes a dataset at path, with Nirvana-style tiles.
        We work with the first layer only.
        """

        root_dir = FilePath(Path.home(), "Downloads/Test_maps/C1")
        filepaths = root_dir.contents()
        layer1_filepaths = [filepath for filepath in filepaths if filepath.k == 1]
        _, _, _, w, h = self.cheap_tile_loader_knock_off(layer1_filepaths)

        img = BigImage()
        BlockEntry.reduction = Method.NUMPY

        for filepath in layer1_filepaths:
            pixel_x = (filepath.i - 1) * w
            pixel_y = (filepath.j - 1) * h

            entry = BlockEntry(
                coords=(pixel_x, pixel_y), data=None, image_filepath=filepath
            )
            img.add_entry(entry)

        # with cProfile.Profile() as pr:
        with MemoryMonitor():
            preview = img.get_reduced_resolution_preview(factor=32)
            # pr.print_stats(sort="time")

        plt.imshow(preview, interpolation="nearest")
        plt.show()

    def test_11_pil_thumbnail(self):
        """
        PIL offers a function to create a thumbnail of an image.
        Unfortunately, this is not faster than either numpy slicing or scipy
        """
        root_dir = FilePath(Path.home(), "Downloads/Test_maps/C1")
        filepaths = root_dir.contents()

        layer1_filepaths = [filepath for filepath in filepaths if filepath.k == 1]
        some_filepath = layer1_filepaths[0]
        with TimeIt():
            with Image.open(some_filepath) as im:
                _ = im.thumbnail((64, 64))

    def test_12_tifffile_writes_images_as_tiles(self):
        """
        Tifffile can write "tiled" images. This attempts to use the feature
        to try to see if it means what I think it means, but when the file
        is opened, I see multiple pages, nto a single image.
        Not sure what to do with this.
        """
        data = np.random.rand(2, 5, 3, 301, 219).astype("float32")
        tifffile.imwrite(
            "/tmp/temp.tif",
            data,
            bigtiff=True,
            photometric="rgb",
            planarconfig="separate",
            tile=(32, 32),
            compression="zlib",
            compressionargs={"level": 8},
            predictor=True,
            metadata={"axes": "TZCYX"},
        )

    def test_13_get_fast_preview(self):
        """
        When loading entries directly with data, the BlockEntry class
        will keep a preview reduced by a factor 16.  Making the preview will be really fast

        """

        img = BigImage()
        with MemoryMonitor():
            with Progress(total=100, description="Tile", show_every=10) as p:
                for i in range(10):
                    for j in range(10):
                        small_block = np.random.randint(
                            0, 255, size=(2048, 2048), dtype=np.uint8
                        )
                        img.add_block(coords=(i * 2048, j * 2048), data=small_block)
                        p.next()

        preview = img.get_reduced_resolution_preview(factor=32)
        plt.imshow(preview)
        plt.show()

    @unittest.skip('No gain at all from calculating in parallel.')
    def test_14_compute_previews_in_parallel(self):
        """
        This assumes a dataset at path, with Nirvana-style tiles.
        We work with the first layer only.
        """

        root_dir = FilePath(Path.home(), "Downloads/Test_maps/C1")
        filepaths = root_dir.contents()
        layer1_filepaths = [filepath for filepath in filepaths if filepath.k == 1]
        _, _, _, w, h = self.cheap_tile_loader_knock_off(layer1_filepaths)

        img = BigImage()
        BlockEntry.reduction = Method.NUMPY

        for filepath in layer1_filepaths:
            pixel_x = (filepath.i - 1) * w
            pixel_y = (filepath.j - 1) * h

            entry = BlockEntry(
                coords=(pixel_x, pixel_y), data=None, image_filepath=filepath
            )
            img.add_entry(entry)

        with TimeIt():
            for entry in img.entries:
                compute_previews(entry)

        with TimeIt():
            with Pool(5) as p:
                p.map(compute_previews, img.entries)


def compute_previews(entry):
    """
    Function used in the multiprocessing example
    """
    for factor in [16, 32, 64, 128]:
        preview = entry.get_preview(factor=factor)
        entry.previews[factor] = preview


if __name__ == "__main__":
    unittest.main()
