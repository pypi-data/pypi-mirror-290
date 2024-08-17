"""Test :class:`sievemgr.BaseShell`."""

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

import io
import itertools
import os
import pathlib
import shutil
import sys
import unittest

from typing import Final, Iterator, Optional, Sequence
from unittest.mock import patch

sys.path.append(os.path.realpath(pathlib.Path(__file__).parents[1]))

import sievemgr

from sievemgr import BaseShell, ConfirmEnum, ShellPattern, ShellWord
from . import Test, runtests


#
# Silence the bell
#

def silence():
    pass

sievemgr.bell = silence


#
# Functions
#

def addspaces(s: str, n: int = 3) -> Iterator[str]:
    for i in range(n):
        yield s + ' ' * i
        yield ' ' * i + s


def mixcase(s: str) -> Iterator[str]:
    yield from map(''.join, itertools.product(*zip(s.upper(), s.lower())))


#
# Globals
#

COMPLETIONS: Final[tuple[Test[Optional[str]], ...]] = (
    # Empty
    *[(('', '', i), cmd)
      for i, cmd in enumerate(('bar ', 'exit ', 'foo ', 'help ', None))],

    # Commands
    *[(('', cmd[0:i], j), cmd if j == 0 else None)
      for cmd in ('bar ', 'exit ', 'foo ', 'help ')
      for i in range(1, len(cmd))
      for j in (0, 1)],

    # Arguments
    (('exit ', '', 0), None),
    (('exit ', '', 1), None),
    (('help ', '', 0), 'bar '),
    (('help ', '', 1), 'exit '),
    (('help ', '', 2), 'foo '),
    (('help ', '', 3), 'help '),
    (('help ', '', 4), None),
    (('foo ', '', 0), 'bar '),
    (('foo ', '', 1), 'baz '),
    (('foo ', '', 2), 'foo '),
    (('foo ', '', 3), None),
    (('foo ', '', 4), None),
    (('foo ', 'b', 0), 'bar '),
    (('foo ', 'b', 1), 'baz '),
    (('foo ', 'b', 2), None),
    (('foo ', 'b', 3), None),
    (('foo ', 'ba', 0), 'bar '),
    (('foo ', 'ba', 1), 'baz '),
    (('foo ', 'ba', 2), None),
    (('foo ', 'ba', 3), None),
    (('foo ', 'bar', 0), 'bar '),
    (('foo ', 'bar', 1), None),
    (('foo ', 'bar', 2), None),
    (('foo ', 'baz', 0), 'baz '),
    (('foo ', 'baz', 1), None),
    (('foo ', 'baz', 2), None),
    (('foo ', 'bar ', 0), None),
    (('foo ', 'bar ', 1), None),
    (('foo ', 'baz ', 0), None),
    (('foo ', 'baz ', 1), None),
    (('foo ', 'f', 0), 'foo '),
    (('foo ', 'f', 1), None),
    (('foo ', 'f', 2), None),
    (('foo ', 'fo', 0), 'foo '),
    (('foo ', 'fo', 1), None),
    (('foo ', 'fo', 2), None),
    (('foo ', 'foo', 0), 'foo '),
    (('foo ', 'foo', 1), None),
    (('foo ', 'foo', 2), None),
    (('foo ', 'foo ', 0), None),
    (('foo ', 'foo ', 1), None),
    (('foo foo ', '', 0), 'quuuux'),
    (('foo foo ', '', 1), 'quuux'),
    (('foo foo ', '', 2), 'quux'),
    (('foo foo ', '', 3), None),
    (('foo foo ', 'q', 0), 'quuuux'),
    (('foo foo ', 'q', 1), 'quuux'),
    (('foo foo ', 'q', 2), 'quux'),
    (('foo foo ', 'q', 3), None),
    (('foo foo ', 'qu', 0), 'quuuux'),
    (('foo foo ', 'qu', 1), 'quuux'),
    (('foo foo ', 'qu', 2), 'quux'),
    (('foo foo ', 'qu', 3), None),
    (('foo foo ', 'quu', 0), 'quuuux'),
    (('foo foo ', 'quu', 1), 'quuux'),
    (('foo foo ', 'quu', 2), 'quux'),
    (('foo foo ', 'quu', 3), None),
    (('foo foo ', 'quuu', 0), 'quuuux'),
    (('foo foo ', 'quuu', 1), 'quuux'),
    (('foo foo ', 'quuu', 2), None),
    (('foo foo ', 'quuuu', 0), 'quuuux'),
    (('foo foo ', 'quuuu', 1), None),
    (('foo foo ', 'quuuuu', 0), None),
    (('foo foo ', 'quuuux', 0), 'quuuux'),
    (('foo foo ', 'quuuux', 1), None),
    (('foo foo ', 'quuuux ', 0), None),

    # Patterns
    (('foo ', '*', 0), 'bar '),
    (('foo ', '*', 1), 'baz '),
    (('foo ', '*', 2), 'foo '),
    (('foo ', '*', 3), None),
    (('foo ', 'f*', 0), 'foo '),
    (('foo ', 'f*', 1), None),
    (('foo ', 'fo*', 0), 'foo '),
    (('foo ', 'fo*', 1), None),
    (('foo ', 'f*o', 0), 'foo '),
    (('foo ', 'f*o', 1), None),
    (('foo ', 'fo?', 0), 'foo '),
    (('foo ', 'fo?', 1), None),
    (('foo ', 'f?o', 0), 'foo '),
    (('foo ', 'f?o', 1), None),
    (('foo ', 'fo[mno]', 0), 'foo '),
    (('foo ', 'fo[mno]', 1), None),
    (('foo ', 'f[o]o', 0), 'foo '),
    (('foo ', 'f[o]o', 1), None),
    (('foo ', 'f[np]o', 0), None)
)


CONFIRMATIONS: Final[tuple[Test[ConfirmEnum], ...]] = (
    # Defaults
    *[((' ' * i, enum), enum)
      for enum in ConfirmEnum
      for i in range(3)],

    # Yes, no, all, and none
    *[((z, ConfirmEnum.YES), ConfirmEnum.NO)
      for x in ('n', 'no')
      for y in mixcase(x)
      for z in addspaces(y)],
    *[((z, ConfirmEnum.NO), ConfirmEnum.YES)
      for x in ('y', 'yes')
      for y in mixcase(x)
      for z in addspaces(y)],
    *[((y, ConfirmEnum.YES, True), ConfirmEnum.NONE)
      for x in mixcase('none')
      for y in addspaces(x)],
    *[((y, ConfirmEnum.NO, True), ConfirmEnum.ALL)
      for x in mixcase('all')
      for y in addspaces(x)],

    # Errors
    *[((z, ConfirmEnum.NO), ValueError)
      for x in ('all', 'none')
      for y in mixcase(x)
      for z in addspaces(y)],
    *[((z, ConfirmEnum.NO, False), ValueError)
      for x in ('all', 'none')
      for y in mixcase(x)
      for z in addspaces(y)],
    *[((z, ConfirmEnum.NO), ValueError)
      for x in ('foo', 'bar', 'baz')
      for y in mixcase(x)
      for z in addspaces(y)],
    *[((z, ConfirmEnum.NO, False), ValueError)
      for x in ('foo', 'bar', 'baz')
      for y in mixcase(x)
      for z in addspaces(y)],
)


LINES: Final[tuple[Test[list[ShellWord]], ...]] = (
    # Simple
    (('foo',), ['foo']),
    (('foo bar',), ['foo', 'bar']),
    (('foo bar baz',), ['foo', 'bar', 'baz']),

    # Empty
    (('',), []),
    ((' ',), []),
    (('        ',), []),
    (('\t',), []),
    (('\t\n     ',), []),
    (('#',), []),
    (('# foo',), []),
    (('    # foo',), []),
    (('\t\n    # foo\\\nfoo',), []),

    # Leading and trailing whitespace
    ((' foo',), ['foo']),
    ((' foo bar',), ['foo', 'bar']),
    ((' foo bar baz',), ['foo', 'bar', 'baz']),
    (('foo ',), ['foo']),
    (('foo bar ',), ['foo', 'bar']),
    (('foo bar baz ',), ['foo', 'bar', 'baz']),
    ((r'foo\ ',), ['foo ']),
    ((r'foo bar\ ',), ['foo', 'bar ']),
    ((r'foo bar baz\ ',), ['foo', 'bar', 'baz ']),

    # Quotes
    (('"foo bar"',), ['foo bar']),
    (("'foo bar'",), ['foo bar']),

    # Escaped sequences
    ((r'foo\ bar',), ['foo bar']),
    ((r'\"foo bar"',), ['"foo', 'bar']),
    ((r"\'foo bar'",), ["'foo", 'bar']),

    # Escaped and quoted patterns
    ((r'\*',), ['*']),
    ((r'\?',), ['?']),
    ((r'\[',), ['[']),
    ((r'"*"',), ['*']),
    ((r'"?"',), ['?']),
    ((r'"["',), ['[']),
    ((r"'*'",), ['*']),
    ((r"'?'",), ['?']),
    ((r"'['",), ['[']),
    ((r'foo \*',), ['foo', '*']),
    ((r'\?\bar',), ['?bar']),
    ((r'\[foo]',), ['[foo]']),
    ((r'"foo *"',), ['foo *']),
    ((r'"b?r"',), ['b?r']),
    ((r'"[bar" ]',), ['[bar', ']']),
    ((r"'fo*' fo",), ['fo*', 'fo']),
    ((r"bar '?'",), ['bar', '?']),
    ((r"'['",), ['[']),
)


PATTERNSRAW: Final[tuple[Test[list[ShellWord]], ...]] = (
    (('* bar',), [ShellPattern('*'), 'bar']),
    (('? bar',), [ShellPattern('?'), 'bar']),
    (('[foo] bar',), [ShellPattern('[foo]'), 'bar']),
    ((r'\* bar',), [r'*', 'bar']),
    ((r'\? bar',), [r'?', 'bar']),
    ((r'\[foo] bar',), [r'[foo]', 'bar']),
    ((r'\** bar',), [ShellPattern(r'[*]*'), 'bar']),
    ((r'\?? bar',), [ShellPattern(r'[?]?'), 'bar']),
    ((r'\[foo][bar] baz',), [ShellPattern(r'[[]foo][bar]'), 'baz'])
)


PATTERNSEXP: Final[tuple[Test[list[ShellWord]], ...]] = (
    (('foo * ',), ['foo', 'bar', 'baz', 'foo']),
    (('foo ?oo',), ['foo', 'foo']),
    (('foo [f]oo',), ['foo', 'foo']),
    ((r'foo \*',), ['foo', '*']),
    ((r'foo \?',), ['foo', '?']),
    ((r'foo \[foo]',), ['foo', '[foo]']),
    ((r'foo \**',), ValueError),
    ((r'foo \??',), ValueError),
    ((r'foo \[foo][foo]',), ValueError)
)


USAGE: Final[tuple[Test[Optional[str]], ...]] = (
    ((None,), None),
    (('',), None),
    (('-',), None),
    ((' -',), None),
    (('- ',), None),
    ((' - ',), None),
    (('- foo',), None),
    (('-- foo',), 'usage: -'),
    (('frob',), 'usage: frob'),
    (('frob foo - frobnicate foo',), 'usage: frob foo'),
    (('frob [-o] foo - frobnicate foo',), 'usage: frob [-o] foo'),
)


WORDS: Final[tuple[Test[str], ...]] = (
    (((), 0), ''),
    ((('',), 0), '\n'),
    (((' ',), 0), '\n'),
    (((), 1), ''),
    ((('',), 1), '\n'),
    (((' ',), 1), '\n'),
    (((), 2), ''),
    ((('',), 2), '\n'),
    (((' ',), 2), '\n'),
    ((('foo',), 3), 'foo\n'),
    ((('foo', 'bar'), 3), 'foo\nbar\n'),
    ((('foo', 'bar'), 4), 'foo\nbar\n'),
    ((('foo', 'bar'), 6), 'foo\nbar\n'),
    ((('foo', 'bar'), 7), 'foo bar\n')
)


#
# Classes
#

class MockReadline():
    def __init__(self, line: str):
        for func in self.functions:
            self.mockups[func] = patch(func, autospec=True)
        self.line = line

    def __enter__(self) -> 'MockReadline':
        ctx = {func.removeprefix('readline.'): mockup.__enter__()
               for func, mockup in self.mockups.items()}
        ctx['get_begidx'].return_value = None
        ctx['get_line_buffer'].return_value = self.line
        return self

    def __exit__(self, exctype, excvalue, traceback):
        for mockup in self.mockups.values():
            mockup.__exit__(exctype, excvalue, traceback)

    functions = ('readline.get_begidx', 'readline.get_line_buffer')
    mockups: dict = {}


class TestShellMixin():
    def do_foo(self):
        pass

    def do_bar(self):
        pass

    def do_(self):
        pass

    def complete_foo(self, argidx, _) -> tuple[tuple[str, bool], ...]:
        if argidx == 0:
            return (('impossible', False),)
        if argidx == 1:
            return tuple((s, True) for s in ('foo', 'bar', 'baz'))
        if argidx == 2:
            return tuple((s, False) for s in ('quux', 'quuux', 'quuuux'))
        return ()


#
# Tests
#

class TestBaseShell(unittest.TestCase):
    # Wrappers
    @classmethod
    def columnise(cls, words: Sequence[str],
                  width: int = shutil.get_terminal_size().columns) -> str:
        buf = io.StringIO()
        cls.basecls.columnise(words, file=buf, width=width)
        return buf.getvalue()

    def complete(self, line: str, text: str, n: int) -> Optional[str]:
        with MockReadline(line=line):
            return self.shell.complete(text, n)

    @classmethod
    def confirm(cls, line: str, default: ConfirmEnum = ConfirmEnum.NO,
                multi: bool = False) -> ConfirmEnum:
        confirm = cls.basecls.confirm
        with patch('sievemgr.TermIO.readline', autospec=True) as readline:
            with patch('sievemgr.TermIO.write', autospec=True):
                readline.return_value = line
                return confirm('', default=default, multi=multi, attempts=1)

    def expand(self, line: str) -> list[ShellWord]:
        return self.shell.expand(line)

    @classmethod
    def getargs(cls, line: str) -> list[ShellWord]:
        with MockReadline(line=line):
            return cls.basecls.getargs()

    @classmethod
    def getusage(cls, docstring: Optional[str]) -> Optional[str]:
        def func():
            pass
        func.__doc__ = docstring
        return cls.basecls.getusage(func)

    @classmethod
    def split(cls, line: str) -> list[ShellWord]:
        return cls.basecls.split(line)

    # Setup
    def setUp(self):
        self.shellcls = type('TestShell', (self.basecls, TestShellMixin), {})
        self.shell = self.shellcls()

    # Tests
    def test_init(self):
        base = self.basecls()
        assert {'exit', 'help'} <= set(base.commands)
        sh = self.shellcls()
        assert {'bar', 'exit', 'foo', 'help'} <= set(sh.commands)

    def test_columnise(self):
        return runtests(self, self.columnise, WORDS)

    def test_complete(self):
        return runtests(self, self.complete, COMPLETIONS)

    @unittest.skipIf(os.getenv('QUICKTEST'), 'slow')
    def test_confirm(self):
        try:
            self.basecls.confirm('foo', attempts=0)
        except AssertionError:
            return
        self.fail('expected AssertionError')
        return runtests(self, self.confirm, CONFIRMATIONS)

    # TODO
    # def test_enter

    # TODO
    # def test_execute

    # TODO
    # def test_executeline

    # TODO
    # def test_executescript

    def test_expand(self):
        return runtests(self, self.expand, LINES + PATTERNSEXP)

    @unittest.skipIf(os.getenv('QUICKTEST'), 'slow')
    def test_getargs(self):
        return runtests(self, self.getargs, LINES + PATTERNSRAW)

    def test_getcommands(self):
        self.assertEqual(list(self.shell.getcommands()),
                         ['bar', 'exit', 'foo', 'help'])

    def test_getprompt(self):
        self.assertEqual(self.shell.getprompt(), '> ')

    def test_getusage(self):
        return runtests(self, self.getusage, USAGE)

    def test_split(self):
        return runtests(self, self.split, LINES + PATTERNSRAW)

    def test_do_exit(self):
        try:
            self.shell.do_exit()
        except StopIteration:
            return
        self.fail('expected StopIteration')

    # TODO
    # def test_do_help

    basecls: type[BaseShell] = BaseShell

    shellcls: type[BaseShell]


# TODO:
# * Test if aliases are resolved
# * Test if help messages are generated correctly
# * Add tests for ShellPattern


#
# Boilerplate
#

if __name__ == '__main__':
    unittest.main()
