import unittest
import subprocess
import tempfile
import shutil
from pathlib import Path


class TestInterlocutorCLI(unittest.TestCase):
    script_module = "interlocutor.interlocutor"

    def setUp(self):
        # Create a temporary directory for the repository
        self.test_dir = tempfile.mkdtemp()
        self.repo_path = Path(self.test_dir) / "test_repo"
        self.repo_path.mkdir()

        # Create some files and directories in the test repo
        (self.repo_path / "file1.txt").write_text("This is file 1")
        (self.repo_path / "file2.log").write_text("This is file 2")
        (self.repo_path / "dir1").mkdir()
        (self.repo_path / "dir1" / "file3.txt").write_text("This is file 3")
        (self.repo_path / "dir1" / ".hidden").write_text("This is a hidden file")
        (self.repo_path / ".gptignore").write_text(".hidden\n*.log\n.gptignore\n")

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def test_interlocutor_basic(self):
        output_file = self.repo_path / "output.txt"

        result = subprocess.run(
            ["python", "-m", self.script_module, str(self.repo_path), "-o", str(output_file)],
            capture_output=True,
            text=True,
        )
        self.assertTrue(output_file.exists())

        with open(output_file, "r") as f:
            output_content = f.read()

        self.assertIn("Directory Structure:", output_content)
        self.assertIn("file1.txt", output_content)
        self.assertIn("dir1/file3.txt", output_content)
        self.assertNotIn(".hidden", output_content)
        self.assertNotIn("file2.log", output_content)

    def test_interlocutor_with_preamble(self):
        output_file = self.repo_path / "output.txt"

        # Create a preamble file
        preamble_file = self.repo_path / "preamble.txt"
        preamble_file.write_text("This is a preamble.")

        result = subprocess.run(
            ["python", "-m", self.script_module, str(self.repo_path), "-p", str(preamble_file), "-o", str(output_file)],
            capture_output=True,
            text=True,
        )
        self.assertTrue(output_file.exists())

        with open(output_file, "r") as f:
            output_content = f.read()
        self.assertIn("This is a preamble.", output_content)

    def test_interlocutor_missing_arguments(self):
        result = subprocess.run(
            ["python", "-m", self.script_module],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("usage:", result.stderr.lower())

    def test_structure_only(self):
        output_file = self.repo_path / "structure_output.txt"

        result = subprocess.run(
            ["python", "-m", self.script_module, str(self.repo_path), "--structure-only", "-o", str(output_file)],
            capture_output=True,
            text=True,
        )
        self.assertTrue(output_file.exists())

        with open(output_file, "r") as f:
            output_content = f.read()

        self.assertNotIn("----", output_content)
        self.assertIn("|-- file1.txt", output_content)
        self.assertIn("|   |-- file3.txt", output_content)
        self.assertNotIn(".hidden", output_content)
        self.assertNotIn("file2.log", output_content)

    def test_structure_only_with_preamble(self):
        output_file = self.repo_path / "structure_output_with_preamble.txt"

        preamble_file = self.repo_path / "preamble.txt"
        preamble_file.write_text("This is a preamble.")

        result = subprocess.run(
            [
                "python", "-m", self.script_module, str(self.repo_path),
                "--structure-only",
                "--preamble", str(preamble_file),
                "-o", str(output_file)
            ],
            capture_output=True,
            text=True,
        )

        self.assertTrue(output_file.exists())

        with open(output_file, "r") as f:
            output_content = f.read()

        self.assertIn("This is a preamble.", output_content)
        self.assertNotIn("----", output_content)
        self.assertIn("|-- file1.txt", output_content)
        self.assertIn("|   |-- file3.txt", output_content)
        self.assertNotIn(".hidden", output_content)
        self.assertNotIn("file2.log", output_content)
