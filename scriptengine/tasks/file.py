"""ScriptEngine file tasks
Provides Copy, Move, Link, Remove and MakeDir tasks
"""

import os
import shutil

from scriptengine.tasks import Task
from scriptengine.jinja import render as j2render


class Copy(Task):
    """ScriptEngine Copy task: Copies files or directories. It needs 'src' and
    'dst' parameters when it is created, providing the source and destination
    paths for the copy operation. Directories are copied recursively,
    maintaining symlinks.
    """
    def __init__(self, parameters):
        super().__init__(__name__+".copy", parameters, required_parameters=["src", "dst"])

    def run(self, context):
        src_path = j2render(self.src, context)
        dst_path = j2render(self.dst, context)
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
        src_path = j2render(self.src, context)
        dst_path = j2render(self.dst, context)
        self.log_info(f"Move file: {src_path} --> {dst_path}")
        shutil.move(src_path, dst_path)


class Link(Task):
    """ScriptEngine Link task: Creates symlinks. It needs 'src' and 'dst'
    parameters when it is created, providing the source and destination paths
    for the link.
    """
    def __init__(self, parameters):
        super().__init__(__name__+".link", parameters, required_parameters=["src", "dst"])

    def run(self, context):
        src_path = j2render(self.src, context)
        dst_path = j2render(self.dst, context)
        self.log_info(f"Create link: {src_path} --> {dst_path}")
        os.symlink(src_path, dst_path)
        if not os.path.exists(dst_path):
            self.log_warning(f"Created dangling symlink: '{dst_path}-->{src_path}'")


class Remove(Task):
    """ScriptEngine Remove task: Removes (deletes) files or directories.
    Directories are removed recursively. It needs the 'path' parameter when it
    is created, providing the path to the file or directory to be removed.
    """
    def __init__(self, parameters):
        super().__init__(__name__+".remove", parameters, required_parameters=["path"])

    def run(self, context):
        path = j2render(self.path, context)
        if os.path.exists(path):
            if os.path.isdir(path):
                self.log_info(f"Removing directory '{path}'")
                shutil.rmtree(path)
            else:
                self.log_info(f"Removing file '{path}'")
                os.remove(path)
        else:
            self.log_info(f"Non-existing path '{path}'; nothing removed")


class MakeDir(Task):
    """ScriptEngine MakeDir task: Creates a directory. It needs the 'path'
    parameter when it is created, providing the path of the new directory
    """
    def __init__(self, parameters):
        super().__init__(__name__+".make_dir", parameters, required_parameters=["path"])

    def run(self, context):
        path = j2render(self.path, context)
        if os.path.isdir(path):
            self.log_info(f"Directory '{path}' exists already.")
        elif os.path.isfile(path):
            raise RuntimeError(f"'{path}' is a file, can't create directory")
        else:
            self.log_info(f"Creating directory '{path}'")
            os.makedirs(path)
