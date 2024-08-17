"""Test :func:`sievemgr.backup`."""

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

import os
import pathlib
import shutil
import sys
import tempfile
import unittest

from os import path

sys.path.append(path.realpath(pathlib.Path(__file__).parents[1]))

from sievemgr import backup, readdir


#
# Cases
#

MOCK_ERRORS: tuple[tuple[str, int, type[Exception]], ...] = (
    ('foo', -1, ValueError),
    ('bar', 1, KeyError),
    ('bar', 2, KeyError)
)


FILE_ERRORS: tuple[tuple[str, int, type[Exception]], ...] = (
    ('foo', -1, ValueError),
    ('bar', 1, FileNotFoundError),
    ('bar', 2, FileNotFoundError)
)


#
# Tests
#

class TestMockup(unittest.TestCase):
    def backup(self, fname: str, keep: int):
        def getfiles() -> tuple[str, ...]:
            return tuple(self.filesystem)
        def copy(src: str, targ: str):
            if src not in self.filesystem:
                raise KeyError(src)
            self.filesystem.add(targ)
        def remove(fname: str):
            self.filesystem.remove(fname)
        return backup(fname, keep, getfiles, copy, remove)

    def test_error(self):
        for i, (fname, keep, exctype) in enumerate(MOCK_ERRORS):
            with self.subTest(i=i, keep=keep, exctype=exctype):
                self.filesystem = {'foo'}
                try:
                    self.backup(fname, keep)
                # pylint: disable=broad-exception-caught
                except Exception as err:
                    self.assertIsInstance(err, exctype)
                    continue
                self.fail(f'expected {exctype}')

    def test_noop(self):
        self.filesystem = {'foo'}
        self.backup('foo', 0)
        self.assertEqual(self.filesystem, {'foo'})

    def test_simple(self):
        for i in range(1, 12):
            with self.subTest(i=i):
                self.filesystem = {'foo'}
                for _ in range(i):
                    self.backup('foo', 1)
                self.assertEqual(len(self.filesystem), 2)
                self.assertIn('foo', self.filesystem)
                self.assertIn('foo~', self.filesystem)

    def test_numbered(self):
        for i in range(2, 11):
            with self.subTest(i=i):
                self.filesystem = {'foo'}
                delta = 2
                count = i + delta
                for _ in range(count):
                    self.backup('foo', i)
                self.assertEqual(len(self.filesystem), i + 1)
                self.assertIn('foo', self.filesystem)
                for j in range(delta, count):
                    self.assertIn(f'foo.~{j + 1}~', self.filesystem)

    filesystem: set[str] = set()


class TestFile(unittest.TestCase):
    def backup(self, fname: str, keep: int):
        return backup(fname, keep, lambda: readdir(''), shutil.copy, os.remove)

    def test_error(self):
        oldwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                with open('foo', 'w', encoding='utf8'):
                    pass
                for i, (fname, keep, exctype) in enumerate(FILE_ERRORS):
                    with self.subTest(i=i, fname=fname,
                                      keep=keep, exctype=exctype):
                        try:
                            self.backup(fname, keep)
                        # pylint: disable=broad-exception-caught
                        except Exception as err:
                            self.assertIsInstance(err, exctype)
                            continue
                        self.fail(f'expected {exctype}')

            finally:
                os.chdir(oldwd)

    def test_noop(self):
        oldwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                with open('foo', 'w', encoding='utf8'):
                    pass
                self.backup('foo', 0)
                self.assertEqual(len(list(readdir('.', path.isfile))), 1)
            finally:
                os.chdir(oldwd)

    def test_simple(self):
        oldwd = os.getcwd()
        for i in range(1, 12):
            with self.subTest(i=i):
                with tempfile.TemporaryDirectory() as tmpdir:
                    try:
                        os.chdir(tmpdir)
                        with open('foo', 'w', encoding='utf8'):
                            pass
                        for _ in range(i):
                            self.backup('foo', 1)
                        files = list(readdir('', path.isfile))
                        self.assertEqual(len(files), 2)
                        self.assertIn('foo', files)
                        self.assertIn('foo~', files)
                    finally:
                        os.chdir(oldwd)

    def test_numbered(self):
        oldwd = os.getcwd()
        for i in range(2, 12):
            with self.subTest(i=i):
                delta = 2
                count = i + delta
                with tempfile.TemporaryDirectory() as tmpdir:
                    try:
                        os.chdir(tmpdir)
                        with open('foo', 'w', encoding='utf8'):
                            pass
                        for _ in range(count):
                            self.backup('foo', i)
                        files = list(readdir('', path.isfile))
                        self.assertEqual(len(files), i + 1)
                        self.assertIn('foo', files)
                        for j in range(delta, count):
                            self.assertIn(f'foo.~{j + 1}~', files)
                    finally:
                        os.chdir(oldwd)


#
# Boilerplate
#

if __name__ == '__main__':
    unittest.main()
