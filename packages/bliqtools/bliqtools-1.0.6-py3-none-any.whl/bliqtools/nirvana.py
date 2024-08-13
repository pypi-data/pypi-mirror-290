"""
This module is a helper to access files as saved by Nirvana VMS and Lightsheet
from Bliq Photonics.

You can do:
    
    import bliqtools.nirvana

"""

import unittest
import os
import re
from enum import StrEnum
from pathlib import Path
from contextlib import suppress


class FileType(StrEnum):
    """
    The types of files produced by Nirvana
    """

    IMAGE_VMS = "ImageVMS"
    IMAGE_LIGHTSHEET = "ImageLightsheet"
    IMAGE_SPARQ = "ImageSparq"
    IMAGE_SLAM = "ImageSlam"


class UnableToExtractMetadata(ValueError):
    """
    Exception when metadata is not extractable from the filename
    """


class File:
    """
    A class representing a file saved by Nirvana, with its name containing metadata
    """

    patterns = {
        FileType.IMAGE_VMS: {
            "regex": r"-([^-.]+?)-Ch-(\d)-Frame_(\d+)-Time_(\d.+?)s\.",
            "groups": ["provider", "channel", "frame", "time"],
            "types": [str, int, int, float],
        }
    }

    def __init__(self, filepath):
        """
        Initializing file from complete filepath
        """
        self.filepath = filepath
        if not os.path.exists(self.filepath):
            raise ValueError(f"{self.filepath} does not exist")

        if not os.path.isfile(self.filepath):
            raise ValueError(f"{self.filepath} is not a file")

        self.metadata = self.extract_meta_data()
        self.metadata["filepath"] = self.filepath

    @property
    def provider(self):
        """
        Image provider that created this image
        """
        return self.metadata["provider"]

    @property
    def channel(self):
        """
        Image provider channel
        """
        return self.metadata["channel"]

    @property
    def frame(self):
        """
        Frame number in sequence
        """
        return self.metadata["frame"]

    @property
    def time(self):
        """
        Time since beginning of save action
        """
        return self.metadata["time"]

    @property
    def filetype(self):
        """
        The type of Nirvana file
        """
        return self.metadata["filetype"]

    @classmethod
    def is_valid_name(cls, filepath):
        """
        Returns if a name is a valid Nirvana file name before creating an object File
        """
        for _, matching_info in cls.patterns.items():
            match = re.search(matching_info["regex"], str(filepath))
            if match is not None:
                return True
        return False

    def extract_meta_data(self):
        """
        Extract metadata from filename
        """
        metadata = {}

        for filetype, matching_info in self.patterns.items():
            match = re.search(matching_info["regex"], str(self.filepath))
            if match is not None:
                for i, name in enumerate(matching_info["groups"]):
                    cast_type = matching_info["types"][i]
                    metadata[name] = cast_type(match.group(i + 1))
                metadata["filetype"] = filetype
            else:
                raise UnableToExtractMetadata(
                    f"Unable to extract metadata from filename {self.filepath}"
                )

        return metadata


class Folder:
    """
    A class representing a folder where images were saved by Nirvana. The folder can be a Channel folder
    or the root folder containing the Channels folder.

    """

    def __init__(self, path):
        self.path = path

        if not os.path.exists(self.path):
            raise ValueError(f"{self.path} does not exist")

        if not os.path.isdir(self.path):
            raise ValueError(f"{self.path} is not a directory")

        self.files = self.get_nirvana_files()

    def get_nirvana_files(self):
        """
        Retrieve all files in the present directory that are Nirvana image files and return them
        """
        files = os.listdir(self.path)

        nirvana_files = []
        for filename in files:
            filepath = Path(self.path, filename)
            with suppress(ValueError):
                file = File(filepath=filepath)
                nirvana_files.append(file)

        return nirvana_files

    def get_metadata(self):
        """
        Make a list of the metadata of each file and return it
        """
        return [file.metadata for file in self.files]


class TestClasses(unittest.TestCase):
    """
    Unittesting demonstrating use of classes.

    """

    test_dir = "./test_data"
    filepath = Path(
        test_dir,
        "Test-001",
        "FLIR camera-Ch-1",
        "Test-001-FLIR camera-Ch-1-Frame_002377-Time_0.023s.tif",
    )
    large_folder = ""
    nirvana_dir = Path(test_dir, "Test-001")
    channel_dir = Path(test_dir, "Test-001", "FLIR camera-Ch-1")

    def short_test_id(self):
        """
        Simple function to identify running test
        """
        return self.id().split(".")[
            -1
        ]  # Remove complete class name before the function name

    def test_check_valid_file(self):
        """
        The filepath must exist and be a file for File to be created
        """
        with self.assertRaises(Exception):
            self.assertIsNotNone(File("/tmp"))

        with self.assertRaises(Exception):
            self.assertIsNotNone(File("/tmp/idontexist"))

        self.assertIsNotNone(File(self.filepath))

    def test_check_metadata(self):
        """
        Extract metadata from filename
        """
        nirvana_file = File(self.filepath)
        self.assertIsNotNone(nirvana_file)
        metadata = nirvana_file.extract_meta_data()
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata["provider"], "FLIR camera")
        self.assertEqual(metadata["channel"], 1)
        self.assertEqual(metadata["frame"], 2377)
        self.assertEqual(metadata["time"], 0.023)
        self.assertEqual(metadata["filetype"], FileType.IMAGE_VMS)

    def test_get_metadata_as_properties(self):
        """
        Meta data properties are accessible as Python properties
        """
        nirvana_file = File(self.filepath)
        self.assertIsNotNone(nirvana_file)
        self.assertEqual(nirvana_file.provider, "FLIR camera")
        self.assertEqual(nirvana_file.channel, 1)
        self.assertEqual(nirvana_file.frame, 2377)
        self.assertEqual(nirvana_file.time, 0.023)
        self.assertEqual(nirvana_file.filetype, FileType.IMAGE_VMS)

    def test_init_valid_nirvana_folder(self):
        """
        The folder must exist and be a directory
        """
        with self.assertRaises(Exception):
            f = Folder("/idontexist")

        f = Folder("/tmp")
        self.assertIsNotNone(f)

    def test_get_files(self):
        """
        The folder must contain Nirvana files with understandable metadata
        """
        with self.assertRaises(Exception):
            f = Folder("/idontexist")

        f = Folder(self.channel_dir)
        self.assertIsNotNone(f)
        files = f.get_nirvana_files()
        self.assertIsNotNone(files)
        self.assertTrue(len(files) == 3)

    def test_get_all_metadata_from_folder(self):
        """
        We can obtain a list of metadata for each file, and it must include filepath
        """
        f = Folder(self.channel_dir)
        metadata = f.get_metadata()
        self.assertEqual(len(metadata), 3)
        self.assertIsNotNone(metadata[0]["filepath"])

    def test_is_a_nirvana_file(self):
        """
        Check if name is valid before creating object
        """
        self.assertTrue(File.is_valid_name(self.filepath))
        self.assertFalse(File.is_valid_name("/tmp/123.tif"))

    @unittest.skip("No access")
    def test_large_folder(self):
        """
        Retrieve large number of files from directory (only tested locally)
        """
        f = Folder(self.large_folder)
        self.assertIsNotNone(f)
        files = f.get_nirvana_files()
        self.assertTrue(len(files) > 60_000)


if __name__ == "__main__":
    unittest.main()
