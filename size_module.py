def organize_by_size(folder, files):
    """
    Organizes files into folders based on their size.
    :param folder: The folder where the files are located.
    :param files: A list of file names to be organized.
    """

    import os, shutil, logging
    from helper_functions import safe_input, convert_to_bytes

    logging.info(
        'In this mode, the files will be split up into multiple folders depending on their size. You can customize both the number of folders to organize them into, as well as\n'
        'the maximum file size for each folder. For example, you could create 3 folders, one for files up to 50MB, second for files up to 200MB, and third for files up to 1GB.')

    # Stores the file sizes in bytes, in the same order as the 'files' list
    file_sizes = []
    for f in files:
        try:
            file_sizes.append(os.path.getsize(os.path.join(folder, f)))
        except OSError as e:
            logging.error(f"Error getting size of file {f}: {e}")
            choice = input('Do you want to continue? (y/n): ')
            if choice.lower() != 'y':
                return False, 'Canceled by user'
            else:
                continue

    # Stores the number of folders to split files into
    num_folders = safe_input(2, 100, 'How many folders would you like to organize the files into?\n')

    # Stores the maximum file sizes allowed in each folder, in bytes
    logging.info(
        'Next, please enter the maximum size for the files in each folder, followed by the unit without spaces (e.g. 100MB, 1GB). If you skip the input for the last folder,\n'
        'all files exceeding the maximum size of all other folders will be stored into the last folder.')
    sizes, counter = [], 0
    while counter < num_folders:
        while True:
            size = input(f'Size for folder {counter + 1}: ')
            converted_size = convert_to_bytes(size)
            if converted_size == -1:
                if counter == num_folders - 1:
                    converted_size = float('inf')
                    size = 'Above max limit'
                    break
                else:
                    logging.error('Invalid size. Please enter a valid size.')
            else:
                break

        logging.info('Folder max size converted to bytes: ' + str(converted_size))
        sizes.append((size, converted_size))
        counter += 1

    sizes.sort(key=lambda x: x[1])

    # Stores the names of the newly created folders and creates them
    folder_names = []
    for size, _ in sizes:
        folder_name = 'Up to ' + size
        folder_path = os.path.join(folder, folder_name)
        if not os.path.exists(folder_path):
            try:
                os.mkdir(folder_path)
                logging.info(f'Created folder: {folder_name}')
            except OSError as e:
                logging.error(f"Error creating folder {folder_name}: {e}")
                return False, 'Error during folder creation'
        folder_names.append(folder_name)

    # Organizes the files into the folders based on their sizes
    for i in range(len(files)):
        for j in range(len(sizes)):
            if file_sizes[i] < sizes[j][1]:
                dest_folder = os.path.join(folder, folder_names[j])
                dest_path = os.path.join(dest_folder, files[i])
                try:
                    if not os.path.exists(dest_path):
                        shutil.move(os.path.join(folder, files[i]), dest_path)
                        logging.info(f'Moved file {files[i]} with size {file_sizes[i]} to folder {folder_names[j]}')
                    else:
                        logging.warning(f'File {files[i]} already exists in {folder_names[j]}. Skipping.')
                except shutil.Error as e:
                    logging.error(f"Error moving file {files[i]}: {e}")
                    choice = input('Do you want to continue? (y/n): ')
                    if choice.lower() != 'y':
                        return False, 'Canceled by user'
                break

    logging.info('Files organized by size successfully.')
    return True, 'No errors'