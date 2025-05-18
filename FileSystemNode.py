import os

class FileSystemNode:
    def __init__(self, name, is_directory=False):
        self.name = name
        self.is_directory = is_directory
        self.children = [] if is_directory else None
        if not name:
            self.metadata = {}
        else:
            self.metadata = {
                'size': os.path.getsize(self.name),
                'date_created': os.path.getctime(self.name),
                'date_modified': os.path.getmtime(self.name)
            }


    def add_child(self, child):
        if self.is_directory:
            self.children.append(child)
            return True
        return False

def build_filesystem_tree(start_path):
    path_to_node = {}
    has_files = False

    for dirpath, dirnames, filenames in os.walk(start_path):
        if dirpath not in path_to_node:
            node = FileSystemNode(dirpath, is_directory=True)
            path_to_node[dirpath] = node
        else:
            node = path_to_node[dirpath]

        for fname in filenames:
            file_node = FileSystemNode(os.path.join(dirpath, fname), is_directory=False)
            node.add_child(file_node)
            has_files = True

        for dname in dirnames:
            subdir_path = os.path.join(dirpath, dname)
            subdir_node = FileSystemNode(subdir_path, is_directory=True)
            path_to_node[subdir_path] = subdir_node
            node.add_child(subdir_node)

    return path_to_node[start_path], has_files

def build_shallow_filesystem_tree(start_path):
    root = FileSystemNode(start_path, is_directory=True)
    has_files = False

    for entry in os.listdir(start_path):
        full_path = os.path.join(start_path, entry)
        if os.path.isfile(full_path):
            file_node = FileSystemNode(full_path, is_directory=False)
            root.add_child(file_node)
            has_files = True

    return root, has_files

def print_tree(node, indent=0):
    print('  ' * indent + os.path.basename(node.name) + ('/' if node.is_directory else ''))
    if node.is_directory:
        for child in node.children:
            print_tree(child, indent + 1)

def apply_to_tree(node, function):
    for child in node.children:
        if child.is_directory:
            apply_to_tree(child, function)
        else:
            if not function(child):
                return False
    return True