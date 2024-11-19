import unittest
from datetime import datetime
from shell_emulator import ShellEmulator

class TestShellEmulator(unittest.TestCase):

    def setUp(self):
        self.vfs = [
            "file1.txt",
            "dir1/file2.txt",
            "dir1/dir2/file3.txt",
            "dir1/dir2/"
        ]
        self.shell = ShellEmulator(self.vfs)

    def test_ls_root(self):
        result = self.shell.ls()
        self.assertEqual(result.strip(), "dir1\nfile1.txt")

    def test_ls_subdir(self):
        self.shell.cd("dir1")
        result = self.shell.ls()
        self.assertEqual(result.strip(), "dir2\nfile2.txt")

    def test_cd_to_root(self):
        self.shell.cd("dir1")
        result = self.shell.cd("")
        self.assertEqual(result.strip(), "Returned to root directory")
        self.assertEqual(self.shell.current_dir, "")

    def test_cd_to_parent(self):
        self.shell.cd("dir1/dir2")
        result = self.shell.cd("..")
        self.assertEqual(result.strip(), "Moved to parent directory")
        self.assertEqual(self.shell.current_dir, "dir1/")

    def test_cd_nonexistent(self):
        result = self.shell.cd("nonexistent")
        self.assertEqual(result.strip(), "Directory not found")
        self.assertEqual(self.shell.current_dir, "")

    def test_date(self):
        result = self.shell.date()
        self.assertTrue(result.strip().startswith(str(datetime.now().date())))

    def test_echo(self):
        result = self.shell.echo("Hello, world!")
        self.assertEqual(result.strip(), "Hello, world!")

    def test_chown(self):
        result = self.shell.chown(["file1.txt"])
        self.assertEqual(result.strip(), "Changed ownership of file1.txt")

    def test_unknown_command(self):
        result = self.shell.echo("unknown command")
        self.assertEqual(result.strip(), "unknown command")


if __name__ == "__main__":
    unittest.main()
