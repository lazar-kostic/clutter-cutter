from abc import abstractmethod
from utils import in_range, choose_mode
import logging

class Organizer:
    def __init__(self, root_node, args = None):
        self.root_node = root_node
        self.args = args
        self.arg_counter, self.selected_inner = 0, 0
        self.modes = []

    def load_arguments(self):
        if self.args:
            self.selected_inner = self.args[self.arg_counter]
            if not in_range(self.selected_inner, 1, len(self.modes)):
                logging.error('The provided choice for the sorting option is invalid.\n')
                selected_inner = choose_mode(self.modes)
            self.selected_inner = int(selected_inner)
            self.arg_counter += 1
        else:
            self.selected_inner = choose_mode(self.modes)

    @abstractmethod
    def create_folders(self):
        pass

    @abstractmethod
    def organize(self, file_node):
        pass

    @abstractmethod
    def run_all(self):
        pass
