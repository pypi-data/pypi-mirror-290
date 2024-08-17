"""Test :class:`sievemgr.TermIO`."""

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
import sys
import unittest

sys.path.append(os.path.realpath(pathlib.Path(__file__).parents[1]))

from sievemgr import TermIO


#
# Tests
#

class TestTermIO(unittest.TestCase):
    """Tests for :class:`TermIO`."""

    def setUp(self):
        self.tty = TermIO()

    def tearDown(self):
        if not self.tty.closed:
            self.tty.close()

    def test_close(self):
        tty = TermIO()
        tty.close()
        self.assertTrue(tty.closed)

    def test_closed(self):
        self.assertFalse(self.tty.closed)

    def test_fileno(self):
        self.assertTrue(self.tty.fileno() > 0)

    def test_flush(self):
        self.tty.flush()

    def test_isatty(self):
        self.assertTrue(self.tty.isatty())

    def test_read(self):
        self.assertEqual(self.tty.read(0), '')

    def test_readable(self):
        self.assertTrue(self.tty.readable())

    def test_write(self):
        self.tty.write('')

    def test_writable(self):
        return self.assertTrue(self.tty.writable)


#
# Boilerplate
#

if __name__ == '__main__':
    unittest.main()
