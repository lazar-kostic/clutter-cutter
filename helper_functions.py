import re, os, logging
from tkinter import filedialog

def select_folder():
    folder_temp = filedialog.askdirectory(
        title='Select a folder',
        initialdir='/'
    )
    return folder_temp

def choose_option(list_of_options):
    for i in range(len(list_of_options)):
        logging.info(f'({i + 1}) {list_of_options[i]}')
    num = input('Please enter the number in front of your desired option:\n')
    if not num.isdigit() or int(num) < 1 or int(num) > len(list_of_options):
        return -1
    return int(num)

def convert_to_bytes(size_):
    size_ = size_.upper().strip()
    pattern = r'(\d+(?:.\d+)?)\s*(B|KB|MB|GB|TB)'
    match = re.search(pattern, size_)
    if not match:
        return -1

    number, unit = match.group(1), match.group(2)
    number_val = float(number)
    if unit == 'B':
        return int(number_val)
    elif unit == 'KB':
        return int(number_val * 1024)
    elif unit == 'MB':
        return int(number_val * 1024 * 1024)
    elif unit == 'GB':
        return int(number_val * 1024 * 1024 * 1024)
    elif unit == 'TB':
        return int(number_val * 1024 * 1024 * 1024 * 1024)
    else:
        return -1

def safe_input(min_value, max_value, message):
    while True:
        entered = input(message)
        if not entered.isdigit():
            logging.error('The value you entered is not a valid number.')
            continue

        entered = int(entered)

        if min_value <= entered <= max_value:
            return entered

        else:
            logging.error(f'The value entered must be between {min_value} and {max_value}.')

def in_range(num, min_, max_):
    if not str(num).isdigit():
        return False
    return min_ <= int(num) <= max_

def convert_to_quarter(date):
    quarter = (date.month - 1) // 3 + 1
    return f"{date.year}Q{quarter}"

# Currently unused
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def extract_extension(file_name):
    ext = os.path.splitext(file_name)[1]
    return ext[1:]

def valid_folder_name(message):
    while True:
        name = input(message)
        if not name:
            logging.error('The string cannot be empty.')
            continue

        if len(name) > 255:
            logging.error('The string is too long. Please enter a shorter string.')
            continue

        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        if any(char in name for char in invalid_chars):
            logging.error('The string contains invalid characters. Please enter a different string.')
            continue

        return name