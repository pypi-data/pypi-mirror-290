#!/usr/bin/env python3
"""Tests for the ManageSieve API."""

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
import re
import sys
import unittest

from typing import Final

sys.path.append(os.path.realpath(pathlib.Path(__file__).parents[1]))

from sievemgr import (Atom, Capabilities, Response, SieveManager,
                      SieveError, SieveConnectionError,
                      SieveOperationError, SieveProtocolError, URL)
from . import Test, makerunner


#
# Globals
#

SCRIPTNAMES: Final[tuple[Test[bool], ...]] = (
    # Simple tests
    (('',), False),
    *[((chr(i),), False) for i in range(32)],
    (('\0x7f',), False),
    *[((chr(i),), False) for i in range(0x80, 0xa0)],
    (('\0x2028',), False),
    (('\0x2029',), False),
    (('\0xfeff',), False),
    (('\n',), False),
    (('\r',), False),
    ('\0', False),

    # Paradigmatic cases
    (('foo',), True),
    (('bar.sieve',), True),

    # Edge cases
    ((' ',), True),

    # Non-ASCII characters
    (('𝚏õȫ',), True),
    (('𝕗ōȏ.ⓢℹéṽ𝕖',), True)
)


SCRIPTNAME_ERRORS: Final[tuple[Test[bool], ...]] = tuple(
    ((*args, True), exp if exp else ValueError) for args, exp in SCRIPTNAMES
)


CAPABILITIES: Final[tuple[Test[Capabilities], ...]] = (
    # Simple cases
    (([],), Capabilities()),
    (([['IMPLEMENTATION', '']],), Capabilities(implementation='')),
    (([['IMPLEMENTATION', 'Foo v1']],), Capabilities(implementation='Foo v1')),
    (([['SASL', '']],), Capabilities()),
    (([['SASL', 'FOO']],), Capabilities(sasl=('foo',))),
    (([['SASL', 'FOO BAR']],), Capabilities(sasl=('foo', 'bar'))),
    (([['SIEVE', '']],), Capabilities()),
    (([['SIEVE', 'foo']],), Capabilities(sieve=('foo',))),
    (([['SIEVE', 'foo bar']],), Capabilities(sieve=('foo', 'bar'))),
    (([['STARTTLS']],), Capabilities(starttls=True)),
    (([['MAXREDIRECTS', '0']],), Capabilities(maxredirects=0)),
    (([['MAXREDIRECTS', '1']],), Capabilities(maxredirects=1)),
    (([['MAXREDIRECTS', '1']],), Capabilities(maxredirects=1)),
    (([['MAXREDIRECTS', '4294967295']],),
     Capabilities(maxredirects=4294967295)),
    (([['NOTIFY', '']],), Capabilities()),
    (([['NOTIFY', 'foo']],), Capabilities(notify=('foo',))),
    (([['NOTIFY', 'foo bar']],), Capabilities(notify=('foo', 'bar'))),
    (([['OWNER', 'user']],), Capabilities(owner='user')),
    (([['VERSION', '1.0']],), Capabilities(version='1.0')),
    (([['UNAUTHENTICATE']],), Capabilities(unauthenticate=True)),

    # Examples from RFC 5804
    (
        ([
            ['IMPlemENTATION', 'Example1 ManageSieved v001'],
            ['SASl', 'DIGEST-MD5 GSSAPI'],
            ['SIeVE', 'fileinto vacation'],
            ['StaRTTLS'],
            ['NOTIFY', 'xmpp mailto'],
            ['MAXREdIRECTS', '5'],
            ['VERSION', '1.0']
        ],),
        Capabilities(
             implementation='Example1 ManageSieved v001',
             sasl=('digest-md5', 'gssapi'),
             sieve=('fileinto', 'vacation'),
             starttls=True,
             notify=('xmpp', 'mailto'),
             maxredirects=5,
             version='1.0'
        )
    ),
    (
        ([
            ['IMPlemENTATION', 'Example1 ManageSieved v001'],
            ['SASl', 'DIGEST-MD5 GSSAPI'],
            ['SIeVE', 'fileinto vacation'],
            ['StaRTTLS'],
            ['NOTIFY', 'xmpp mailto'],
            ['MAXREdIRECTS', '5'],
            ['OWNER', 'alexey@example.com'],
            ['VERSION', '1.0']
        ],),
        Capabilities(
            implementation='Example1 ManageSieved v001',
            sasl=('digest-md5', 'gssapi'),
            sieve=('fileinto', 'vacation'),
            starttls=True,
            notify=('xmpp', 'mailto'),
            owner='alexey@example.com',
            maxredirects=5,
            version='1.0'
        )
    ),

    # Real-world data
    (
        ([
            ['IMPLEMENTATION', 'Dovecot Pigeonhole'],
            ['SIEVE', 'fileinto reject envelope encoded-character '
                      'vacation subaddress comparator-i;ascii-numeric '
                      'relational regex imap4flags copy include '
                      'variables body enotify environment '
                      'mailbox date index ihave duplicate '
                      'vacation-seconds imapflags notify '
                      'vnd.dovecot.pgp-encrypt editheader'],
            ['NOTIFY', 'mailto'],
            ['SASL', ''],
            ['STARTTLS'],
            ['VERSION', '1.0']
        ],),
        Capabilities(
            implementation='Dovecot Pigeonhole',
            sieve=('fileinto', 'reject', 'envelope', 'encoded-character',
                   'vacation', 'subaddress', 'comparator-i;ascii-numeric',
                   'relational', 'regex', 'imap4flags', 'copy', 'include',
                   'variables', 'body', 'enotify', 'environment',
                   'mailbox', 'date', 'index', 'ihave', 'duplicate',
                   'vacation-seconds', 'imapflags', 'notify',
                   'vnd.dovecot.pgp-encrypt', 'editheader'),
            notify=('mailto',),
            starttls=True,
            version='1.0'
        )
    ),
    (
        ([
            ['IMPLEMENTATION', 'Dovecot Pigeonhole'],
            ['SIEVE', 'fileinto reject envelope encoded-character '
                      'vacation subaddress comparator-i;ascii-numeric '
                      'relational regex imap4flags copy include '
                      'variables body enotify environment '
                      'mailbox date index ihave duplicate '
                      'vacation-seconds imapflags notify '
                      'vnd.dovecot.pgp-encrypt editheader'],
            ['NOTIFY', 'mailto'],
            ['SASL', 'PLAIN LOGIN OAUTHBEARER XOAUTH2'],
            ['VERSION', '1.0']
        ],),
        Capabilities(
            implementation='Dovecot Pigeonhole',
            sieve=('fileinto', 'reject', 'envelope', 'encoded-character',
                   'vacation', 'subaddress', 'comparator-i;ascii-numeric',
                   'relational', 'regex', 'imap4flags', 'copy', 'include',
                   'variables', 'body', 'enotify', 'environment',
                   'mailbox', 'date', 'index', 'ihave', 'duplicate',
                   'vacation-seconds', 'imapflags', 'notify',
                   'vnd.dovecot.pgp-encrypt', 'editheader'),
            notify=('mailto',),
            sasl=('plain', 'login', 'oauthbearer', 'xoauth2'),
            version='1.0'
        )
    ),
    (
        ([
            ['IMPLEMENTATION', 'Cyrus timsieved (Murder) 2.5.17'],
            ['SASL', 'PLAIN'],
            ['SIEVE', 'comparator-i;ascii-numeric fileinto reject '
                      'vacation vacation-seconds imapflags notify '
                      'envelope imap4flags relational regex '
                      'subaddress copy date'],
            ['UNAUTHENTICATE']
        ],),
        Capabilities(
            implementation='Cyrus timsieved (Murder) 2.5.17',
            sasl=('plain',),
            sieve=('comparator-i;ascii-numeric', 'fileinto', 'reject',
                   'vacation', 'vacation-seconds', 'imapflags', 'notify',
                   'envelope', 'imap4flags', 'relational', 'regex',
                   'subaddress', 'copy', 'date'),
            unauthenticate=True
        )
    ),

    # Errors
    (([[]],), SieveProtocolError),
    (([['IMPLEMENTATION']],), SieveProtocolError),
    (([['IMPLEMENTATION', None]],), SieveProtocolError),
    (([['IMPLEMENTATION', True]],), SieveProtocolError),
    (([['IMPLEMENTATION', 0]],), SieveProtocolError),
    (([['IMPLEMENTATION', 1]],), SieveProtocolError),
    (([['IMPLEMENTATION', []]],), SieveProtocolError),
    (([['IMPLEMENTATION', 'foo', 'bar']],), SieveProtocolError),
    (([['SASL']],), SieveProtocolError),
    (([['SASL', None]],), SieveProtocolError),
    (([['SASL', True]],), SieveProtocolError),
    (([['SASL', 0]],), SieveProtocolError),
    (([['SASL', 1]],), SieveProtocolError),
    (([['SASL', []]],), SieveProtocolError),
    (([['SASL', 'foo', 'bar']],), SieveProtocolError),
    (([['SIEVE']],), SieveProtocolError),
    (([['SIEVE', None]],), SieveProtocolError),
    (([['SIEVE', True]],), SieveProtocolError),
    (([['SIEVE', 0]],), SieveProtocolError),
    (([['SIEVE', 1]],), SieveProtocolError),
    (([['SIEVE', []]],), SieveProtocolError),
    (([['SIEVE', 'foo', 'bar']],), SieveProtocolError),
    (([['MAXREDIRECTS']],), SieveProtocolError),
    (([['MAXREDIRECTS', None]],), SieveProtocolError),
    (([['MAXREDIRECTS', True]],), SieveProtocolError),
    (([['MAXREDIRECTS', 0]],), SieveProtocolError),
    (([['MAXREDIRECTS', 1]],), SieveProtocolError),
    (([['MAXREDIRECTS', []]],), SieveProtocolError),
    (([['MAXREDIRECTS', 'foo', 'bar']],), SieveProtocolError),
    (([['NOTIFY']],), SieveProtocolError),
    (([['NOTIFY', None]],), SieveProtocolError),
    (([['NOTIFY', True]],), SieveProtocolError),
    (([['NOTIFY', 0]],), SieveProtocolError),
    (([['NOTIFY', 1]],), SieveProtocolError),
    (([['NOTIFY', []]],), SieveProtocolError),
    (([['NOTIFY', 'foo', 'bar']],), SieveProtocolError),
    (([['OWNER']],), SieveProtocolError),
    (([['OWNER', None]],), SieveProtocolError),
    (([['OWNER', True]],), SieveProtocolError),
    (([['OWNER', 0]],), SieveProtocolError),
    (([['OWNER', 1]],), SieveProtocolError),
    (([['OWNER', []]],), SieveProtocolError),
    (([['OWNER', 'foo', 'bar']],), SieveProtocolError),
    (([['VERSION']],), SieveProtocolError),
    (([['VERSION', None]],), SieveProtocolError),
    (([['VERSION', True]],), SieveProtocolError),
    (([['VERSION', 0]],), SieveProtocolError),
    (([['VERSION', 1]],), SieveProtocolError),
    (([['VERSION', []]],), SieveProtocolError),
    (([['VERSION', 'foo', 'bar']],), SieveProtocolError),
)


MESSAGES: Final[tuple[Test[str], ...]] = (
    # No message
    ((Response(Atom('OK')),), 'server says OK'),
    ((Response(Atom('NO')),), 'server says NO'),
    ((Response(Atom('BYE')),), 'server says BYE'),

    # Empty message
    ((Response(Atom('OK'), message=''),), 'server says OK'),
    ((Response(Atom('NO'), message=''),), 'server says NO'),
    ((Response(Atom('BYE'), message=''),), 'server says BYE'),

    # Message
    ((Response(Atom('OK'), message='foo'),), 'foo'),
    ((Response(Atom('NO'), message='foo'),), 'foo'),
    ((Response(Atom('BYE'), message='foo'),), 'foo')
)


RESPONSES: Final[tuple[Test[Response], ...]] = (
    # Simple cases
    (([Atom('OK')],), Response(response=Atom('OK'))),
    (([Atom('NO')],), Response(response=Atom('NO'))),
    (([Atom('BYE')],), Response(response=Atom('BYE'))),

    # Response codes
    (([Atom('OK'), []],),
     Response(response=Atom('OK'))),
    (([Atom('NO'), []],),
     Response(response=Atom('NO'))),
    (([Atom('BYE'), []],),
     Response(response=Atom('BYE'))),
    (([Atom('OK'), [Atom('foo')]],),
     Response(response=Atom('OK'), code=(Atom('foo'),))),
    (([Atom('NO'), [Atom('foo')]],),
     Response(response=Atom('NO'), code=(Atom('foo'),))),
    (([Atom('BYE'), [Atom('foo')]],),
     Response(response=Atom('BYE'), code=(Atom('foo'),))),
    (([Atom('OK'), ['foo', 'bar']],),
     Response(response=Atom('OK'), code=('foo', 'bar'))),
    (([Atom('NO'), ['foo', 'bar']],),
     Response(response=Atom('NO'), code=('foo', 'bar'))),
    (([Atom('BYE'), ['foo', 'bar']],),
     Response(response=Atom('BYE'), code=('foo', 'bar'))),
    (([Atom('NO'), [None, True, False, 0, 1, [], 'foo']],),
     Response(response=Atom('NO'), code=(None, True, False, 0, 1, [], 'foo'))),
    (([Atom('NO'), [[[]]]],),
     Response(response=Atom('NO'), code=([[]],))),
    (([Atom('NO'), [[[Atom('NIL')]]]],),
     Response(response=Atom('NO'), code=([[Atom('NIL')]],))),

    # Messages
    (([Atom('OK'), 'Success'],),
     Response(response=Atom('OK'), message='Success')),
    (([Atom('NO'), 'Failure'],),
     Response(response=Atom('NO'), message='Failure')),
    (([Atom('BYE'), 'Bye'],),
     Response(response=Atom('BYE'), message='Bye')),

    # Full responses
    (([Atom('OK'), [Atom('WARNINGS')], 'foo'],),
     Response(Atom('OK'), ('warnings',), 'foo')),
    (([Atom('NO'), [Atom('AUTH-TOO-WEAK')], 'Authentication failed'],),
     Response(Atom('NO'), ('auth-too-weak',), 'Authentication failed')),
    (([Atom('NO'), [Atom('ENCRYPT-NEEDED')], 'Authentication failed'],),
     Response(Atom('NO'), ('encrypt-needed',), 'Authentication failed')),
    (([Atom('NO'), [Atom('QUOTA')], 'Over quota'],),
     Response(Atom('NO'), ('quota',), 'Over quota')),
    (([Atom('NO'), [Atom('QUOTA/MAXSCRIPTS')], 'Too many scripts'],),
     Response(Atom('NO'), ('quota/maxscripts',), 'Too many scripts')),
    (([Atom('NO'), [Atom('QUOTA/MAXSIZE')], 'Script too large'],),
     Response(Atom('NO'), ('quota/maxsize',), 'Script too large')),

    # Examples from RFC 5804
    (
        ([
            Atom('OK'), [
                Atom('SASL'),
                'cnNwYXV0aD1lYTQwZjYwMzM1YzQyN2I1NTI3Yjg0ZGJhYmNkZmZmZA=='
            ]
        ],),
        Response(
            Atom('OK'), (
                Atom('SASL'),
                'cnNwYXV0aD1lYTQwZjYwMzM1YzQyN2I1NTI3Yjg0ZGJhYmNkZmZmZA=='
            )
        )
    ),
    (
        ([
            Atom('OK'),
            [Atom('WARNINGS')],
            'line 8: server redirect action limit is 2, '
            'this redirect might be ignored'
        ],),
        Response(
            Atom('OK'),
            (Atom('WARNINGS'),),
            'line 8: server redirect action limit is 2, '
            'this redirect might be ignored'
        )
    ),
    (
        ([Atom('OK'), 'NOOP completed'],),
        Response(Atom('OK'), message='NOOP completed')
    ),
    (
        ([Atom('OK'), [Atom('TAG'), 'STARTTLS-SYNC-42'], 'Done'],),
        Response(Atom('OK'), (Atom('TAG'), 'STARTTLS-SYNC-42'), 'Done')
    ),
    (
        ([Atom('NO'), [Atom('QUOTA/MAXSIZE')], 'Quota exceeded'],),
        Response(Atom('NO'), (Atom('QUOTA/MAXSIZE'),), 'Quota exceeded')
    ),
    (
        ([Atom('NO'), 'line 2: Syntax error'],),
        Response(Atom('NO'), message='line 2: Syntax error')
    ),
    (
        ([Atom('BYE'), 'Too many failed authentication attempts'],),
        Response(
            Atom('BYE'),
            message='Too many failed authentication attempts'
        )
    ),

    # Errors
    (([],), SieveProtocolError),
    (([None],), SieveProtocolError),
    (([[]],), SieveProtocolError),
    ((['foo'],), SieveProtocolError),
    (([Atom('FOO'), None],), SieveProtocolError),
    (([Atom('FOO'), Atom('BAR')],), SieveProtocolError),
    (([Atom('FOO'), [Atom('BAR')], None],), SieveProtocolError),
    (([Atom('FOO'), 'foo', None],), SieveProtocolError),
    (([Atom('FOO'), [Atom('BAR')], 'foo', None],), SieveProtocolError),
    (([Atom('FOO'), [Atom('BAR')], 'foo', Atom('FOO')],), SieveProtocolError),
    (([Atom('FOO'), [Atom('BAR')], 'foo', []],), SieveProtocolError),
    (([Atom('FOO'), [Atom('BAR')], 'foo', 'foo'],), SieveProtocolError)
)


CODES: Final[tuple[Test[bool], ...]] = (
    # Edge cases
    ((Response(Atom('OK')),), False),
    ((Response(Atom('OK')), ''), False),
    ((Response(Atom('OK'), ('',)),), False),
    ((Response(Atom('OK'), ('',)), ''), True),
    ((Response(Atom('OK'), ('',)), 'foo'), False),
    ((Response(Atom('OK')), '/'), False),
    ((Response(Atom('OK'), ('/',)),), False),
    ((Response(Atom('OK'), ('/',)), '/'), True),
    ((Response(Atom('OK'), ('/',)), 'foo'), False),
    ((Response(Atom('OK'), ('',)), '/'), True),
    ((Response(Atom('OK'), ('/',)), ''), True),
    ((Response(Atom('OK'), ('foo',)), ''), False),
    ((Response(Atom('OK'), ('foo',)), '/'), False),

    # Category in tree
    ((Response(Atom('OK'), ('foo',)), 'foo'), True),
    ((Response(Atom('OK'), ('foo/',)), 'foo'), True),
    ((Response(Atom('OK'), ('foo/bar',)), 'foo'), True),
    ((Response(Atom('OK'), ('',)), 'Foo'), False),
    ((Response(Atom('OK'), ('Foo',)), ''), False),
    ((Response(Atom('OK'), ('Foo',)), 'foo'), True),
    ((Response(Atom('OK'), ('FoO/',)), 'foo'), True),
    ((Response(Atom('OK'), ('foO/BAR',)), 'foo'), True),
    ((Response(Atom('OK'), ('',)), 'FOO'), False),
    ((Response(Atom('OK'), ('foo',)), ''), False),
    ((Response(Atom('OK'), ('foo',)), 'FOO'), True),
    ((Response(Atom('OK'), ('foo/',)), 'Foo'), True),
    ((Response(Atom('OK'), ('foo/bar',)), 'fOo'), True),
    ((Response(Atom('OK'), ('foo',)), 'bar'), False),
    ((Response(Atom('OK'), ('foo/',)), 'bar'), False),
    ((Response(Atom('OK'), ('foo/bar',)), 'bar'), False),
    ((Response(Atom('OK'), ('Foo',)), 'bar'), False),
    ((Response(Atom('OK'), ('FoO/',)), 'bar'), False),
    ((Response(Atom('OK'), ('foO/BAR',)), 'bar'), False),
    ((Response(Atom('OK'), ('foo',)), 'Bar'), False),
    ((Response(Atom('OK'), ('foo/',)), 'bAr'), False),
    ((Response(Atom('OK'), ('foo/bar',)), 'baR'), False),

    # Tree in category
    ((Response(Atom('OK'), ('foo',)), ''), False),
    ((Response(Atom('OK'), ('foo',)), '/foo'), False),
    ((Response(Atom('OK'), ('foo',)), '/foo/'), False),
    ((Response(Atom('OK'), ('foo',)), '/foo/bar'), False),
    ((Response(Atom('OK'), ('foo',)), 'foo'), True),
    ((Response(Atom('OK'), ('foo',)), 'foo/'), True),
    ((Response(Atom('OK'), ('foo',)), 'foo/bar'), False),
    ((Response(Atom('OK'), ('Foo',)), 'foo'), True),
    ((Response(Atom('OK'), ('fOo',)), 'foo/'), True),
    ((Response(Atom('OK'), ('foO',)), 'foo/bar'), False),
    ((Response(Atom('OK'), ('foo',)), '/FOO'), False),
    ((Response(Atom('OK'), ('foo',)), '/foO/'), False),
    ((Response(Atom('OK'), ('foo',)), '/foo/BaR'), False),
    ((Response(Atom('OK'), ('foo',)), 'Foo'), True),
    ((Response(Atom('OK'), ('foo',)), 'fOo/'), True),
    ((Response(Atom('OK'), ('foo',)), 'foO/bAR'), False),
    ((Response(Atom('OK'), ('foo',)), 'bar/foo'), False),
    ((Response(Atom('OK'), ('foo',)), 'bar/foo'), False),
    ((Response(Atom('OK'), ('foo',)), 'bar/foo'), False),
    ((Response(Atom('OK'), ('Foo',)), 'bar/foo'), False),
    ((Response(Atom('OK'), ('FoO',)), 'bar/foo'), False),
    ((Response(Atom('OK'), ('foO',)), 'bar/foo'), False),
    ((Response(Atom('OK'), ('foo',)), 'Bar/FOO'), False),
    ((Response(Atom('OK'), ('foo',)), 'bAr/foO'), False),
    ((Response(Atom('OK'), ('foo',)), 'baR/Foo'), False),

    # Tree in tree
    ((Response(Atom('OK'), ('/bar',)), '/bar'), True),
    ((Response(Atom('OK'), ('/bar/',)), '/bar'), True),
    ((Response(Atom('OK'), ('/bar',)), '/bar/'), True),
    ((Response(Atom('OK'), ('/bar',)), '/foo'), False),
    ((Response(Atom('OK'), ('/bar/baz',)), '/bar'), True),
    ((Response(Atom('OK'), ('/bar',)), '/bar/baz'), False),
    ((Response(Atom('OK'), ('foo/bar',)), 'foo/bar'), True),
    ((Response(Atom('OK'), ('foo/bar/',)), 'foo/bar'), True),
    ((Response(Atom('OK'), ('foo/bar',)), 'foo/bar/'), True),
    ((Response(Atom('OK'), ('foo/bar',)), 'bar/foo'), False),
    ((Response(Atom('OK'), ('foo/bar/baz',)), 'foo/bar'), True),
    ((Response(Atom('OK'), ('foo/bar',)), 'foo/bar/baz'), False),

    # Regular expressions
    ((Response(Atom('OK'), ('.',)), '.'), True),
    ((Response(Atom('OK'), ('foo',)), '.'), False),
    ((Response(Atom('OK'), ('foo',)), '.*'), False),
)


ERRORS: Final[tuple[Test[SieveError], ...]] = (
    ((Response(Atom('')),), SieveOperationError(Atom(''))),
    ((Response(Atom('FOO')),), SieveOperationError(Atom('FOO'))),
    ((Response(Atom('OK')),), SieveOperationError(Atom('OK'))),
    ((Response(Atom('NO')),), SieveOperationError()),
    ((Response(Atom('BYE')),), SieveConnectionError()),
)


URLS: Final[tuple[Test[URL], ...]] = (
    (('foo',),
     URL(hostname='foo')),
    (('foo:0',),
     URL(hostname='foo', port=0)),
    (('foo/user',),
     URL(hostname='foo', owner='user')),
    (('foo/user/script',),
     URL(hostname='foo', owner='user', scriptname='script')),
    (('foo/user/script/script',),
     URL(hostname='foo', owner='user', scriptname='script/script')),
    (('sieve://foo',),
     URL(hostname='foo')),
    (('http://foo',),
     URL(scheme='http', hostname='foo')),
    (('user@foo',),
     URL(username='user', hostname='foo')),
    (('user:password@foo',),
     URL(username='user', password='password',  # nosec B106
         hostname='foo')),
    (('user:password@foo/jdoe',),
     URL(username='user', password='password',  # nosec B106
         hostname='foo', owner='jdoe')),
    (('sieve://user:password@foo/jdoe',),
     URL(username='user', password='password',  # nosec B106
         hostname='foo', owner='jdoe')),
    (('sieve://user:password@foo:123/jdoe/script',),
     URL(username='user', password='password',  # nosec B106
         hostname='foo', port=123, owner='jdoe', scriptname='script')),

    # Errors
    (('',), ValueError),
    (('sieve://',), ValueError),
    (('sieve://',), ValueError),
    ((':80',), ValueError),
    (('/foo',), ValueError),
    (('sieve://foo?bar=true',), ValueError),
)


REVERSEURLS: Final[tuple[Test[str], ...]] = tuple(
    ((u,), s if re.match(r'\w+://', s) else 'sieve://' + s)
    for ((s,), u) in URLS
    if not (isinstance(u, type) and issubclass(u, Exception))  # type: ignore
)


#
# Tests
#

class TestSieveManager(unittest.TestCase):
    test_validname = makerunner(SieveManager.validname, SCRIPTNAMES)
    test_validname_chk = makerunner(SieveManager.validname, SCRIPTNAME_ERRORS)


class TestCapabilities(unittest.TestCase):
    test_fromlines = makerunner(Capabilities.fromlines, CAPABILITIES)


class TestResponse(unittest.TestCase):
    test_str = makerunner(Response.__str__, MESSAGES)
    test_fromline = makerunner(Response.fromline, RESPONSES)
    test_matches = makerunner(Response.matches, CODES)
    test_toerror = makerunner(Response.toerror, ERRORS)


class TestURL(unittest.TestCase):
    test_fromurl = makerunner(URL.fromstr, URLS)
    test_str = makerunner(URL.__str__, REVERSEURLS)


#
# Boilerplate
#

if __name__ == '__main__':
    unittest.main()
