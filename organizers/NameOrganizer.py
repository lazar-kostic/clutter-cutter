from .Organizer import Organizer
import os, re, logging
from utils import valid_folder_name, create_folder, move_file
from FileSystemNode import apply_to_tree

class NameOrganizer(Organizer):
    def __init__(self, root_node, args=None):
        super().__init__(root_node, args)
        self.modes = ['First character', 'Chosen prefix', 'Chosen suffix', 'Chosen keyword', 'Chosen regex', 'Name length']
        self.selected_inner = 0
        self.string, self.regex = '', ''

        if not args: logging.info(
            'In this mode, the files will be split up into multiple folders depending on their name. Sort by:\n')

    def create_folders(self):
        if self.selected_inner in range(1, len(self.modes)) and self.selected_inner !=1:
            if self.selected_inner < 5:
                if self.args:
                    self.string = self.args[self.arg_counter]
                    self.arg_counter += 1
                else:
                    self.string = valid_folder_name('Please enter the ' + (
                        'prefix' if self.selected_inner == 2 else 'suffix' if self.selected_inner == 3 else 'keyword') + ' you wish to use:\n')
            else:
                if self.args:
                    self.regex = self.args[self.arg_counter]
                    self.arg_counter += 1
                else:
                    self.regex = input('Please enter the regex: ')

    def organize(self, file_node):
        if self.selected_inner in range(1, len(self.modes)):
            if self.selected_inner == 1:
                first_char = file_node.name[0].upper()
                dest_folder = os.path.join(self.root_node.name, first_char)
                dest_path = os.path.join(dest_folder, os.path.basename(file_node.name))
                if not os.path.exists(dest_folder):
                    create_folder(dest_folder)

                if not move_file(file_node.name, dest_path):
                    return False
                else:
                    return True

            else:
                if self.selected_inner == 2 and file_node.name.startswith(self.string):
                    dest_folder = os.path.join(self.root_node.name, 'Starts with ' + self.string)
                elif self.selected_inner == 3 and file_node.name.endswith(self.string):
                    dest_folder = os.path.join(self.root_node.name, 'Ends with ' + self.string)
                elif self.selected_inner == 4 and self.string in file_node.name:
                    dest_folder = os.path.join(self.root_node.name, 'Contains ' + self.string)
                elif self.selected_inner == 5 and re.search(self.regex, file_node.name):
                    dest_folder = os.path.join(self.root_node.name, 'Matches regex')
                else:
                    dest_folder = os.path.join(self.root_node.name, 'Other files')

                if not os.path.exists(dest_folder):
                    create_folder(dest_folder)

                dest_path = os.path.join(dest_folder, os.path.basename(file_node.name))
                if not move_file(file_node.name, dest_path):
                    return False
                else:
                    return True

        else:
            length = len(file_node.name)
            dest_folder = os.path.join(self.root_node.name, str(length) + ' characters')
            if not os.path.exists(dest_folder):
                create_folder(dest_folder)

            dest_path = os.path.join(dest_folder, os.path.basename(file_node.name))
            if not move_file(file_node.name, dest_path):
                return False
            else:
                return True

    def run_all(self):
        super().load_arguments()
        self.create_folders()
        if apply_to_tree(self.root_node, self.organize):
            return True, 'No errors'
        else:
            return False, 'Error'

