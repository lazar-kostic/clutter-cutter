from .Organizer import Organizer
import os, time, logging
from datetime import datetime
from utils import convert_to_quarter, create_folder, move_file
from FileSystemNode import apply_to_tree

class DateOrganizer(Organizer):
    def __init__(self, root_node, selected, args=None):
        super().__init__(root_node, args)
        self.modes = ['Group by year', 'Group by month', 'Group by day', 'Group by weekday', 'Group by quarters']
        self.selected = selected
        self.formats = ['%Y', '%B', '%d']
        self.selected_inner = 0

        if not args: logging.info(
            'In this mode, the files will be split up into multiple folders depending on their date ' + (
            'created' if selected == 2 else 'modified') + '. '
            'The files can be organized into separate folders for each year, month, day, weekday (Monday - Sunday) or quarter. Please select between:\n')

    def create_folders(self):
        pass

    def organize(self, file_node):
        formatted_date = ''
        date_type = 'date_created' if self.selected == 2 else 'date_modified'
        if self.selected_inner <= 3:
            formatted_date = time.strftime(self.formats[self.selected_inner - 1], time.localtime(file_node.metadata[date_type]))
        elif self.selected_inner == 4:
            weekdays = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday",
                        7: "Sunday"}
            formatted_date = weekdays[datetime.fromtimestamp(file_node.metadata[date_type]).isoweekday()]
        elif self.selected_inner == 5:
            formatted_date = convert_to_quarter(datetime.fromtimestamp(file_node.metadata[date_type]))

        dest_folder = os.path.join(self.root_node.name, formatted_date)
        dest_path = os.path.join(dest_folder, os.path.basename(file_node.name))

        if not os.path.exists(dest_folder):
            create_folder(dest_folder)

        if not move_file(file_node.name, dest_path):
            return False
        return True

    def run_all(self):
        super().load_arguments()
        if apply_to_tree(self.root_node, self.organize):
            return True, 'No errors'
        else:
            return False, 'Error'

