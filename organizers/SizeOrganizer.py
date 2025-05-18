from .Organizer import Organizer
from FileSystemNode import apply_to_tree
import os, logging
from utils import in_range, safe_input, convert_to_bytes, create_folder, move_file

class SizeOrganizer(Organizer):
    def __init__(self, root_node, args=None):
        super().__init__(root_node, args)
        self.sizes, self.folder_names = [], []
        self.counter, self.num_folders = 0, 0

        if not args: logging.info(
                "In this mode, the files will be split up into multiple folders depending on their size.\n"
                "You can customize both the number of folders to organize them into, as well as the maximum file size\n"
                "for each folder. For example, you could create 3 folders: one for files up to 50MB, a second \n"
                "for files up to 200MB, and a third for files up to 1GB."
            )

    def load_arguments(self):
        if self.args:
            self.num_folders = self.args[self.arg_counter]
            if not in_range(self.num_folders, 2, 100):
                logging.error('The provided choice for the number of folders is invalid.\n')
                self.num_folders = safe_input(2, 100, 'How many folders would you like to organize the files into?\n')
            self.num_folders = int(self.num_folders)
            self.arg_counter += 1
        else:
            self.num_folders = safe_input(2, 100, 'How many folders would you like to organize the files into?\n')

    def load_folder_names(self):
        if not self.args: logging.info(
            'Next, please enter the maximum size for the files in each folder, followed by the unit without spaces (e.g. 100MB, 1GB). If you skip the input for the last folder, '
            'all files exceeding the maximum size of all other folders will be stored into the last folder.')

        while self.counter < self.num_folders:
            while True:
                if self.args:
                    size = self.args[self.arg_counter]
                    self.arg_counter += 1
                else:
                    size = input(f'Size for folder {self.counter + 1}: ')
                size_in_bytes = convert_to_bytes(size)
                if size_in_bytes == -1:
                    if self.counter == self.num_folders - 1:
                        size_in_bytes = float('inf')
                        size = 'Above max limit'
                        break
                    else:
                        if self.args:
                            logging.error(
                                'The provided file size is invalid. Please change it to the correct format and restart the program.')
                            exit(1)
                        else:
                            logging.error('Invalid size. Please enter a valid size.')
                else:
                    break

            self.sizes.append((size, size_in_bytes))
            self.counter += 1

        self.sizes.sort(key=lambda x: x[1])

    def create_folders(self):
        for size, _ in self.sizes:
            folder_name = 'Up to ' + size
            folder_path = os.path.join(self.root_node.name, folder_name)
            create_folder(folder_path)
            self.folder_names.append(folder_name)

    def organize(self, file_node):
        for i in range(len(self.sizes)):
            if file_node.metadata['size'] < self.sizes[i][1]:
                dest_folder = os.path.join(self.root_node.name, self.folder_names[i])
                dest_path = os.path.join(dest_folder, os.path.basename(file_node.name))
                if not move_file(file_node.name, dest_path):
                    return False
                break
        return True

    def run_all(self):
        self.load_arguments()
        self.load_folder_names()
        self.create_folders()
        if apply_to_tree(self.root_node, self.organize):
            return True, 'No errors'
        else:
            return False, 'Error'
