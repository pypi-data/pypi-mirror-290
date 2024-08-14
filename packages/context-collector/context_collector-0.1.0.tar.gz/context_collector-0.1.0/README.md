# Context Collector

Context Collector is a Python tool designed to gather context information from code repositories. It traverses specified directories, reads file contents, and consolidates them into a single output file, facilitating potential use with Large Language Models (LLMs) for chat applications.

## Features
- Traverses specified directories and subdirectories
- Reads file contents and consolidates them into a single output file
- Supports .gitignore rules
- Includes a built-in default ignore list (e.g., binary files, images)
- Allows user-defined ignore items
- Flexible command-line parameter configuration


## Installation

- Ensure you have Python 3.10 or higher installed on your system.
- Clone this repository:
- cd <project_name> && poetry install

## Usage

```shell
contc -p /path/to/your/project -o output.txt
```

Parameter description:
- `-p` or `--path`: Specify the repository path to collect context from (default is the current directory)
- `-o` or `--output`: Specify the output file name (default is the project name with a .txt extension)
- `-e` or `--exclude`: Specify additional files or directories to exclude