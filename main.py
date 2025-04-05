# Libraries
import logging
from os.path import isfile
from os import listdir

# Modules
from size_module import organize_by_size
from date_module import organize_by_date
from name_module import organize_by_name
from extension_module import organize_by_extension
from helper_functions import choose_option, clear_console, select_folder

# Variables
options = ['File size', 'Date created', 'Date modified', 'File name', 'Extension']
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Main function
if __name__ == '__main__':
    logging.info('File Organizer v1.0.0-beta')
    logging.info('To begin, please select the folder which contains the files you wish to organize.')

    folder = select_folder()
    if folder == '':
        exit(1)

    files = [f for f in listdir(folder) if isfile(os.path.join(folder, f))]

    if len(files) == 0:
        logging.error('No files detected in chosen folder.')
        exit(1)

    logging.info('The following files were detected in your chosen folder:')
    for f in files:
        logging.info(f)

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
