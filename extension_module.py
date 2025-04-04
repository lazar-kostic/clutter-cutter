def organize_by_extension(folder, files):
    """
    Organizes files in the specified folder by their extensions. The user can choose to organize files into separate folders for each extension or based on their type (photos, videos, documents, etc.).
    :param folder: The folder where the files are located.
    :param files: A list of file names to be organized.
    """

    import os, shutil, logging
    from helper_functions import choose_option, extract_extension

    logging.info('In this mode, the files will be split up into multiple folders depending on their extension. You can choose between organizing files into separate folders for each different\n'
          'extension found (e. g. "png", "mp4", "pdf"), and organizing them into folders based on their type (e. g. photos, videos, documents).')

    folder_name = None
    options = ['Separately for each extension', 'Based on type (photos, videos, documents...)']
    groups = {
        'photos': ['png', 'jpg', 'jpeg', 'gif', 'bmp'],
        'videos': ['mp4', 'avi', 'mov', 'mkv'],
        'documents': ['pdf', 'doc', 'docx', 'txt', 'xls', 'xlsx'],
        'audio': ['mp3', 'wav', 'aac', 'flac'],
        'archives': ['zip', 'rar', 'tar', 'gz']
    }

    selected_inner = choose_option(options)

    # Create folders for each extension, and organize files into them
    for f in files:
        extension = extract_extension(f)
        if selected_inner == 1:
            if extension == '':
                logging.warning('Skipping file with no extension: ' + f)
                continue
            folder_name = os.path.join(folder, extension)

        elif selected_inner == 2:
            folder_name = None
            for group, extensions in groups.items():
                if extension in extensions:
                    folder_name = os.path.join(folder, group)
                    break
            if folder_name is None:
                folder_name = os.path.join(folder, 'Other')

        if os.path.exists(folder_name):
            try:
                shutil.move(os.path.join(folder, f), folder_name)
                logging.info(f'Moved file {f} to folder {folder_name}')
            except shutil.Error as e:
                logging.error(f"Error moving file {f}: {e}")
                choice = input('Do you want to continue? (y/n): ')
                if choice.lower() != 'y':
                    return False, 'Canceled by user'
        else:
            try:
                os.mkdir(folder_name)
                logging.info(f'Created new folder {folder_name}')
                shutil.move(os.path.join(folder, f), folder_name)
                logging.info(f'Moved file {f} to folder {folder_name}')
            except shutil.Error as e:
                logging.error(f"Error moving file {f}: {e}")
                choice = input('Do you want to continue? (y/n): ')
                if choice.lower() != 'y':
                    return False, 'Canceled by user'

    logging.info('Files organized by extension successfully.')
    return True, 'No errors'