"""ScriptEngine file tasks
Provides Copy, Move, Link, Remove and MakeDir tasks
"""

import os
import shutil

from scriptengine.tasks.base import Task
from scriptengine.tasks.base.timing import timed_runner


class Copy(Task):
    """ScriptEngine Copy task: Copies files or directories. It needs 'src' and
    'dst' parameters when it is created, providing the source and destination
    paths for the copy operation. Directories are copied recursively,
    maintaining symlinks.
    """
    def __init__(self, parameters):
        super().__init__(parameters, required_parameters=["src", "dst"])

    @timed_runner
    def run(self, context):
        src = self.getarg('src', context)
        dst = self.getarg('dst', context)
        if os.path.isfile(src):
            self.log_info(f"Copy file: {src} --> {dst}")
            if os.path.isfile(dst):
                self.log_warning(f"Destination file '{dst}' exists already; overwriting")
            shutil.copy(src, dst)
        else:
            self.log_info(f"Copy directory: {src} --> {dst}")
            if os.path.exists(dst):
                raise RuntimeError(f"Target '{dst}' for directory copy exists already")
            shutil.copytree(src, dst, symlinks=True)


class Move(Task):
    """ScriptEngine Move task: Moves files or directories. It needs 'src' and
    'dst' parameters when it is created, providing the source and destination
    paths for the move operation.
    """
    def __init__(self, parameters):
        super().__init__(parameters, required_parameters=["src", "dst"])

    @timed_runner
    def run(self, context):
        src = self.getarg('src', context)
        dst = self.getarg('dst', context)
        self.log_info(f"Move file: {src} --> {dst}")
        shutil.move(src, dst)


class Link(Task):
    """ScriptEngine Link task: Creates symlinks. It needs 'src' and 'dst'
    parameters when it is created, providing the source and destination paths
    for the link.
    """
    def __init__(self, parameters):
        super().__init__(parameters, required_parameters=["src", "dst"])

    @timed_runner
    def run(self, context):
        src = self.getarg('src', context)
        dst = self.getarg('dst', context)
        self.log_info(f"Create link: {src} --> {dst}")
        os.symlink(src, dst)
        if not os.path.exists(dst):
            self.log_warning(f"Created dangling symlink: '{dst}-->{src}'")


class Remove(Task):
    """ScriptEngine Remove task: Removes (deletes) files or directories.
    Directories are removed recursively. It needs the 'path' parameter when it
    is created, providing the path to the file or directory to be removed.
    """
    def __init__(self, parameters):
        super().__init__(parameters, required_parameters=["path"])

    @timed_runner
    def run(self, context):
        path = self.getarg('path', context)
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
        super().__init__(parameters, required_parameters=["path"])

    @timed_runner
    def run(self, context):
        path = self.getarg('path', context)
        if os.path.isdir(path):
            self.log_info(f"Directory '{path}' exists already.")
        elif os.path.isfile(path):
            raise RuntimeError(f"'{path}' is a file, can't create directory")
        else:
            self.log_info(f"Creating directory '{path}'")
            os.makedirs(path)
