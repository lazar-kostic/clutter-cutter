# Libraries
import logging, os, argparse, json
from os.path import isfile
from os import listdir

# Modules
from size_module import organize_by_size
from date_module import organize_by_date
from name_module import organize_by_name
from extension_module import organize_by_extension
from helper_functions import choose_option, select_folder

# Variables
options = ['File size', 'Date created', 'Date modified', 'File name', 'Extension']
options_short = ['size', 'date_created', 'date_modified', 'name', 'extension']
user_choices = {}
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

# Main function
if __name__ == '__main__':
    logging.info('ClutterCutter v.1.0.2')

    try:
        with open(args.c, 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        config = {'directory': None}
        logging.warning('Configuration file not found.')

    folder = args.d if args.d else config["directory"]

    if not folder:
        logging.info('To begin, please select the folder which contains the files you wish to organize.')
        folder = select_folder()
        if folder == '':
            exit(1)
        user_choices['directory'] = folder
    else:
        logging.info('Running using the directory provided in the ' +  ('console argument(s).' if args.d else 'config file.'))
        user_choices['directory'] = folder

    try:
        files = [f for f in listdir(folder) if isfile(os.path.join(folder, f))]
        if len(files) == 0:
            logging.error('No files detected in chosen folder.')
            exit(1)
    except FileNotFoundError:
        logging.error('No such file or directory.')
        exit(1)

    logging.info('The following files were detected in your chosen folder:')
    for f in files:
        logging.info(f)

    user_choices['arguments'] = []

    if args.m:
        logging.info('Running using the provided arguments.')
        user_choices['mode'] = args.m
        if args.m == 'size':
            organize_by_size(folder, files, user_choices, args.a)

        if args.m == 'date_created' or args.m == 'date_modified':
            organize_by_date(folder, files, args.m, user_choices, args.a)

        if args.m == 'name':
            organize_by_name(folder, files, user_choices, args.a)

        if args.m == 'extension':
            organize_by_extension(folder, files, user_choices, args.a)

    elif config:
        logging.info('Running using the configuration file.')
        user_choices['mode'] = config['mode']
        if config['mode'] == 'size':
            organize_by_size(folder, files, user_choices, config['arguments'])

        if config['mode'] == 'date_created' or config['mode'] == 'date_modified':
            organize_by_date(folder, files, config['mode'], user_choices, config['arguments'])

        if config['mode'] == 'name':
            organize_by_name(folder, files, user_choices, config['arguments'])

        if config['mode'] == 'extension':
            organize_by_extension(folder, files, user_choices, config['arguments'])

    else:
        logging.info('Please select your desired mode for organizing files. Instructions and explanations for each mode will be shown after selection. You may choose between:\n')
        selected = choose_option(options)
        user_choices['mode'] = options[selected - 1]

        # Organizing
        if selected == 1:
            organize_by_size(folder, files, user_choices)

        if selected == 2 or selected == 3:
            organize_by_date(folder, files, selected, user_choices)

        if selected == 4:
            organize_by_name(folder, files, user_choices)

        if selected == 5:
            organize_by_extension(folder, files, user_choices)

    choice = input('Would you like to save this configuration to a configuration file? (y/n): ')
    if choice == 'y':
        with open('config.json', 'w', encoding='utf-8') as config_file:
            json.dump(user_choices, config_file, ensure_ascii=False, indent=4)

