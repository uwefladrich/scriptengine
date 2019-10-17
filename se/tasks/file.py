"""ScriptEngine file tasks"""

import os
import shutil

from se.tasks import Task
from se.helpers import render_string


class Copy(Task):
    """ScriptEngine Copy task: Copies files or directories. It needs 'src' and
    'dst' parameters when it is created, providing the source and destination
    paths for the copy operation. Directories are copied recursively,
    maintaining symlinks.
    """
    def __init__(self, parameters):
        super().__init__(__name__+".copy", parameters, required_parameters=["src", "dst"])

    def run(self, context):
        src_path = render_string(self.src, context)
        dst_path = render_string(self.dst, context)
        if os.path.isfile(src_path):
            self.log_info(f"Copy file: {src_path} --> {dst_path}")
            if os.path.isfile(dst_path):
                self.log_warning(f"Destination file '{dst_path}' exists already; overwriting")
            shutil.copy(src_path, dst_path)
        else:
            self.log_info(f"Copy directory: {src_path} --> {dst_path}")
            if os.path.exists(dst_path):
                raise RuntimeError(f"Target '{dst_path}' for directory copy exists already")
            shutil.copytree(src_path, dst_path, symlinks=True)


class Move(Task):
    """ScriptEngine Move task: Moves files or directories. It needs 'src' and
    'dst' parameters when it is created, providing the source and destination
    paths for the move operation.
    """
    def __init__(self, parameters):
        super().__init__(__name__+".move", parameters, required_parameters=["src", "dst"])

    def run(self, context):
        src_path = render_string(self.src, context)
        dst_path = render_string(self.dst, context)
        shutil.move(src_path, dst_path)


class Link(Task):
    """ScriptEngine Link task: Creates symlinks. It needs 'src' and 'dst'
    parameters when it is created, providing the source and destination paths
    for the link.
    """
    def __init__(self, parameters):
        super().__init__(__name__+".link", parameters, required_parameters=["src", "dst"])

    def run(self, context):
        src_path = render_string(self.src, context)
        dst_path = render_string(self.dst, context)
        os.symlink(src_path, dst_path)
        if not os.path.exists(dst_path):
            self.log_warning(f"Created dangling symlink: '{dst_path}-->{src_path}'")


class Remove(Task):
    """ScriptEngine Remove task: Removes (deletes) files or directories.
    Directories are removed recursively. It needs the 'src' parameter when it
    is created, providing the paths that is to be removed.
    """
    def __init__(self, parameters):
        super().__init__(__name__+".remove", parameters, required_parameters=["src"])

    def run(self, context):
        src_path = render_string(self.src, context)
        if os.path.exists(src_path):
            if os.path.isdir(src_path):
                self.log_info(f"Removing directory '{src_path}'")
                shutil.rmtree(src_path)
            else:
                self.log_info(f"Removing file '{src_path}'")
                os.remove(src_path)
        else:
            self.log_info(f"Non-existing path '{src_path}'; nothing removed")


class MakeDir(Task):
    """ScriptEngine MakeDir task: Creates a directory. It needs the 'dst'
    parameter when it is created, providing the path of the new directory
    """
    def __init__(self, parameters):
        super().__init__(__name__+".make_dir", parameters, required_parameters=["dst"])

    def run(self, context):
        dst_path = render_string(self.dst, context)
        if os.path.isdir(dst_path):
            self.log_info(f"Directory '{dst_path}' exists already.")
        elif os.path.isfile(dst_path):
            raise RuntimeError(f"'{dst_path}' is a file, can't create directory")
        else:
            self.log_info(f"Creating directory '{dst_path}'")
            os.makedirs(dst_path)
