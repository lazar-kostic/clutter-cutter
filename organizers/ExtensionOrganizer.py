from FileSystemNode import apply_to_tree
from .Organizer import Organizer
import os, logging
from utils import create_folder, extract_extension, move_file


class ExtensionOrganizer(Organizer):
    def __init__(self, root_node, args=None):
        super().__init__(root_node, args)
        self.arg_counter, self.selected_inner = 0, 0
        self.modes = ['Separately for each extension', 'Based on type (photos, videos, documents...)']
        self.groups = {
            'photos': ['png', 'jpg', 'jpeg', 'gif', 'bmp'],
            'videos': ['mp4', 'avi', 'mov', 'mkv'],
            'documents': ['pdf', 'doc', 'docx', 'txt', 'xls', 'xlsx'],
            'audio': ['mp3', 'wav', 'aac', 'flac'],
            'archives': ['zip', 'rar', 'tar', 'gz']
        }

        if not self.args: logging.info(
            'In this mode, the files will be split up into multiple folders depending on their extension. You can choose between organizing files into separate folders for each different'
            'extension found (e. g. "png", "mp4", "pdf"), and organizing them into folders based on their type (e. g. photos, videos, documents).')

    def create_folders(self):
        pass

    def organize(self, file_node):
        extension = extract_extension(file_node.name)

        if self.selected_inner == 1:
            if extension == '':
                logging.warning('Skipping file with no extension: ' + file_node.name)
                return True
            folder_name = os.path.join(self.root_node.name, extension)

            if not os.path.exists(folder_name):
                create_folder(folder_name)

            if not move_file(file_node.name, os.path.join(folder_name, os.path.basename(file_node.name))):
                return False
            return True

        elif self.selected_inner == 2:
            folder_name = None
            for group, extensions in self.groups.items():
                if extension in extensions:
                    folder_name = os.path.join(self.root_node.name, group)
                    break
            if folder_name is None:
                folder_name = os.path.join(self.root_node.name, 'Other')

            if not os.path.exists(folder_name):
                create_folder(folder_name)

            if not move_file(file_node.name, os.path.join(folder_name, os.path.basename(file_node.name))):
                return False
            return True

        return False

    def run_all(self):
        super().load_arguments()
        if apply_to_tree(self.root_node, self.organize):
            return True, 'No errors'
        else:
            return False, 'Error'


