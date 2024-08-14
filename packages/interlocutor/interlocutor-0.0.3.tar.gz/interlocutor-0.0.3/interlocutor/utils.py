import os
from pathlib import Path
from typing import Optional

import pathspec


def load_ignore_patterns(
    ignore_file_paths: list[str],
    additional_ignore_patterns: Optional[list[str]] = None
) -> pathspec.PathSpec:
    """
    Load patterns from ignore files and append additional patterns.

    Parameters:
    - ignore_file_paths: A list of paths to ignore files
    - additional_ignore_patterns: A list of additional patterns to ignore

    Returns:
    - A PathSpec object compiled with the ignore patterns
    """
    ignore_list = []

    for ignore_file_path in ignore_file_paths:
        try:
            if os.path.exists(ignore_file_path):
                with open(ignore_file_path, 'r') as file:
                    ignore_list.extend(file.read().splitlines())
            else:
                print(f"Warning: {ignore_file_path} not found.")
        except FileNotFoundError:
            print(f"Warning: {ignore_file_path} not found.")

    # Add additional ignore patterns, if provided
    if additional_ignore_patterns:
        ignore_list.extend(additional_ignore_patterns)

    return pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, ignore_list)


def generate_project_structure(
    root: str,
    ignore_spec: pathspec.PathSpec,
    indent: str = "|   ",
) -> str:
    """
    Generate a visual representation of the directory structure.

    Parameters:
    - root: The root directory
    - ignore_spec: A PathSpec object containing patterns to ignore
    - indent: The string used for indentation (default: "|   ")

    Returns:
    - A string representing the directory structure
    """

    def walk(path: Path, level: int = 0) -> str:
        output = ""
        try:
            entries = sorted(path.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower()))
            subdir_output = ""
            has_visible_entries = False

            for entry in entries:
                relative_path = entry.relative_to(root)

                if ignore_spec.match_file(str(relative_path)):
                    continue

                if entry.is_dir():
                    sub_output = walk(entry, level + 1)

                    if sub_output.strip() or not list(entry.iterdir()):
                        subdir_output += f"{indent * level}|-- {entry.name}/\n"
                        subdir_output += sub_output
                        has_visible_entries = True
                else:
                    subdir_output += f"{indent * level}|-- {entry.name}\n"
                    has_visible_entries = True

            if has_visible_entries or subdir_output.strip():
                output += subdir_output

        except PermissionError:
            output += f"{indent * level}|-- [Permission Denied]\n"
        return output

    return walk(Path(root))


def process_repository(repo_path: str, ignore_spec: pathspec.PathSpec, output_file):
    """
    Process the repository and write file contents to the output file.

    Parameters:
    - repo_path: The path to the Git repository
    - ignore_spec: A PathSpec object containing patterns to ignore
    - output_file: The output file object to write the contents
    """
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, repo_path)

            if ignore_spec.match_file(relative_path):
                continue

            with open(file_path, 'r', errors='ignore') as f:
                content = f.read()
                output_file.write(f"----\n{relative_path}\n{content}\n")
