import argparse
import os

from interlocutor.utils import load_ignore_patterns, process_repository, generate_project_structure


def write_preamble(output_file, preamble_file):
    if preamble_file:
        with open(preamble_file, 'r') as pf:
            preamble_text = pf.read()
            output_file.write(f"{preamble_text}\n")


def main():
    parser = argparse.ArgumentParser(description="Process and describe a Git repository.")
    parser.add_argument("repo_path", type=str, help="Path to the Git repository")
    parser.add_argument("-p", "--preamble", type=str, help="Path to the preamble file")
    parser.add_argument("-o", "--output", type=str, default="output.txt", help="Path to the output file")
    parser.add_argument("-i", "--ignore", type=str, help="Path to additional ignore files", nargs='+')
    parser.add_argument("-s", "--structure-only", action="store_true", help="Output only the project structure")

    args = parser.parse_args()

    repo_path = args.repo_path
    ignore_file_paths = [os.path.join(repo_path, ".gptignore")]

    # Platform-specific issues
    if os.name == 'nt':  # Windows
        ignore_file_paths = [path.replace("/", "\\") for path in ignore_file_paths]

    if not os.path.exists(ignore_file_paths[0]):
        HERE = os.path.dirname(os.path.abspath(__file__))
        ignore_file_paths[0] = os.path.join(HERE, ".gptignore")

    if args.ignore:
        ignore_file_paths.extend(args.ignore)

    ignore_spec = load_ignore_patterns(ignore_file_paths)
    project_structure = generate_project_structure(repo_path, ignore_spec)

    with open(args.output, 'w') as output_file:
        write_preamble(output_file, args.preamble)

        if args.structure_only:
            output_file.write(project_structure)
            print(f"Project structure written to {args.output}")
        else:
            output_file.write(f"Directory Structure:\n{project_structure}\n")
            process_repository(repo_path, ignore_spec, output_file)
            output_file.write("--END--")
            print(f"Repository contents written to {args.output}.")


if __name__ == "__main__":
    main()
