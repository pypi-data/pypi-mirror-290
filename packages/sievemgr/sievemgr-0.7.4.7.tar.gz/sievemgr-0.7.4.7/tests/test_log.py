"""Test :class:`sievemgr.LogIOWrapper`."""

#
# Copyright 2024  Odin Kroeger
#
# This file is part of SieveManager.
#
# SieveManager is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# SieveManager is distributed in the hope that it will be useful,
# but WITHOUT ALL WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SieveManager. If not, see <https://www.gnu.org/licenses/>.
#

# pylint: disable=missing-class-docstring,missing-function-docstring


#
# Modules
#

import logging
import os
import pathlib
import sys
import tempfile
import unittest

sys.path.append(os.path.realpath(pathlib.Path(__file__).parents[1]))

from sievemgr import LogIOWrapper


#
# Tests
#

class TestLogIOWrapper(unittest.TestCase):
    """Tests for :class:`LogIOWrapper`."""

    def setUp(self):
        progname = os.path.basename(sys.argv[0])
        logging.basicConfig(format=f'{progname}: %(message)s')
        self.file = LogIOWrapper(tempfile.TemporaryFile())

    def tearDown(self):
        self.file.close()

    def test_close(self):
        file = LogIOWrapper(tempfile.TemporaryFile())
        file.close()
        self.assertTrue(file.closed)

    def test_closed(self):
        self.assertFalse(self.file.closed)

    def test_fileno(self):
        self.assertTrue(self.file.fileno() > 0)

    def test_flush(self):
        self.file.flush()

    def test_isatty(self):
        self.assertFalse(self.file.isatty())
        with open('/dev/tty', mode='rb') as tty:
            file = LogIOWrapper(tty)
            self.assertTrue(file.isatty())

    def test_iter(self):
        file = self.file
        pos = file.tell()
        write = (b'foo\n', b'bar\n', b'baz\n')
        file.writelines(write)
        file.seek(pos)
        read = tuple(line for line in file)
        self.assertEqual(read, write)

    def test_read(self):
        pos = self.file.tell()
        self.file.write(b'foo\n')
        self.file.seek(pos)
        self.assertEqual(self.file.read(), b'foo\n')

    def test_readinto(self):
        pos = self.file.tell()
        write = b'foo\n'
        self.file.write(write)
        self.file.seek(pos)
        read = bytearray(len(write))
        self.file.readinto(read)
        self.assertEqual(read, write)

    def test_readable(self):
        self.assertTrue(self.file.readable())

    def test_readline(self):
        pos = self.file.tell()
        self.file.write(b'foo\n')
        self.file.seek(pos)
        self.assertEqual(self.file.readline(), b'foo\n')

    def test_readlines(self):
        pos = self.file.tell()
        self.file.write(b'foo\nbar\n')
        self.file.seek(pos)
        self.assertEqual(self.file.readlines(), [b'foo\n', b'bar\n'])

    def test_seek(self):
        pos = self.file.tell()
        self.file.seek(0)
        self.assertEqual(self.file.tell(), 0)
        self.file.seek(pos)

    def test_seekable(self):
        self.assertTrue(self.file.seekable())

    def test_truncate(self):
        self.file.write(b'foo')
        self.file.seek(0)
        self.assertEqual(self.file.truncate(), 0)
        self.file.seek(0, os.SEEK_END)
        self.assertEqual(self.file.tell(), 0)

    def test_writable(self):
        return self.assertTrue(self.file.writable)

    def test_writelines(self):
        lines = [b'foo\n', b'bar\n']
        pos = self.file.tell()
        self.file.writelines(lines)
        self.file.seek(pos)
        self.assertEqual(self.file.readlines(), lines)


#
# Boilerplate
#

logging.getLogger(__name__).addHandler(logging.NullHandler())

if __name__ == '__main__':
    unittest.main()
