# ClutterCutter

A Python utility to organize files in a directory based on various criteria like size, date, name, and extension.

## Features

- Organize files by size (customizable size brackets)
- Organize files by date created or modified (year, month, day, weekday, quarter)
- Organize files by name (first character, prefix, suffix, keyword, regex, length)
- Organize files by extension (separately or by type)
- User-friendly console interface with clear prompts

## Installation

```bash
# Clone the repository
git clone https://github.com/lazar-kostic/clutter-cutter.git
cd clutter-cutter
```

## Usage

Run the script using Python:

```bash
python main.py
```

Follow the on-screen prompts to select the folder and the criteria for organizing files.

## Arguments

ClutterCutter supports the following command-line arguments:

- `--d` or `--directory`: Specifies the path to the directory to be organized. If the path includes empty characters, it should be wrapped in quotes, e.g. "C:\Downloads\Test Folder".
- `--m` or `--mode`: Specifies the organizing mode. Options are:
  - `size`: Organize files by size.
  - `date_created`: Organize files by creation date.
  - `date_modified`: Organize files by modification date.
  - `name`: Organize files by name.
  - `extension`: Organize files by file extension.
- `--a` or `--arguments`: Provides additional arguments for the selected organizing mode. These depend on the mode being used.

### Organize files in the specified directory by size
```
python main.py --d /path/to/directory --m size --a 3 100MB 500MB 1GB
```
Where '3' is the number of folders to organize the files into, followed by the maximum size for files in each folder.

### Organize files in the specified directory by creation date
```
python main.py --d /path/to/directory --m date_created
```
Since there are no arguments in the command, the script will prompt you for them when needed.

### Organize files in the specified directory by modification date
```
python main.py --d /path/to/directory --m date_modified
```

### Organize files in the specified directory by name using additional arguments
```
python main.py --d /path/to/directory --m name --a 2 _
```
Where '2' is the second sorting option for organizing by name (sorting by prefix), and '_' is the prefix.

## Logging

The script uses the `logging` module to log messages. Logs will be displayed in the console with timestamps and log levels.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Planned Features
- Configuration file support
- Undo functionality
- Preview mode
- Progress bars
- Recursive option
- Better console UI
- Command-line arguments ✅

## License

This project is licensed under the MIT License.
