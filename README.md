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

# Install dependencies
pip install -r requirements.txt
```

## Usage

Run the script using Python:

```bash
python main.py
```

Follow the on-screen prompts to select the folder and the criteria for organizing files.

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
- Command-line arguments

## License

This project is licensed under the MIT License.
