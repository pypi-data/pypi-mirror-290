# interlocutor: Describing Repositories  
  
interlocutor is a tool for generating descriptions of repositories that are machine-readable.  It can output the folder and file structure, process repository contents, and write this information to an output file.

## Features  

- **Generate Directory Structure**: Output the folder and file structure of a repository in a clear and organized format that is machine and human-readable.
- **Process Repository Files**: Extract and save the contents of files in a repository to a structured output file.
- **Customizable Output**: Specify a preamble, output file, and additional ignore files to customize the output.
- **Structure-Only Option**: Generate only the directory structure without processing file contents.
  
## Installation  
  
You can install postnormalism using pip:  
  
```sh  
pip install interlocutor  
```  

## Usage  

### Generating Structure Only

To generate only the directory structure of a repository without including file contents:

```sh
interlocutor /path/to/git/repository --structure-only -o structure_output.txt
```

### Including a Preamble

You can include a preamble at the beginning of the output file:

```sh
interlocutor /path/to/git/repository -p /path/to/preamble.txt -o output.txt
```

### Using Additional Ignore Files

If you want to use additional ignore files along with `.gptignore`, specify them using the --ignore option:

```sh
interlocutor /path/to/git/repository --ignore /path/to/additional_ignore_file.txt -o output.txt
```

### Or Do Your Own Thing

Or just import and use the underlying utility functions.

## Contributing  
  
Please submit a start a discussion, create a pull request or create an issue if you have any suggestions or improvements.  

### Primary Authors

- @jzmiller1 (Zac Miller)

### Other Contributors

- N/A


## License  
  
interlocutor is released under the MIT License. See the `LICENSE` file for more information.
