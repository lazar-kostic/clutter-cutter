def organize_by_date(folder, files, selected):
    """
    Organizes files by their date created or modified. The user can choose to organize the files by year, month, day, weekday, or quarter.
    :param folder: The folder where the files are located.
    :param files: A list of file names to be organized.
    :param selected: The selected option for organizing files (2 for date created, 3 for date modified).
    """

    import os, shutil, time, logging
    from datetime import datetime
    from helper_functions import choose_option, convert_to_quarter

    logging.info('In this mode, the files will be split up into multiple folders depending on their date ' + (
        'created' if selected == 2 else 'modified') + '.\n' 
        'The files can be organized into separate folders for each year, month, day, weekday (Monday - Sunday) or quarter. Please select between:\n')

    sorting_options = ['Group by year', 'Group by month', 'Group by day', 'Group by weekday', 'Group by quarters']
    sorting_formats = ['%Y', '%B', '%d']
    selected_inner = choose_option(sorting_options)

    dates = []

    for f in files:
        try:
            if selected == 2:
                dates.append(os.path.getctime(os.path.join(folder, f)))
            else:
                dates.append(os.path.getmtime(os.path.join(folder, f)))
        except OSError as e:
            logging.error(f"Error getting creation time of file {f}: {e}")
            choice = input('Do you want to continue? (y/n): ')
            if choice.lower() != 'y':
                return False, 'Canceled by user'
            else:
                continue

    for i in range(len(files)):
        formatted_date = ''
        if selected_inner <= 3:
            formatted_date = time.strftime(sorting_formats[selected_inner - 1], time.gmtime(dates[i]))
        elif selected_inner == 4:
            weekdays = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday",
                        7: "Sunday"}
            formatted_date = weekdays[datetime.fromtimestamp(dates[i]).isoweekday()]
        elif selected_inner == 5:
            formatted_date = convert_to_quarter(datetime.fromtimestamp(dates[i]))

        dest_folder = os.path.join(folder, formatted_date)
        dest_path = os.path.join(dest_folder, files[i])
        if not os.path.exists(dest_folder):
            try:
                os.mkdir(dest_folder)
                logging.info('Created folder: ' + dest_folder)
                shutil.move(os.path.join(folder, files[i]), dest_path)
                logging.info('Moved file: ' + files[i] + ' to ' + dest_folder)
            except shutil.Error as e:
                logging.error(f"Error moving file {files[i]}: {e}")
                choice = input('Do you want to continue? (y/n): ')
                if choice.lower() != 'y':
                    return False, 'Canceled by user'
                else:
                    continue
        else:
            try:
                shutil.move(os.path.join(folder, files[i]), dest_path)
                logging.info('Moved file: ' + files[i] + ' to ' + dest_folder)
            except shutil.Error as e:
                logging.error(f"Error moving file {files[i]}: {e}")
                choice = input('Do you want to continue? (y/n): ')
                if choice.lower() != 'y':
                    return False, 'Canceled by user'
                else:
                    continue

    logging.info('Files organized by date.')
    return True, 'No errors'
