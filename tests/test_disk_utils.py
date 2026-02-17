import unittest
import os
import shutil
from src.disk_utils import get_dir_size

class TestDiskUtils(unittest.TestCase):
    def setUp(self):
        # Create a temporary test directory
        self.test_dir = "test_folder"
        os.makedirs(self.test_dir, exist_ok=True)
        # Create a dummy file (100 bytes)
        with open(os.path.join(self.test_dir, "test.txt"), "wb") as f:
            f.write(b"0" * 100)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_dir_size(self):
        # Verify the size matches our 100 byte file
        size = get_dir_size(self.test_dir)
        self.assertEqual(size, 100)

    def test_exclude_logic(self):
        # Create a .git folder (which should be excluded)
        git_dir = os.path.join(self.test_dir, ".git")
        os.makedirs(git_dir, exist_ok=True)
        with open(os.path.join(git_dir, "large_file.txt"), "wb") as f:
            f.write(b"0" * 1000)
        
        # Size should still be 100 because .git is ignored
        size = get_dir_size(self.test_dir)
        self.assertEqual(size, 100)