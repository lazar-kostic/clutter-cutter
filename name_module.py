def organize_by_name(folder, files):
    """
    Organizes files by their name. The user can choose to organize the files by the first character, a chosen prefix, suffix, keyword, regex, or name length.
    :param folder: The folder where the files are located.
    :param files: A list of file names to be organized.
    """

    import os, shutil, re, logging
    from helper_functions import choose_option, valid_folder_name

    logging.info('In this mode, the files will be split up into multiple folders depending on their name. Sort by:\n')
    options=['First character', 'Chosen prefix', 'Chosen suffix', 'Chosen keyword', 'Chosen regex', 'Name length']
    selected_inner = choose_option(options)

    if selected_inner in range(1, len(options)):
        if selected_inner == 1:
            for f in files:
                try:
                    first_char = f[0].upper()
                    dest_folder = os.path.join(folder, first_char)
                    dest_path = os.path.join(dest_folder, f)
                    if not os.path.exists(dest_folder):
                        os.mkdir(dest_folder)
                        logging.info('Created folder: ' + dest_folder)

                    shutil.move(os.path.join(folder, f), dest_path)
                    logging.info('Moved file: ' + f + ' to folder ' + dest_folder)
                except shutil.Error as e:
                    logging.error(f"Error moving file {f}: {e}")
                    choice = input('Do you want to continue? (y/n): ')
                    if choice.lower() != 'y':
                        return False, 'Canceled by user'
        else:
            string, regex = '', ''
            if selected_inner < 5:
                string = valid_folder_name('Please enter the ' + ('prefix' if selected_inner == 2 else 'suffix' if selected_inner == 3 else 'keyword') + ' you wish to use:\n')
            else:
                regex = input('Please enter the regex: ')

            for f in files:
                if selected_inner == 2 and f.startswith(string):
                    folder_name = os.path.join(folder, 'Starts with ' + string)
                elif selected_inner == 3 and f.endswith(string):
                    folder_name = os.path.join(folder, 'Ends with ' + string)
                elif selected_inner == 4 and string in f:
                    folder_name = os.path.join(folder, 'Contains ' + string)
                elif selected_inner == 5 and re.search(regex, f):
                    folder_name = os.path.join(folder, 'Matches regex')
                else:
                    folder_name = os.path.join(folder, 'Other files')

                if not os.path.exists(folder_name):
                    try:
                        os.mkdir(folder_name)
                        logging.info('Created folder: ' + folder_name)
                    except OSError as e:
                        logging.error(f"Error creating folder {folder_name}: {e}")
                        choice = input('Do you want to continue? (y/n): ')
                        if choice.lower() != 'y':
                            return False, 'Canceled by user'
                try:
                    shutil.move(os.path.join(folder, f), folder_name)
                    logging.info('Moved file: ' + f + 'to folder ' + folder_name)
                except shutil.Error as e:
                    logging.error(f"Error moving file {f}: {e}")
                    choice = input('Do you want to continue? (y/n): ')
                    if choice.lower() != 'y':
                        return False, 'Canceled by user'

    else:
        for f in files:
            length = len(f)
            folder_name = os.path.join(folder, str(length) + ' characters')
            if not os.path.exists(folder_name):
                try:
                    os.mkdir(folder_name)
                    logging.info('Created folder: ' + folder_name)
                except OSError as e:
                    logging.error(f"Error creating folder {folder_name}: {e}")
                    choice = input('Do you want to continue? (y/n): ')
                    if choice.lower() != 'y':
                        return False, 'Canceled by user'

            try:
                shutil.move(os.path.join(folder, f), folder_name)
                logging.info('Moved file: ' + f + 'to folder ' + folder_name)
            except shutil.Error as e:
                logging.error(f"Error moving file {f}: {e}")
                choice = input('Do you want to continue? (y/n): ')
                if choice.lower() != 'y':
                    return False, 'Canceled by user'

    logging.info('Files organized by name.')
    return True, 'No errors'
