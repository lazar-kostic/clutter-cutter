# ClutterCutter 
![cluttercutter_logo_small](https://github.com/user-attachments/assets/e77b8056-db32-4cab-8ec4-f9c138e02cd2)

A Python utility to organize files in a directory based on various criteria like size, date, name, and extension.

## Features

- Multiple organization modes - easily separate files based on any criteria, with custom rules
- Command-line arguments and configuration file support for repeated organizing
- Recursive mode for organizing files in subdirectories with a single run
- Detailed instructions and feedback during the entire organizing process
- Logging of performed operations (using the `logger` module)

### Organization modes:
- Organize files by size (customizable size brackets)
- Organize files by date created or modified (year, month, day, weekday, quarter)
- Organize files by name (first character, prefix, suffix, keyword, regex, length)
- Organize files by extension (separately or by type)
- User-friendly console interface with clear prompts

## Installation

You can install ClutterCutter by cloning the repository:

```bash
git clone https://github.com/yourusername/ClutterCutter.git
cd ClutterCutter
```

ClutterCutter requires Python 3.7 or higher. It uses only standard library modules, so no additional dependencies are needed.

## Usage

Run the script using Python:

```bash
python main.py
```

Follow the on-screen prompts to select the folder and the criteria for organizing files.

## Arguments

ClutterCutter supports the following command-line arguments:

- `--d` or `--directory`: Specifies the path to the directory to be organized. If the path includes empty characters, it should be wrapped in quotes, e.g. "C:\Downloads\Test Folder".
- `--r` or `--recursive`: Enables recursive mode (files in each subdirectory will also be organized)
- `--c` or `--config`: Specifies the path to the configuration file. By default, the value is `config.json`.
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

### Organize files in the specified directory by creation date, using recursive mode
```
python main.py --d /path/to/directory --r --m date_created
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

## Configuration file
In order to save time when organizing files the same way, you can also use a configuration file.
- By default, the script will look for a `config.json` file inside its own folder. The folder's location can also be specified using the command-line arguments.
- You can combine command-line arguments and a configuration file, in which case the CLA are given priority.
- If no configuration file is found, the script will use the provided command-line arguments or run in interactive mode.
- Upon successfully organizing files, the script will also offer to save the settings used to a valid configuration file for you.

### Configuration file format
The configuration file format is identical to the format used when specifying command-line arguments.
```json
{
    "directory": "example\\directory",
    "options": {
        "recursive": true
    },
    "mode": "mode_name",
    "arguments": ["arg1", "arg2", "..."]
}
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Planned Features
- Undo functionality
- Preview mode
- Progress bars
- Better console UI
- Recursive option - Since v1.1.0 ✅
- Configuration file support - Since v1.0.2 ✅ 
- Command-line arguments - Since v1.0.1 ✅ 

## License

This project is licensed under the MIT License.
