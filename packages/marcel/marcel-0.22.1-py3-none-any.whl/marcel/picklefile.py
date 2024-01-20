# This file is part of Marcel.
# 
# Marcel is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or at your
# option) any later version.
# 
# Marcel is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Marcel.  If not, see <https://www.gnu.org/licenses/>.

import os
import dill
import time


class PickleFile:

    def __init__(self, path):
        self.path = path
        self._readers = {}  # path -> Reader
        self._writer = None

    def __repr__(self):
        return f'{self.__class__.__name__}({self.path})'

    def __hash__(self):
        return self.path.hash()

    def __eq__(self, other):
        return self is other or (type(self) is type(other) and self.path == other.path)

    def __ne__(self, other):
        return not (self == other)

    def __iter__(self):
        return self.reader()

    def __enter__(self):
        return self.reader()

    def __exit__(self):
        self.close()
        return self

    def reader(self):
        assert self._writer is None, self
        reader = Reader(self)
        self._readers[self.path] = reader
        return reader

    def writer(self, append):
        assert len(self._readers) == 0 and self._writer is None, self
        writer = Writer(self, append)
        self._writer = writer
        return writer

    def ensure_deleted(self):
        assert len(self._readers) == 0 and self._writer is None, self
        try:
            os.unlink(self.path)
        except FileNotFoundError:
            pass

    def close(self):
        try:
            access = self._readers.pop(self.path)
        except KeyError:
            access = self._writer
            self._writer = None
        if access is not None:
            access.close_file()


class Access:

    def __init__(self, owner):
        self.owner = owner
        self.file = None

    def close(self):
        self.owner.close()

    def close_file(self):
        self.file.close()
        self.file = None


class Reader(Access):

    def __init__(self, owner):
        super().__init__(owner)
        self.file = open(owner.path, 'rb')
        self.unpickler = dill.Unpickler(self.file)

    def __next__(self):
        try:
            return self.read()
        except EOFError:
            self.close()
            raise StopIteration()
        except:
            self.close()
            raise

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def read(self):
        return self.unpickler.load()


class Writer(Access):

    FLUSH_INTERVAL_SEC = 1.0

    def __init__(self, owner, append):
        super().__init__(owner)
        self.append = append
        self.file = open(owner.path, 'ab' if self.append else 'wb')
        self.pickler = dill.Pickler(self.file)
        self.last_flush = time.time()

    def write(self, x):
        assert self.file is not None
        try:
            self.pickler.dump(x)
            now = time.time()
            if now - self.last_flush > Writer.FLUSH_INTERVAL_SEC:
                self.file.flush()
                self.last_flush = now
        except:
            self.close()
            raise
