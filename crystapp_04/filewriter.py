#!/usr/bin/env python
import pathlib
import os

from crystapp_04 import set_filename, path_exists

class GentleFileWriter:
    def __init__(self, folder, buffer, filename=None):
        self.buffer_path = pathlib.Path(buffer)
        if filename is None:
            self.data_path = pathlib.Path(set_filename(folder=folder))
        else:
            self.data_path = pathlib.Path(folder+filename)
        self.file = None

    def exists(self):
        return self.data_path.is_file()

    def has_parent(self):
        if path_exists(self.data_path.parent):
            return True
        return

    def _add_header(self):
        if not self.exists():
            if not self.has_parent():
                os.mkdir(self.data_path.parent)
            with open(self.data_path, "w+", encoding="UTF-8") as file:
                with open(self.buffer_path, "r", encoding="UTF-8") as buffer:
                    file.write(buffer.readline())
        else:
            if not self.header_is_ok():
                raise BufferError("New data colides old data!")

    def _delete(self):
        self.data_path.unlink()

    def header_is_ok(self):
        with open(self.data_path, "r", encoding="UTF-8") as file:
                with open(self.buffer_path, "r", encoding="UTF-8") as buffer:
                    if file.readline() == buffer.readline():
                        return True
                    return False

    def is_almost_empty(self):
        with open(self.data_path, "r", encoding="UTF-8") as file:
            # NOTE: read header first, that is the "almost" empty part
            file.readline()
            if not file.readline().strip():
                return True
            return False

    def __enter__(self):
        self._add_header()
        self.file = open(self.data_path, "a", encoding="UTF-8")
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
        if self.is_almost_empty():
            self._delete()
