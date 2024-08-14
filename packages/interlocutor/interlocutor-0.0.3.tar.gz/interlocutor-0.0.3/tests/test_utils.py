import unittest
import tempfile
from pathlib import Path
import shutil

from interlocutor.utils import load_ignore_patterns, generate_project_structure, process_repository


class TestInterlocutorUtils(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.repo_path = Path(self.test_dir) / "test_repo"
        self.repo_path.mkdir()

        (self.repo_path / "file1.txt").write_text("This is file 1")
        (self.repo_path / "file2.log").write_text("This is file 2")
        (self.repo_path / "dir1").mkdir()
        (self.repo_path / "dir1" / "file3.txt").write_text("This is file 3")
        (self.repo_path / "dir1" / ".hidden").write_text("This is a hidden file")
        (self.repo_path / ".gptignore").write_text(".hidden\n*.log\n.gptignore\n")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def remove_gptignore(self):
        gptignore_path = self.repo_path / ".gptignore"
        if gptignore_path.exists():
            gptignore_path.unlink()

    def test_load_ignore_patterns(self):
        ignore_spec = load_ignore_patterns([str(self.repo_path / ".gptignore")])
        self.assertTrue(ignore_spec.match_file(".hidden"))
        self.assertTrue(ignore_spec.match_file("file2.log"))
        self.assertTrue(ignore_spec.match_file(".gptignore"))
        self.assertFalse(ignore_spec.match_file("file1.txt"))

    def test_load_ignore_patterns_with_additional_files(self):
        additional_ignore_file1 = self.repo_path / "additional1.ignore"
        additional_ignore_file1.write_text("*.log\n")
        additional_ignore_file2 = self.repo_path / "additional2.ignore"
        additional_ignore_file2.write_text("file1.txt\n")

        ignore_spec = load_ignore_patterns(
            [str(self.repo_path / ".gptignore"), str(additional_ignore_file1), str(additional_ignore_file2)]
        )
        self.assertTrue(ignore_spec.match_file(".hidden"))
        self.assertTrue(ignore_spec.match_file("file2.log"))
        self.assertTrue(ignore_spec.match_file("file1.txt"))
        self.assertFalse(ignore_spec.match_file("dir1/file3.txt"))

    def test_generate_project_structure(self):
        ignore_spec = load_ignore_patterns([str(self.repo_path / ".gptignore")])
        structure = generate_project_structure(str(self.repo_path), ignore_spec)
        expected_structure = (
            "|-- dir1/\n"
            "|   |-- file3.txt\n"
            "|-- file1.txt\n"
        )
        self.assertEqual(structure.strip(), expected_structure.strip())

        self.remove_gptignore()
        ignore_spec = load_ignore_patterns([])
        structure = generate_project_structure(str(self.repo_path), ignore_spec)
        expected_structure_no_ignore = (
            "|-- dir1/\n"
            "|   |-- .hidden\n"
            "|   |-- file3.txt\n"
            "|-- file1.txt\n"
            "|-- file2.log\n"
        )
        self.assertEqual(structure.strip(), expected_structure_no_ignore.strip())

    def test_process_repository(self):
        ignore_spec = load_ignore_patterns([str(self.repo_path / ".gptignore")])
        output_file_path = self.repo_path / "output.txt"
        with open(output_file_path, 'w') as output_file:
            process_repository(str(self.repo_path), ignore_spec, output_file)

        with open(output_file_path, 'r') as output_file:
            output_content = output_file.read()
        self.assertIn("file1.txt", output_content)
        self.assertIn("dir1/file3.txt", output_content)
        self.assertNotIn(".hidden", output_content)
        self.assertNotIn("file2.log", output_content)
        self.assertNotIn(".gptignore", output_content)

        self.remove_gptignore()
        ignore_spec = load_ignore_patterns([])
        output_file_path = self.repo_path / "output_no_ignore.txt"
        with open(output_file_path, 'w') as output_file:
            process_repository(str(self.repo_path), ignore_spec, output_file)

        with open(output_file_path, 'r') as output_file:
            output_content = output_file.read()
        self.assertIn("file1.txt", output_content)
        self.assertIn("dir1/file3.txt", output_content)
        self.assertIn(".hidden", output_content)
        self.assertIn("file2.log", output_content)

    def test_generate_project_structure_with_ignored_empty_directory(self):
        (self.repo_path / "empty_dir").mkdir()
        (self.repo_path / ".gptignore").write_text(".hidden\n*.log\n.gptignore\nempty_dir\n")

        ignore_spec = load_ignore_patterns([str(self.repo_path / ".gptignore")])
        structure = generate_project_structure(str(self.repo_path), ignore_spec)

        expected_structure = (
            "|-- dir1/\n"
            "|   |-- file3.txt\n"
            "|-- file1.txt\n"
        )
        self.assertEqual(structure.strip(), expected_structure.strip())

    def test_generate_project_structure_with_empty_directory(self):
        (self.repo_path / "empty_dir").mkdir()

        ignore_spec = load_ignore_patterns([])
        structure = generate_project_structure(str(self.repo_path), ignore_spec)

        expected_structure_no_ignore = (
            "|-- dir1/\n"
            "|   |-- .hidden\n"
            "|   |-- file3.txt\n"
            "|-- empty_dir/\n"
            "|-- .gptignore\n"
            "|-- file1.txt\n"
            "|-- file2.log\n"
        )
        self.assertEqual(structure.strip(), expected_structure_no_ignore.strip())
