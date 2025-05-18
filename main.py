# Libraries
import logging, argparse, json

# Modules
from utils import choose_mode, select_folder
from FileSystemNode import build_filesystem_tree, build_shallow_filesystem_tree, print_tree
from organizers import DateOrganizer, SizeOrganizer, NameOrganizer, ExtensionOrganizer

# Variables
settings = {
    'directory': None,
    'options': {
        'recursive': None
    },
    'mode': None,
    'arguments': None
}
modes = ['File size', 'Date created', 'Date modified', 'File name', 'Extension']
modes_short = ['size', 'date_created', 'date_modified', 'name', 'extension']
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Argparse setup
parser = argparse.ArgumentParser(prog='ClutterCutter',
                                 description='A Python utility to organize files in a directory based on various criteria like size, date, name, and extension.',
                                 usage='%(prog)s [options]')
parser.add_argument('--c', '--config', type=str, default='config.json', help='Path to configuration file (default: config.json)')
parser.add_argument('--d', '--directory', type=str, help='Path to directory which will be organized')
parser.add_argument('--p', '--preview', action='store_true', help='Preview the changes before running')
parser.add_argument('--r', '--recursive', action='store_true', help='Also process files in subdirectories of chosen directory')
parser.add_argument('--m', '--mode', type=str, choices=['size', 'date_created', 'date_modified', 'name', 'extension'], help='Change mode for organizing')
parser.add_argument('--a', '--arguments', nargs='+', help='Arguments, only if organizing mode is specified using --m or --mode')
args = parser.parse_args()

def load_from_cla():
    try:
        if args.d:
            settings['directory'] = args.d
        if args.r:
            settings['options']['recursive'] = args.r
        if args.m:
            settings['mode'] = args.m
        if args.a:
            settings['arguments'] = args.a
    except AttributeError:
        logging.error('The provided arguments are invalid.')

def load_from_config_file():
    try:
        with open(args.c, 'r', encoding='utf-8') as config_file:
            for key, value in json.load(config_file).items():
                #Avoid overwriting settings parsed from CLA
                if not settings[key]:
                    settings[key] = value
    except FileNotFoundError:
        logging.warning('Configuration file not found.')
    except PermissionError:
        logging.warning('Permission to open configuration file was denied.')

def manual_input():
    if not settings['directory']:
        logging.info('To begin, please select the folder which contains the files you wish to organize.')
        folder_name = select_folder()
        if not folder_name:
            logging.error('User canceled action.')
            exit(1)
        settings['directory'] = folder_name
    else:
        logging.info('Running using the directory provided in the ' +  ('console argument(s).' if args.d else 'config file.'))

# Main function
if __name__ == '__main__':
    logging.info('ClutterCutter v.1.1.0')

    # Load information from the CLA first, if provided
    load_from_cla()

    # Load provided data from the config file into the settings dictionary
    load_from_config_file()

    # If directory is not provided through CLA or config file, prompt the user for it
    manual_input()

    # Scan either all the files in the root directory, or recursively scan all subdirectories too if using recursive mode
    if settings['options']['recursive']:
        root_node, has_files = build_filesystem_tree(settings['directory'])
    else:
        root_node, has_files = build_shallow_filesystem_tree(settings['directory'])

    # If there are no children (files) in the provided root directory
    if not has_files:
        logging.error('The provided directory contains no files.')
        exit(1)

    logging.info('The following files were found in the provided directory:')
    print_tree(root_node)

    # If the mode is not provided through CLA or config file, prompt the user for it
    if not settings['mode']:
        logging.info('Please select your desired mode for organizing files. Instructions and explanations for each mode will be shown after selection. You may choose between:\n')
        settings['mode'] = choose_mode(modes)

    # Organizing
    organizer_classes = {
        1: SizeOrganizer,
        2: lambda root, args: DateOrganizer(root, 2, args),
        3: lambda root, args: DateOrganizer(root, 3, args),
        4: NameOrganizer,
        5: ExtensionOrganizer
    }

    organizer = None
    if settings['mode'] in organizer_classes:
        if settings['mode'] in [2, 3]:
            organizer = organizer_classes[settings['mode']](root_node, args.a)
            organizer.run_all()
        else:
            organizer = organizer_classes[settings['mode']](root_node, args.a)
            organizer.run_all()

    choice = input('Would you like to save this configuration to a configuration file? (y/n): ')
    if choice == 'y':
        with open('config.json', 'w', encoding='utf-8') as config_file:
            json.dump(settings, config_file, ensure_ascii=False, indent=4)

