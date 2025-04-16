# Libraries
import logging, os, argparse
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
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Argparse setup
parser = argparse.ArgumentParser(prog='ClutterCutter',
                                 description='A Python utility to organize files in a directory based on various criteria like size, date, name, and extension.',
                                 usage='%(prog)s [options]')
parser.add_argument('--c', '--config', type=str, default='config.ini', help='Path to configuration file (default: config.ini)')
parser.add_argument('--d', '--directory', type=str, help='Path to directory which will be organized')
parser.add_argument('--p', '--preview', action='store_true', help='Preview the changes before running')
parser.add_argument('--r', '--recursive', action='store_true', help='Also process files in subdirectories of chosen directory')
parser.add_argument('--m', '--mode', type=str, choices=['size', 'date_created', 'date_modified', 'name', 'extension'], help='Change mode for organizing')
parser.add_argument('--a', '--arguments', nargs='+', help='Arguments, only if organizing mode is specified using --m or --mode')
args = parser.parse_args()

# Main function
if __name__ == '__main__':
    logging.info('ClutterCutter v.1.0.1')

    folder = args.d

    if not folder:
        logging.info('To begin, please select the folder which contains the files you wish to organize.')
        folder = select_folder()
        if folder == '':
            exit(1)
    else:
        logging.info('Running using the directory provided in the console argument(s).')

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

    if args.m:
        logging.info('Running using the provided arguments.')
        if args.m == 'size':
            organize_by_size(folder, files, args.a)

        if args.m == 'date_created' or args.m == 'date_modified':
            organize_by_date(folder, files, args.m, args.a)

        if args.m == 'name':
            organize_by_name(folder, files, args.a)

        if args.m == 'extension':
            organize_by_extension(folder, files, args.a)

    else:
        logging.info('Please select your desired mode for organizing files. Instructions and explanations for each mode will be shown after selection. You may choose between:\n')
        selected = choose_option(options)

        # Organizing
        if selected == 1:
            organize_by_size(folder, files)

        if selected == 2 or selected == 3:
            organize_by_date(folder, files, selected)

        if selected == 4:
            organize_by_name(folder, files)

        if selected == 5:
            organize_by_extension(folder, files)
