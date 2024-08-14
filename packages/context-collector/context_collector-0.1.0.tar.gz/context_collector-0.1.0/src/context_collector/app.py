import argparse
import fnmatch
import os.path

from pathlib import Path

DEFAULT_IGNORES = [
    # Version control and IDE related
    '.git/',
    '.gitignore',
    '.idea/',
    '__pycache__',
    '*.pyc',
    '*.pyo',
    '*.pyd',
    '.DS_Store',

    # java jar
    '*.jar',

    # Image formats
    '*.jpg',
    '*.jpeg',
    '*.png',
    '*.gif',
    '*.bmp',
    '*.svg',
    '*.ico',

    # Documents and presentations
    '*.pdf',
    '*.doc',
    '*.docx',
    '*.ppt',
    '*.pptx',
    '*.xls',
    '*.xlsx',

    # Compressed files
    '*.zip',
    '*.rar',
    '*.7z',
    '*.tar',
    '*.gz',

    # Audio and video files
    '*.mp3',
    '*.wav',
    '*.mp4',
    '*.avi',
    '*.mov',

    # Other binary files
    '*.exe',
    '*.dll',
    '*.so',
    '*.dylib'
]
def get_ignore_patterns(path: str):
    gitignore_path = os.path.join(path, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []


def should_ignore(file_path: str, rel_path: str, ignore_patterns: list[str]):
    path = Path(file_path)
    parts = path.parts

    for pattern in ignore_patterns:
        if pattern.endswith("/"):
            if any(part == pattern[:-1] for part in parts):
                return True
    return any(fnmatch.fnmatch(rel_path, pattern) for pattern in ignore_patterns)


def collect_context(path: str, output_file: str, user_ignores: list[str]):
    ignore_patterns = get_ignore_patterns(path)
    # exclude the files
    ignore_patterns.append(output_file)
    ignore_patterns.extend(DEFAULT_IGNORES)
    ignore_patterns.extend(user_ignores)
    with open(output_file, "w") as output_file:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, path)
                if should_ignore(file_path, relative_path, ignore_patterns):
                    continue
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        output_file.write(f"{relative_path}\n```\n{content}\n```\n\n")

                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")


def get_project_name(path: str):
    return os.path.basename(os.path.abspath(path))


def main():
    parser = argparse.ArgumentParser(description="Collect context from a code repository")
    parser.add_argument("-p", "--path", default=".", help="Path to the repository")
    parser.add_argument("-o", "--output", help="Output file name, default: project_name.txt")
    parser.add_argument("-e", "--exclude", nargs="*", default=[], help="exclude files")
    args = parser.parse_args()

    if not args.output:
        args.output = get_project_name(args.path) + ".txt"

    collect_context(args.path, args.output, args.exclude)


if __name__ == '__main__':
    main()
