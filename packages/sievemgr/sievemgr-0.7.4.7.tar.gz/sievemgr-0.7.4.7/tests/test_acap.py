#!/usr/bin/env python3
"""Tests for :class:`sievemgr.BaseACAPConn`."""

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

import copy
import io
import os
import pathlib
import sys
import unittest

from typing import Final, IO, Union, Sequence, TypeVar

sys.path.append(os.path.realpath(pathlib.Path(__file__).parents[1]))

from sievemgr import Atom, Line, Word, BaseACAPConn


#
# Types
#

T = TypeVar('T')

MyTest = tuple[bytes, list[Union[Word, io.BytesIO, io.StringIO, bytes]]]


#
# Globals
#

LITERAL: Final[bytes] = b'x' * 1025


BYTESTOLINE: Final[tuple[tuple[bytes, Line], ...]] = (
    # Simple tests
    (b'NIL\r\n', [None]),
    (b'FOO\r\n', [Atom('FOO')]),
    (b'0\r\n', [0]),
    (b'1\r\n', [1]),
    (b'4294967295\r\n', [4_294_967_295]),
    (b'""\r\n', ['']),
    (b'"0"\r\n', ['0']),
    (b'"foo"\r\n', ['foo']),
    (b'{%d+}\r\n%s\r\n' % (len(LITERAL), LITERAL), [LITERAL.decode('utf8')]),
    (b'()\r\n', [[]]),
    (b'(0 1 4294967295)\r\n', [[0, 1, 4_294_967_295]]),

    # Nested lists
    (b'1 (2 3) 4\r\n', [1, [2, 3], 4]),
    (b'1 (2 () 3) 4\r\n', [1, [2, [], 3], 4]),

    # Control characters
    (b'{1+}\r\n\0\r\n', ['\0']),
    (b'{1+}\r\n\r\r\n', ['\r']),
    (b'{1+}\r\n\n\r\n', ['\n']),
    (b'{2+}\r\n\0\r\r\n', ['\0\r']),
    (b'{2+}\r\n\n\r\r\n', ['\n\r']),
    (b'{3+}\r\n\n\0\r\r\n', ['\n\0\r']),

    # Spaces
    (b'" "\r\n', [' ']),
    (b'" foo"\r\n', [' foo']),
    (b'"foo "\r\n', ['foo ']),
    (b'"foo bar"\r\n', ['foo bar']),

    # ManageSieve commands
    (b'Authenticate "PLAIN" "QJIrweAPyo6Q1T9xu"\r\n',
     [Atom('Authenticate'), 'PLAIN', 'QJIrweAPyo6Q1T9xu']),
    (b'StartTls\r\n', [Atom('StartTls')]),
    (b'Logout\r\n', [Atom('Logout')]),
    (b'CAPABILITY\r\n', [Atom('CAPABILITY')]),
    (b'HAVESPACE "myscript" 999999\r\n',
     [Atom('HAVESPACE'), 'myscript', 999999]),
    (b'HAVESPACE "foobar" 435\r\n',
     [Atom('HAVESPACE'), 'foobar', 435]),
    (b'Putscript "foo" {31+}\r\n#comment\r\nInvalidSieveCommand\r\n\r\n',
     [Atom('Putscript'), 'foo', '#comment\r\nInvalidSieveCommand\r\n']),
    (b'Putscript "mysievescript" {97+}\r\n'
     b'require ["fileinto"];\r\n'
     b'\r\n'
     b'if envelope :contains "to" "tmartin+sent" {\r\n'
     b'  fileinto "INBOX.sent";\r\n'
     b'}\r\n',
     [Atom('Putscript'), 'mysievescript',
      'require ["fileinto"];\r\n'
      '\r\n'
      'if envelope :contains "to" "tmartin+sent" {\r\n'
      '  fileinto "INBOX.sent";\r\n'
      '}']),
    (b'Putscript "myforwards" {188+}\r\n'
     b'redirect "111@example.net";\r\n'
     b'\r\n'
     b'if size :under 10k {\r\n'
     b'    redirect "mobile@cell.example.com";\r\n'
     b'}\r\n'
     b'\r\n'
     b'if envelope :contains "to" "tmartin+lists" {\r\n'
     b'    redirect "lists@groups.example.com";\r\n'
     b'}\r\n',
     [Atom('Putscript'), 'myforwards',
      'redirect "111@example.net";\r\n'
      '\r\n'
      'if size :under 10k {\r\n'
      '    redirect "mobile@cell.example.com";\r\n'
      '}\r\n'
      '\r\n'
      'if envelope :contains "to" "tmartin+lists" {\r\n'
      '    redirect "lists@groups.example.com";\r\n'
      '}']),
     (b'Listscripts\r\n', [Atom('Listscripts')]),
     (b'listscripts\r\n', [Atom('listscripts')]),
     (b'Setactive "vacationscript"\r\n',
      [Atom('Setactive'), 'vacationscript']),
     (b'Setactive ""\r\n',
      [Atom('Setactive'), '']),
     (b'Setactive "baz"\r\n',
      [Atom('Setactive'), 'baz']),
     (b'Getscript "myscript"\r\n',
      [Atom('Getscript'), 'myscript']),
     (b'Deletescript "foo"\r\n',
      [Atom('Deletescript'), 'foo']),
     (b'Renamescript "foo" "bar"\r\n',
      [Atom('Renamescript'), 'foo', 'bar']),
     (b'Renamescript "baz" "bar"\r\n',
      [Atom('Renamescript'), 'baz', 'bar']),
     (b'CheckScript {31+}\r\n'
      b'#comment\r\n'
      b'InvalidSieveCommand\r\n\r\n',
      [Atom('CheckScript'),
       '#comment\r\n'
       'InvalidSieveCommand\r\n']),
     (b'NOOP\r\n', [Atom('NOOP')]),
     (b'NOOP "STARTTLS-SYNC-42"\r\n',
      [Atom('NOOP'), 'STARTTLS-SYNC-42']),
     (b'UNAUTHENTICATE\r\n', [Atom('UNAUTHENTICATE')]),

    # ManageSieve responses
    (b'OK\r\n', [Atom('OK')]),
    (b'Ok\r\n', [Atom('Ok')]),
    (b'oK\r\n', [Atom('oK')]),
    (b'ok\r\n', [Atom('ok')]),
    (b'NO\r\n', [Atom('NO')]),
    (b'No\r\n', [Atom('No')]),
    (b'nO\r\n', [Atom('nO')]),
    (b'no\r\n', [Atom('no')]),
    (b'BYE "Too many failed authentication attempts"\r\n',
     [Atom('BYE'), 'Too many failed authentication attempts']),
    (b'"IMPLEMENTATION" "Example1 ManageSieved v001"\r\n',
     ['IMPLEMENTATION', 'Example1 ManageSieved v001']),
    (b'"VERSION" "1.0"\r\n',
     ['VERSION', '1.0']),
    (b'"SASL" "PLAIN SCRAM-SHA-1 GSSAPI"\r\n',
     ['SASL', 'PLAIN SCRAM-SHA-1 GSSAPI']),
    (b'"SIEVE" "fileinto vacation"\r\n',
     ['SIEVE', 'fileinto vacation']),
    (b'"STARTTLS"\r\n', ['STARTTLS']),
    (b'NO (QUOTA/MAXSIZE) "Quota exceeded"\r\n',
     [Atom('NO'), [Atom('QUOTA/MAXSIZE')], 'Quota exceeded']),
    (b'NO "line 2: Syntax error"\r\n',
     [Atom('NO'), 'line 2: Syntax error']),
    (b'OK (WARNINGS) "line 8: server redirect action '
     b'limit is 2, this redirect might be ignored"\r\n',
     [Atom('OK'), [Atom('WARNINGS')],
      'line 8: server redirect action limit is 2, '
      'this redirect might be ignored']),
    (b'"summer_script"\r\n', ['summer_script']),
    (b'"vacation_script"\r\n', ['vacation_script']),
    (b'{13+}\r\nclever"script\r\n', ['clever"script']),
    (b'"main_script" ACTIVE\r\n',
     ['main_script', Atom('ACTIVE')]),
    (b'No (ACTIVE) "You may not delete an active script"\r\n',
     [Atom('No'), [Atom('ACTIVE')],
      'You may not delete an active script']),
    (b'No "bar already exists"\r\n',
     [Atom('No'), 'bar already exists']),
    (b'OK "NOOP completed"\r\n',
     [Atom('OK'), 'NOOP completed'])
)


RECEIVELINES: tuple[MyTest, ...] = (
    # Literals with and without continuation request
    (b'{3}\r\nfoo\r\n', ['foo']),
    (b'{3+}\r\nfoo\r\n', ['foo']),
    (b'{1}\r\n0\r\n', ['0']),
    (b'{3}\r\nfoo BAR\r\n', ['foo', Atom('BAR')]),
    (b'{1}\r\n\n', ['\n']),
    (b'{1+}\r\n\n', ['\n']),
    (b'{1}\r\n\r', ['\r']),
    (b'{1+}\r\n\r', ['\r']),
    (b'{2}\r\n\r\n', ['\r\n']),
    (b'{2+}\r\n\r\n', ['\r\n']),
    (b'{4}\r\n\nfoo', ['\nfoo']),
    (b'{4+}\r\n\nfoo', ['\nfoo']),
    (b'{4}\r\n\rfoo', ['\rfoo']),
    (b'{4+}\r\n\rfoo', ['\rfoo']),
    (b'{6}\r\n\r\nfoo', ['\r\nfoo']),
    (b'{6+}\r\n\r\nfoo', ['\r\nfoo']),
    (b'{4}\r\nfoo\n', ['foo\n']),
    (b'{4+}\r\nfoo\n', ['foo\n']),
    (b'{4}\r\nfoo\r', ['foo\r']),
    (b'{4+}\r\nfoo\r', ['foo\r']),
    (b'{6}\r\nfoo\r\n', ['foo\r\n']),
    (b'{6+}\r\nfoo\r\n', ['foo\r\n']),

    # Ridiculously complex ACAP line
    (b'(FOO NIL (NIL 0 "foo" {3}\r\nbar BAZ) 1 "foo") {3}\r\neof\r\n',
     [[Atom('FOO'), None,
       [None, 0, 'foo', 'bar', Atom('BAZ')],
       1, 'foo'], 'eof']),

    # ManageSieve responses
    (b'OK (TAG {16}\r\nSTARTTLS-SYNC-42) "Done"\r\n',
     [Atom('OK'), [Atom('TAG'), 'STARTTLS-SYNC-42'], 'Done'])
)

RECEIVELINE_ERRORS: tuple[tuple[bytes, type[Exception]], ...] = (
    # Garbage
    (b'{', ValueError),
    (b'{x}', ValueError),
    (b'}', ValueError),
    (b'(', ValueError),
    (b')', ValueError),
    (b'(()', ValueError),
    (b'0foo', ValueError),
    (b'!foo', ValueError)
)


SENDLINES: tuple[MyTest, ...] = (
    # Literals
    (b'{3+}\r\nfoo\r\n', [io.BytesIO(b'foo')]),
    (b'{3+}\r\nfoo\r\n', [io.StringIO('foo')]),
    (b'{1+}\r\n\n\r\n', [b'\n']),

    # Ridiculously complex ACAP line
    (b'(FOO NIL (NIL 0 "foo" BAZ) 1 "foo") "foo"\r\n', [
        [
            Atom('FOO'),
            None,
            [None, 0, 'foo', Atom('BAZ')],
            1,
            'foo'
        ],
        'foo'
    ]),

    # ManageSieve responses
    (b'OK (TAG "STARTTLS-SYNC-42") "Done"\r\n',
     [Atom('OK'), [Atom('TAG'), 'STARTTLS-SYNC-42'], 'Done'])

)


SENDLINE_ERRORS: tuple[tuple[Word, type[Exception]], ...] = (
    (-1, ValueError),
    (4_294_967_296, ValueError)
)


TOKENS: list[Word] = [
    None,
    Atom('atom'),
    0,
    4_294_967_295,
    '',
    ' ',
    '\0',
    '\n',
    '\r\n',
    'string',
    [],
    [[]]
]
"""Tokens to convert back-and-forth."""

# Create nested lists
TOKENS.append(copy.copy(TOKENS))


#
# Tests
#

class TestACAPConn(unittest.TestCase):
    def setUp(self):
        self.acap = MockACAP()

    def test_receiveline(self):
        acap = self.acap
        for i, (bytes_, objs) in enumerate(BYTESTOLINE + RECEIVELINES):
            with self.subTest(i=i, bytes_=bytes_, objs=objs):
                acap.file = io.BytesIO(bytes_)
                parsed = acap.receiveline()
                self.assertEqual(parsed, objs)
                for obj, cls in zip(parsed, map(type, objs)):
                    self.assertIsInstance(obj, cls)

    def test_receiveline_errors(self):
        acap = self.acap
        for i, (bytes_, exctype) in enumerate(RECEIVELINE_ERRORS):
            with self.subTest(i=i, bytes_=bytes_, exctype=exctype):
                acap.file = io.BytesIO(bytes_)
                try:
                    acap.receiveline()
                # pylint: disable=broad-exception-caught
                except Exception as exc:
                    self.assertIsInstance(exc, exctype)
                    continue
                self.fail(f'expected {exctype.__name__}')

    def test_sendline(self):
        acap = self.acap
        for i, (bytes_, objs) in enumerate(BYTESTOLINE + SENDLINES):
            with self.subTest(i=i, bytes_=bytes_, objs=objs):
                acap.file = io.BytesIO()
                rewind(objs)
                acap.sendline(*objs)    # type: ignore
                serialised = acap.file.getvalue()
                self.assertEqual(serialised, bytes_)

    def test_sendline_errors(self):
        acap = self.acap
        for i, (obj, exctype) in enumerate(SENDLINE_ERRORS):
            with self.subTest(i=i, obj=obj, exctype=exctype):
                try:
                    acap.sendline(obj)
                # pylint: disable=broad-exception-caught
                except Exception as exc:
                    self.assertIsInstance(exc, exctype)
                    continue
                self.fail(f'expected {exctype.__name__}')

    def test_sendline_partial(self):
        acap = self.acap
        for i, (bytes_, objs) in enumerate(BYTESTOLINE + SENDLINES):
            with self.subTest(i=i, bytes_=bytes_, objs=objs):
                acap.file = io.BytesIO()
                rewind(objs)
                acap.sendline(*objs, whole=False)   # type: ignore
                serialised = acap.file.getvalue()
                self.assertEqual(serialised, bytes_.removesuffix(b'\r\n'))

    @unittest.skipIf(os.getenv('QUICKTEST'), 'slow')
    def test_mutual(self):
        acap = self.acap
        for i, objs in enumerate(powerset(TOKENS)):
            with self.subTest(i=i, objs=objs):
                acap.file = io.BytesIO()
                acap.sendline(*objs)
                acap.file.seek(0)
                parsed = acap.receiveline()
                self.assertEqual(parsed, objs)


#
# Classes
#

class MockACAP(BaseACAPConn):
    file: IO[bytes] = io.BytesIO()  # type: ignore


#
# Functions
#

def powerset(elems: Sequence[T]) -> list[list[T]]:
    n = len(elems)
    return [[elems[k] for k in range(n) if i & 1 << k] for i in range(2 ** n)]


def rewind(objs):
    for obj in objs:
        if isinstance(obj, io.IOBase) and obj.seekable():
            obj.seek(0)


#
# Boilerplate
#

if __name__ == '__main__':
    unittest.main()
