#!/usr/bin/env python3
"""Client for managing Sieve scripts remotely using the ManageSieve protocol"""

#
# Copyright 2023 and 2024  Odin Kroeger
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


#
# Modules
#

from __future__ import annotations
from abc import ABC, abstractmethod
from base64 import b64decode, b64encode
from collections import UserDict, defaultdict, deque
from collections.abc import Iterable
from contextlib import suppress
from dataclasses import dataclass
from errno import (ECONNABORTED, EEXIST, EINPROGRESS, EISCONN,
                   ENOENT, ENOTCONN, ETIMEDOUT)
from fcntl import LOCK_SH, LOCK_NB
from getopt import GetoptError, getopt
from inspect import Parameter
from os import O_CREAT, O_EXCL, O_WRONLY, O_TRUNC, SEEK_END, SEEK_SET
from os import path
from signal import SIG_DFL, SIG_IGN, SIGHUP, SIGINT, SIGTERM
from tempfile import SpooledTemporaryFile, TemporaryDirectory
from typing import (Any, BinaryIO, Callable, ClassVar, Final, IO, Iterator,
                    NoReturn, Optional, Union, Sequence, TextIO, TypeVar)

import code
import contextlib
import dataclasses
import datetime
import enum
import fcntl
import fnmatch
import getpass
import hashlib
import hmac
import inspect
import io
import ipaddress
import itertools
import locale
import logging
import math
import netrc
import os
import pwd
import random
import re
import readline
import rlcompleter
import secrets
import select
import shlex
import shutil
import signal
import socket
import subprocess   # nosec B404
import ssl
import string
import stringprep
import sys
import threading
import types
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

try:
    from cryptography import x509
    from cryptography.hazmat.primitives.hashes import SHA1
    from cryptography.hazmat.primitives.serialization import Encoding
    from cryptography.x509 import (AuthorityInformationAccess,
                                   ExtensionNotFound, ocsp)
    from cryptography.x509.oid import AuthorityInformationAccessOID
    from cryptography.x509.ocsp import OCSPResponseStatus, OCSPCertStatus

    HAVE_CRYPTOGRAPHY: Final = True   # type: ignore
except ImportError:
    HAVE_CRYPTOGRAPHY: Final = False  # type: ignore

try:
    import dns.rdatatype
    import dns.resolver
    from dns.exception import DNSException

    HAVE_DNSPYTHON = True             # type: ignore
except ImportError:
    HAVE_DNSPYTHON = False            # type: ignore

if sys.version_info < (3, 9):
    sys.exit('SieveManager requires Python 3.9 or later')


#
# Metadata
#

__version__ = '0.7.4.7'
__author__ = 'Odin Kroeger'
__copyright__ = '2023 and 2024 Odin Kroeger'
__license__ = 'GPLv3+'
__all__ = [
    # ABCs
    'AbstractAuth',
    'AbstractSASLAdapter',

    # ManageSieve
    'SieveManager',
    'Atom',
    'Line',
    'Word',
    'Capabilities',
    'Response',
    'URL',

    # SASL
    'BaseAuth',
    'BasePwdAuth',
    'BaseScramAuth',
    'BaseScramPlusAuth',
    'CramMD5Auth',
    'ExternalAuth',
    'LoginAuth',
    'PlainAuth',
    'ExternalAuth',
    'ScramSHA1Auth',
    'ScramSHA1PlusAuth',
    'ScramSHA224Auth',
    'ScramSHA224PlusAuth',
    'ScramSHA256Auth',
    'ScramSHA256PlusAuth',
    'ScramSHA384Auth',
    'ScramSHA384PlusAuth',
    'ScramSHA512Auth',
    'ScramSHA512PlusAuth',
    'ScramSHA3_512Auth',
    'ScramSHA3_512PlusAuth',
    'SASLPrep',

    # Errors
    'Error',
    'ProtocolError',
    'SecurityError',
    'CapabilityError',
    'ConfigError',
    'DataError',
    'OperationError',
    'UsageError',
    'AppError',
    'AppConfigError',
    'AppConnectionError',
    'AppOperationError',
    'AppSecurityError',
    'OCSPError',
    'OCSPDataError',
    'OCSPOperationError',
    'SASLError',
    'SASLCapabilityError',
    'SASLProtocolError',
    'SASLSecurityError',
    'SieveError',
    'SieveCapabilityError',
    'SieveConnectionError',
    'SieveOperationError',
    'SieveProtocolError',
    'TLSError',
    'TLSCapabilityError',
    'TLSSecurityError'
]


#
# Globals
#

ABOUT: Final[str] = f'SieveManager {__version__}\nCopyright {__copyright__}'
"""About message."""

DEBUG: bool = False
"""Print stack traces even for expected error types?"""

EDITOR: Final[list[str]] = shlex.split(os.getenv('EDITOR', 'ed'), posix=True)
""":envvar:`EDITOR` or :command:`ed` if :envvar:`EDITOR` is unset."""

ENCODING: Final[str] = locale.getpreferredencoding(do_setlocale=False)
"""Encoding."""

HOME: Final[str] = os.getenv('HOME', pwd.getpwuid(os.getuid()).pw_dir)
"""Home directory."""

PAGER: Final[list[str]] = shlex.split(os.getenv('PAGER', 'more'), posix=True)
""":envvar:`PAGER` or :command:`more` if :envvar:`PAGER` is unset."""

VISUAL: Final[list[str]] = shlex.split(os.getenv('VISUAL', 'vi'), posix=True)
""":envvar:`VISUAL` or :command:`vi` if :envvar:`VISUAL` is unset."""

XDG_CONFIG_HOME: Final[str] = os.getenv('XDG_CONFIG_HOME', f'{HOME}/.config')
"""X Desktop group base configuration directory."""

CONFIGFILES: Final[tuple[str, ...]] = (
    '/etc/sieve/config',
    '/etc/sieve.cf',
    f'{XDG_CONFIG_HOME}/sieve/config',
    f'{HOME}/.sieve/config',
    f'{HOME}/.sieve.cf'
)
"""Default configuration files."""


#
# Types
#

class Atom(str):
    """ManageSieve keyword (e.g., ``LISTSCRIPTS``, ``OK``)."""

    # pylint: disable=eq-without-hash
    def __eq__(self, other) -> bool:
        return self.casefold() == other.casefold()

    def __ne__(self, other) -> bool:
        return self.casefold() != other.casefold()


AuthMech = type['AbstractAuth']
"""Alias for subclasses of :class:`AbstractAuth`."""


class AuthState(enum.IntEnum):
    """State of the authentication process."""

    PREAUTH = enum.auto()
    """"AUTHENTICATE" has *not* been issued."""

    SENT = enum.auto()
    """Data sent, ready to receive."""

    RECEIVED = enum.auto()
    """Data received, ready to send."""

    DONE = enum.auto()
    """Authentication concluded."""


class ConfirmEnum(enum.IntEnum):
    """Answers that :meth:`BaseShell.confirm` may return."""

    NO = 0
    YES = 1
    ALL = 2
    NONE = 3

    def __bool__(self) -> bool:
        return self in (self.YES, self.ALL)


Line = list['Word']
""":class:`List <list>` of :class:`Word`-s."""


class LogLevel(enum.IntEnum):
    """Logging levels supported by :class:`SieveConfig`."""

    AUTH = logging.DEBUG // 2
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR

    def fromdelta(self, delta: int) -> 'LogLevel':
        """Get a :class:`LogLevel` from a `delta`.

        For example:

        >>> LogLevel.INFO.fromdelta(-1)
        <LogLevel.WARNING: 30>
        >>> LogLevel.INFO.fromdelta(0)
        <LogLevel.INFO: 20>
        >>> LogLevel.INFO.fromdelta(1)
        <LogLevel.DEBUG: 10>
        >>> # Out-of-bounds deltas do not raise an error
        >>> LogLevel.INFO.fromdelta(-math.inf)
        <LogLevel.ERROR: 40>
        >>> LogLevel.INFO.fromdelta(math.inf)
        <LogLevel.AUTH: 5>
        """
        levels = list(self.__class__)
        index = levels.index(self) - delta
        return levels[min(max(index, 0), len(levels) - 1)]


class SASLPrep(enum.IntEnum):
    """Controls which strings are prepared for authentication.

    .. seealso::
        :rfc:`3454`
            Preparation of Internationalized Strings
        :rfc:`4013`
            Stringprep Profile for User Names and Passwords
        :rfc:`4422` (sec. 4)
            SASL protocol requirements
    """

    NONE = 0
    USERNAMES = 1
    PASSWORDS = 2
    ALL = 3


class ShellCmd(enum.IntEnum):
    """Shell actions that may overwrite or remove files."""

    NONE = 0
    CP = 1
    GET = 2
    MV = 4
    PUT = 8
    RM = 16
    ALL = 31


class ShellPattern(str):
    """:class:`BaseShell` pattern."""

    def __add__(self, other: Union['ShellPattern', str]) -> 'ShellPattern':
        return self.__class__(super().__add__(other))

    def __radd__(self, other: Union['ShellPattern', str]) -> 'ShellPattern':
        return self.__class__(other.__add__(self))


ShellWord = Union[ShellPattern, str]
"""Alias for :class:`ShellPattern` and `str`."""


Word = Union[Atom, None, int, str, Line]
"""Alias for :class:`Atom`, ``None``, ``int``, ``str``, and :class:`Line`."""


T = TypeVar('T')
"""Type variable."""


#
# Abstract base classes
#

AbstractAuthT = TypeVar('AbstractAuthT', bound='AbstractAuth')
"""Type variable for :class:`AbstractAuth`."""


class AbstractAuth(ABC):
    """Abstract base class for SASL mechanisms.

    The ManageSieve "AUTHENTICATE" command performs a `Simple Authentication
    and Security Layer`_ (SASL) protocol exchange. SASL is a framework that
    comprises different authentication mechanisms ("SASL mechanisms").
    :meth:`SieveManager.authenticate` does *not* implement any such mechanism
    itself, but delegates the SASL protocol exchange to classes that do.
    Such classes must subclass this class *and* have a :attr:`name`
    attribute that indicates the mechanism they implemented.

    .. tip::
        Do *not* subclass :class:`AbstractAuth` directly.
        Subclass :class:`BaseAuth` instead.

    .. seealso::
        :class:`AbstractSASLAdapter`
            Abstract base class for sending and receiving SASL messages.
        :rfc:`3454`
            Preparation of Internationalized Strings
        :rfc:`4013`
            Stringprep Profile for User Names and Passwords
        :rfc:`4422`
            Simple Authentication and Security Layer (SASL)
        :rfc:`5804` (sec. 2.1)
            ManageSieve "AUTHENTICATE" command
    """

    @abstractmethod
    def __init__(self, conn: 'AbstractSASLAdapter',
                 authcid: str, authzid: str = '',
                 prepare: SASLPrep = SASLPrep.ALL):
        """Prepare authentication.

        `authcid` and `authzid` are prepared according to :rfc:`3454` and
        :rfc:`4013` if the specification of the SASL mechanism mandates or
        recommends string preparation and ``prepare & SASLPrep.USERNAMES``
        evaluates as true.

        Arguments:
            conn: Connection over which to authenticate.
            authcid: Authentication ID (user to login as).
            authzid: Authorisation ID (user whose rights to acquire).
            prepare: Which credentials to prepare.

        Raises:
            ValueError: Bad characters in username.
        """

    @abstractmethod
    def __call__(self) -> Optional[Any]:
        """Authenticate as :attr:`authcid`.

        :attr:`authcid` is authorised as :attr:`authzid`
        if :attr:`authzid` is set (proxy authentication).

        Returns:
            Data returned by the server, if any.

        Raises:
            ConnectionError: Server has closed the connection.
            OperationError: Authentication failed.
            SASLCapabilityError: Some feature is not supported.
            SASLProtocolError: Server violated the SASL protocol.
            SASLSecurityError: Server verification failed.
            TLSCapabilityError: Channel-binding is not supported.
        """

    @classmethod
    def getmechs(cls: type[AbstractAuthT], sort: bool = True,
                 obsolete: bool = False) -> list[type[AbstractAuthT]]:
        """Get authentication classes that subclass this class.

        Arguments:
            sort: Sort mechanisms by :attr:`order`?
            obsolete: Return obsolete mechanisms?
        """
        mechs: list[type[AbstractAuthT]] = []
        for subcls in cls.__subclasses__():
            # pylint: disable=bad-indentation
            if (not subcls.__abstractmethods__
                and (obsolete or not subcls.obsolete)):
                    mechs.append(subcls)
            mechs.extend(subcls.getmechs(sort=False, obsolete=obsolete))
        if sort:
            mechs.sort(key=lambda s: s.order)
        return mechs

    name: ClassVar[str]
    """Mechanism name."""

    authcid: str
    """Authentication ID (user to login as)."""

    authzid: str = ''
    """Authorisation ID (user whose rights to acquire)."""

    obsolete: bool = False
    """Is this mechanism obsolete?"""

    order: int = 0
    """Mechanism precedence."""


class AbstractSASLAdapter(ABC):
    """Abstract base class for sending and receiving SASL messages.

    Messages that comprise an SASL protocol exchange ("SASL messages")
    must be translated to the underlying protocol. This class defines the
    types of messages that may occur in an SASL protocol exchange.
    Classes that translate between SASL and the underlying protocol
    must subclass this class.

    .. seealso::
        :class:`AbstractAuth`
            Abstract base class for SASL mechanisms.
        :rfc:`4422`
            Simple Authentication and Security Layer (SASL)
    """

    @abstractmethod
    def abort(self):
        """Abort authentication.

        Raises:
            ProtocolError: Protocol violation.
        """

    @abstractmethod
    def begin(self, name: str, data: Optional[bytes] = None):
        """Begin authentication.

        Arguments:
            name: SASL mechanism name.
            data: Optional client-first message.

        Raises:
            ConnectionError: Connection was closed.
            ProtocolError: Protocol violation.
        """

    @abstractmethod
    def end(self):
        """Conclude authentication.

        Raises:
            ConnectionError: Connection was closed.
            OperationError: Authentication failed.
            ProtocolError: Protocol violation.
        """

    @abstractmethod
    def send(self, data: bytes):
        """Encode and send an SASL message.

        Raises:
            ConnectionError: Connection was closed.
            ProtocolError: Protocol violation.
        """

    @abstractmethod
    def receive(self) -> bytes:
        """Receive and decode an SASL message.

        Raises:
            ConnectionError: Connection was closed.
            OperationError: Authentication failed.
            ProtocolError: Protocol violation.
        """

    @property
    @abstractmethod
    def sock(self) -> Union[socket.SocketType, ssl.SSLSocket]:
        """Underlying socket."""

    @sock.setter
    @abstractmethod
    def sock(self, sock: Union[socket.SocketType, ssl.SSLSocket]):
        pass


#
# ACAP
#

class BaseACAPConn(ABC):
    """Base class for ACAP parsers/serialisers.

    The ManageSieve uses the syntax and data types of the Application Control
    Access Protocol (ACAP). This class provides a :meth:`parser <receiveline>`
    for converting ACAP lines into Python objects and a :meth:`serialiser
    <sendline>` for converting Python objects into ACAP lines.

    .. seealso::
        :rfc:`2244` (secs. 2.2 and 2.6)
            ACAP commands, responses, and data formats.
        :rfc:`5804` (secs. 1.2 and 4)
            ManageSieve syntax.
    """

    # pylint: disable=missing-raises-doc
    def receiveline(self) -> Line:
        """Receive a line and parse it.

        ==================  =================
        ACAP type           Python type
        ==================  =================
        Atom                :class:`Atom`
        Literal             :class:`str`
        Nil                 ``None``
        Number              :class:`int`
        Parenthesised List  :class:`list`
        String              :class:`str`
        ==================  =================

        For example:

        >>> mgr.sendline(Atom('listscripts'))
        >>> mgr.receiveline()
        ['foo.sieve', 'ACTIVE']
        >>> mgr.receiveline()
        ['bar.sieve']
        >>> mgr.receiveline()
        ['baz.sieve']
        >>> mgr.receiveline()
        ['OK', 'Listscripts completed.']

        Raises:
            ValueError: Line is malformed.
        """
        assert self.file
        words: Line = []
        stack: list[Line] = []
        ptr: Line = words
        while line := self.file.readline().decode('utf8'):
            size: int = -1
            for token in self._lexpattern.finditer(line):
                key = token.lastgroup
                value = token.group(key)    # type: ignore[arg-type]
                if key == 'leftparen':
                    parens: list[Word] = []
                    stack.append(ptr)
                    ptr.append(parens)
                    ptr = parens
                elif key == 'rightparen':
                    try:
                        ptr = stack.pop()
                    except IndexError as err:
                        raise ValueError('unexpected parenthesis') from err
                elif key == 'atom':
                    if value.casefold() == 'nil':
                        ptr.append(None)
                    else:
                        ptr.append(Atom(value))
                elif key == 'number':
                    ptr.append(int(value))
                elif key == 'string':
                    ptr.append(value)
                elif key == 'literal':
                    size = int(value)
                    literal = self.file.read(size).decode('utf8')
                    ptr.append(literal)
                elif key == 'garbage':
                    raise ValueError('unrecognised data')
                else:
                    # NOTREACHED
                    raise AppSoftwareError('unknown data type')
            if size == -1:
                break
        if stack:
            raise ValueError('unbalanced parantheses')
        return words

    def sendline(self, *objs: Union[IO[Any], 'Word'], whole: bool = True):
        """Convert `objs` to ACAP types and send them.

        ==================  ======================================
        Python type         ACAP type
        ==================  ======================================
        :class:`Atom`       Atom
        :class:`typing.IO`  Literal
        ``None``            Nil
        :class:`bytes`      Literal or String [#literal]_
        :class:`list`       Parenthesised List
        :class:`int`        Number [#nums]_
        :class:`str`        Literal or String [#literal]_ [#utf8]_
        ==================  ======================================

        For example:

        >>> mgr.sendline(Atom('havespace'), 'script.sieve', 12345)
        >>> mgr.receiveline()
        ['OK', 'Putscript would succeed.']

        Pipeline commands:

        >>> mgr.isalive(check=True)
        >>> with open('foo.sieve') as script:
        >>>     mgr.sendline(Atom('putscript', script, 'foo.sieve'))
        >>> mgr.sendline(Atom('logout'))
        >>> for _ in range(2):
        >>>     mgr.collect(check=True)

        Arguments:
            objs: Objects to serialise.
            whole: Conclude data with CRLF?

        Raises:
            ValueError: Number is not within the range [0, 4,294,967,295].
            TypeError: Object cannot be represented as ACAP data type.

        .. [#literal] Depending on content.
        .. [#nums] Numbers must be within the range [0, 4,294,967,295]
        .. [#utf8] Strings are encoded in UTF-8 and normalised to form C.
        """
        assert self.file

        write = self.file.write
        normalize = unicodedata.normalize
        isstr = self._isstr

        def encode(s: str) -> bytes:
            return normalize('NFC', s).encode('utf8')

        def writestr(b: bytes):
            write(b'"%s"' % b if isstr(b) else b'{%d+}\r\n%s' % (len(b), b))

        for i, obj in enumerate(objs):
            if i > 0:
                write(b' ')
            if obj is None:
                write(b'NIL')
            elif isinstance(obj, Atom):
                write(encode(obj))
            elif isinstance(obj, int):
                if not 0 <= obj < 4_294_967_296:
                    raise ValueError(f'{obj}: not in [0, 4,294,967,295]')
                write(encode(str(obj)))
            elif isinstance(obj, bytes):
                writestr(obj)
            elif isinstance(obj, str):
                writestr(encode(obj))
            elif isinstance(obj, (IO, io.IOBase, SpooledTemporaryFile)):
                write(b'{%d+}\r\n' % getfilesize(obj))
                while block := obj.read(io.DEFAULT_BUFFER_SIZE):
                    write(encode(block) if isinstance(block, str) else block)
            elif isinstance(obj, Iterable):  # type: ignore
                write(b'(')
                self.sendline(*obj, whole=False)
                write(b')')
            else:
                raise TypeError(type(obj).__name__ + ': not an ACAP type')

        if whole:
            write(b'\r\n')
            self.file.flush()

    @property
    @abstractmethod
    def file(self) -> Optional[Union[IO, io.BufferedRWPair, LogIOWrapper]]:
        """File-like access to the underlying socket."""

    @file.setter
    @abstractmethod
    def file(self, file: Optional[Union[IO, io.BufferedRWPair, LogIOWrapper]]):
        pass

    _lexpattern: re.Pattern = re.compile('|'.join((
        r'\b(?P<atom>[a-z][^(){}\s\\]*)\b',
        r'\b(?P<number>\d+)\b',
        r'"(?P<string>[^\0\r\n"]*)"',
        r'{(?P<literal>\d+)\+?}',
        r'(?P<leftparen>\()',
        r'(?P<rightparen>\))',
        r'(?P<garbage>\S+)'
    )), flags=re.IGNORECASE)
    """Lexer pattern for :meth:`re.Pattern.finditer`."""

    # Strings may be 1024 octets long, but I limit the length to 1020 octets
    # to allow for errors (two octets for quotations marks, one for the
    # terminating null byte, one for other off-by-one errors).
    _isstr: Callable[..., Optional[re.Match]] = \
        re.compile(br'[^\0\r\n"]{0,1020}').fullmatch
    """Check whether bytes can be represented as ACAP string."""


#
# ManageSieve
#

class SieveConn(BaseACAPConn):
    """Low-level connection to a ManageSieve server.

    For example:

    >>> conn = SieveConn('imap.foo.example')
    >>> conn.authenticate('user', 'password')
    >>> with open('script.sieve', 'br') as file:
    >>>     conn.execute('putscript', file.name, file)
    >>> conn.execute('logout')

    .. warning::
        :class:`SieveConn` is not thread-safe.

    .. seealso::
        :rfc:`2244`
            Application Configuration Access Protocol
        :rfc:`2782`
            DNS SRV
        :rfc:`5804`
            ManageSieve
    """

    def __init__(self, *args, **kwargs):
        """Create a :class:`SieveConn` object.

        If `args` or `kwargs` are given, they are passed to :meth:`open`.
        Otherwise, no connection is established.

        For example:

        >>> with SieveConn('imap.host.example') as conn:
        >>>     conn.authenticate('user', 'password')
        >>>     ...

        >>> with SieveConn() as conn:
        >>>     conn.open('imap.host.example')
        >>>     conn.authenticate('user', 'password')
        >>>     ...

        Arguments:
            args: Positional arguments for :meth:`open`.
            kwargs: Keyword arguments for :meth:`open`.

        Raises:
            AppConnectionError: :attr:`sock` has died.
            SieveCapabilityError: "STARTTLS" not supported.
            SieveProtocolError: Server violated the ManageSieve protocol.
            TLSSecurityError: Server certificate has been revoked.
        """
        if args or kwargs:
            self.open(*args, **kwargs)

    def __del__(self):
        """Shut the connection down."""
        with suppress(OSError):
            self.shutdown()

    def authenticate(self, login: str, *auth, owner: str = '',
                     sasl: Union[AuthMech, Iterable[AuthMech]] = (),
                     logauth: bool = False, **kwauth):
        """Authenticate as `login`.

        How the user is authenticated depends on the type of SASL_ mechanisms
        given in `sasl` (e.g., password-based or the "EXTERNAL" mechanism).

        If no mechanisms are given, authentication is attempted with every
        supported non-obsolete password-based mechanism, starting with those
        with better security properties and progressing to those with worse
        security properties.

        Unrecognised arguments are passed on to SASL mechanism constructors.
        Password-based mechanisms require a password:

        >>> mgr.authenticate('user', 'password')

        By contrast, the "EXTERNAL" mechanism takes no arguments:

        >>> mgr.authenticate('user', sasl=ExternalAuth)

        If an `owner` is given, the scripts of that `owner` are managed,
        instead of those owned by `login`. This requires elevated privileges.

        Arguments:
            login: User to login as (authentication ID).
            owner: User whose scripts to manage (authorisation ID).
            sasl: SASL mechanisms (default: :meth:`BasePwdAuth.getmechs`).
            logauth: Log authentication exchange?
            auth: Positional arguments for SASL mechanism constructors.
            kwauth: Keyword arguments for SASL mechanism constructors.

        Raises:
            AppConnectionError: :attr:`sock` has died.
            AppOperationError: Another operation is already in progress.
            SASLCapabilityError: Authentication mechanisms exhausted.
            SASLProtocolError: Server violated the SASL protocol.
            SASLSecurityError: Server could not be verified.
            SieveConnectionError: Server has closed the connection.
            SieveOperationError: Authentication failed.
            SieveProtocolError: Server violated the ManageSieve protocol.
            ValueError: Bad characters in credentials.

        .. note::
            If an `owner` is given, but the selected authentication mechanism
            does not support proxy authentication, an error is logged to the
            console and authentication is attempted with the next mechanism.
        """
        kwauth['authzid'] = owner
        logger = self.logger
        self._auth = auth
        self._kwauth = kwauth
        self._logauth = logauth
        self._sasl = (BasePwdAuth.getmechs() if not sasl else
                      sasl if isinstance(sasl, Iterable) else
                      (sasl,))

        def authenticate():
            # pylint: disable=consider-using-with
            if not self.lock.acquire(blocking=False):
                raise AppOperationError(os.strerror(EINPROGRESS))
            if isinstance(self.file, LogIOWrapper) and not logauth:
                self.file.quiet = True
            try:
                for mech in self._sasl:
                    assert self.capabilities
                    if mech.name.casefold() in self.capabilities.sasl:
                        conn = SieveSASLAdapter(self)
                        try:
                            run = mech(conn, login, *auth, **kwauth)
                            if caps := run():
                                self.capabilities = caps
                        except SASLCapabilityError as err:
                            logger.error(err)
                            continue
                        except SieveOperationError as err:
                            # TRANSITION-NEEDED need not be treated specially.
                            if err.matches('AUTH-TOO-WEAK',
                                           'ENCRYPT-NEEDED',
                                           'TRANSITION-NEEDED'):
                                logger.error(err)
                                continue
                            raise
                        if authcid := run.authcid:
                            self.login = authcid
                            logger.info('Authenticated as %s using %s',
                                        authcid, mech.name.upper())
                        else:
                            # NOTREACHED
                            raise AppSoftwareError('forgot authentication ID')
                        if authzid := run.authzid:
                            self.owner = authzid
                            logger.info('Authorised as %s', authzid)
                        return
                raise SASLCapabilityError('SASL mechanisms exhausted')
            finally:
                if isinstance(self.file, LogIOWrapper):
                    self.file.quiet = False
                self.lock.release()
            # NOTREACHED

        self.isalive(check=True)
        self._withfollow(authenticate)

    def close(self):
        """Close the client side of the connection.

        .. warning::
            Call only when the server has closed the connection.
        """
        if self.file is not None:
            self.file.close()
            self.file = None
        if self.poll is not None:
            assert self.sock
            self.poll.unregister(self.sock)
            self.poll = None
        if self.sock is not None:
            self.sock.close()
            self.sock = None
        self._auth = ()
        self._kwauth = {}
        self.capabilities = None
        self.host = None
        self.port = None
        self.login = ''
        self.owner = ''

    def collect(self, check: bool = False) -> tuple['Response', list[Line]]:
        """Collect the server's response to the last command.

        For example:

        >>> conn.sendline(Atom('listscripts'))
        >>> conn.collect()
        (Response(response=Atom('OK'), code=(), message=None),
         [['foo.sieve', 'ACTIVE'], ['bar.sieve'], ['baz.sieve']])

        Arguments:
            check: Raise an error if the response is not "OK"?

        Raises:
            AppConnectionError: :attr:`sock` has died.
            SieveConnectionError: Server said "BYE". [#collect-check]_
            SieveOperationError: Server said "NO". [#collect-check]_
            SieveProtocolError: Server violated the ManageSieve protocol.

        .. [#collect-check] Only raised if `check` is `True`.
        """
        lines: list[Line] = []
        while True:
            try:
                line = self.receiveline()
            except ValueError as err:
                raise SieveProtocolError(str(err)) from err
            if line and isinstance(line[0], Atom):
                res = Response.fromline(line)
                if check and res.response != 'OK':
                    raise res.toerror()
                self.warning = res.message if res.matches('WARNINGS') else None
                return res, lines
            lines.append(line)
        # NOTREACHED

    def execute(self, command: str, *args: Union[IO, Word]) \
            -> tuple['Response', list[Line]]:
        """Execute `command` and return the server's response.

        For example:

        >>> conn.execute('listscripts')
        (Response(response=Atom('OK'), code=(), message=None),
         [['foo.sieve', 'ACTIVE'], ['bar.sieve'], ['baz.sieve']])

        Raises:
            AppConnectionError: :attr:`sock` has died.
            AppOperationError: Another operation is already in progress.
            SieveConnectionError: Server said "BYE".
            SieveOperationError: Server said "NO".
            SieveProtocolError: Server violated the ManageSieve protocol.

        .. note::
            Referrals are followed automatically.
        """
        def execute() -> tuple['Response', list[Line]]:
            # pylint: disable=consider-using-with
            if not self.lock.acquire(blocking=False):
                raise AppOperationError(os.strerror(EINPROGRESS))
            try:
                self.isalive(check=True)
                self.sendline(Atom(command.upper()), *args)
                res, data = self.collect()
            finally:
                self.lock.release()
            if res.response != 'OK':
                raise res.toerror()
            return res, data

        assert command
        return self._withfollow(execute)

    def geturl(self) -> Optional['URL']:
        """URL of the current connection.

        For example:

        >>> with SieveManager('imap.foo.example') as mgr:
        >>>     mgr.authenticate('user', 'password')
        >>>     mgr.geturl()
        'sieve://user@imap.foo.example'

        .. note::
            Only changes to the connection state effected by :meth:`open`,
            :meth:`close`, :meth:`shutdown`, :meth:`authenticate`,
            :meth:`unauthenticate`, and referrals are tracked.
        """
        if self.host:
            return URL(hostname=self.host,
                       port=self.port if self.port != 4190 else None,
                       username=self.login,
                       owner=self.owner)
        return None

    def isalive(self, check: bool = False) -> bool:
        """Check whether :attr:`sock` is alive.

        Arguments:
            check: Raise an error if :attr:`sock` has died.

        Raises:
            AppConnectionError: :attr:`sock` has died. [#isalive-check]_

        .. [#isalive-check] Only raised if `check` is `True`.
        """
        assert self.poll
        (_, events), = self.poll.poll()
        try:
            if events & select.POLLERR:
                raise AppConnectionError(ENOTCONN, 'socket error')
            if events & select.POLLHUP:
                raise AppConnectionError(ETIMEDOUT, os.strerror(ETIMEDOUT))
            if events & select.POLLNVAL:
                raise AppConnectionError(ENOTCONN, os.strerror(ENOTCONN))
        except AppConnectionError:
            if check:
                raise
        return True

    # pylint: disable=missing-raises-doc, redefined-outer-name
    def open(self, host: str, port: int = 4190,
             source: tuple[str, int] = ('', 0),
             timeout: Optional[float] = socket.getdefaulttimeout(),
             tls: bool = True, ocsp: bool = True):
        """Connect to `host` at `port`.

        Arguments:
            host: Server name or address.
            port: Server port.
            source: Source address and port.
            timeout: Timeout in seconds.
            tls: Secure the connection?
            ocsp: Check whether the server certificate was revoked?

        Raises:
            ConnectionError: Connection failed.
            SieveCapabilityError: "STARTTLS" not supported.
            SieveProtocolError: Server violated the ManageSieve protocol.
            TLSSecurityError: Server certificate has been revoked.
        """
        # pylint: disable=consider-using-with
        if not self.lock.acquire(blocking=False):
            raise AppOperationError(os.strerror(EINPROGRESS))
        try:
            self._connect(host, port, source, timeout)
            _, lines = self.collect(check=True)
            self._source = source
            self.capabilities = Capabilities.fromlines(lines)
            self.logger.info('Connected to %s:%d', host, port)
        finally:
            self.lock.release()
        if tls:
            self._starttls(ocsp=ocsp)

    def shutdown(self):
        """Shut the connection down.

        .. note::
            Use only when :meth:`logging out <logout>` would be unsafe.
        """
        if self.sock is not None:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.logger.info('Shut connection down')
        self.close()

    def _connect(self, host: str, port: int = 4190,
                 source: tuple[str, int] = ('', 0),
                 timeout: Optional[float] = socket.getdefaulttimeout()):
        """Connect to `host` at `port`.

        Arguments:
            host: Server address.
            port: Server port.
            source: Source address and port.
            timeout: Timeout in seconds.

        Raises:
            ConnectionError: Connection failed.
        """
        def connect(host: str):
            self.sock = socket.create_connection(
                (host, port),
                timeout=timeout, source_address=source
            )

        if self.sock or self.file:
            raise AppConnectionError(EISCONN, os.strerror(EISCONN))
        if isinetaddr(host):
            connect(host)
        else:
            try:
                # This is the algorithm specified by RFC 2782, NOT the one
                # specified by RFC 5804, sec. 1.8, which is wrong.
                records = list(resolvesrv(f'_sieve._tcp.{host}.'))
                for rec in records:
                    try:
                        connect(rec.host)
                    except OSError:
                        if rec == records[-1]:
                            raise
            except DNSError:
                connect(host)
        if not self.sock:
            raise AppConnectionError(ECONNABORTED, os.strerror(ECONNABORTED))
        file = self.sock.makefile('rwb')  # type: ignore[attr-defined]
        self.file = LogIOWrapper.wrap(file, self.logger)
        self.poll = select.poll()
        self.poll.register(self.sock)
        self.host = host
        self.port = port

    def _follow(self, url: str):
        """Close the connection, :meth:`open <open>` `url`, and reauthenticate.

        Raises:
            AppConnectionError: :attr:`sock` has died.
            SieveProtocolError: Server violated the ManageSieve protocol.
        """
        try:
            ref = URL.fromstr(url)
        except ValueError as err:
            raise SieveProtocolError(err) from err
        self.logger.info('Referred to %s', url)
        (oargs, okwargs), (auargs, aukwargs) = self._getstate()
        self.close()
        self.open(ref.hostname, ref.port or 4190, *oargs[2:], **okwargs)
        self.authenticate(*auargs, **aukwargs)

    def _getstate(self) -> Iterator[tuple[list, dict[str, Any]]]:
        """Get arguments to re-establish the current connection.

        For example:

        >>> mgr.geturl()
        sieve://user@imap.foo.example
        >>> (oargs, okwargs), (auth, kwauth) = mgr._getstate()
        >>> mgr.shutdown()
        >>> mgr.geturl()
        >>> mgr.open(*oargs, **okwargs)
        >>> mgr.authenticate(*auth, **kwauth)
        >>> mgr.geturl()
        sieve://user@imap.foo.example
        """
        for meth in (self.open, self.authenticate):
            args = []
            kwargs = {}
            signature = inspect.signature(meth)  # type: ignore[arg-type]
            for name, param in list(signature.parameters.items()):
                try:
                    value = getattr(self, name)
                except AttributeError:
                    value = getattr(self, f'_{name}')
                if param.kind in (Parameter.POSITIONAL_ONLY,
                                  Parameter.POSITIONAL_OR_KEYWORD):
                    args.append(value)
                elif param.kind == Parameter.VAR_POSITIONAL:
                    args.extend(value)
                elif param.kind == Parameter.KEYWORD_ONLY:
                    kwargs[name] = value
                elif param.kind == Parameter.VAR_KEYWORD:
                    kwargs.update(value)
            yield (args, kwargs)

    # pylint: disable=redefined-outer-name
    def _starttls(self, ocsp: bool = True):
        """Start TLS encryption.

        Arguments:
            ocsp: Check whether the server certificate was revoked?

        Raises:
            AppConnectionError: :attr:`sock` has died.
            AppOperationError: Another operation is already in progress.
            SieveCapabilityError: "STARTTLS" not supported.
            TLSSecurityError: Server certificate has been revoked.

        .. note::
            Called automatically by :meth:`open` unless `tls` is `False`.
        """
        assert self.sock
        assert self.capabilities
        if not self.capabilities.starttls:
            raise SieveCapabilityError('STARTTLS: not supported')
        self.execute('STARTTLS')
        # pylint: disable=consider-using-with
        if not self.lock.acquire(blocking=False):
            raise AppOperationError(os.strerror(EINPROGRESS))
        try:
            host = self.host
            self.sock = self.sslcontext.wrap_socket(
                self.sock,  # type: ignore[arg-type]
                server_hostname=host
            )
            file = self.sock.makefile('rwb')
            self.file = LogIOWrapper.wrap(file, self.logger)  # type: ignore
            _, lines = self.collect(check=True)
            self.capabilities = Capabilities.fromlines(lines)
            self.ocsp = ocsp
            proto = self.sock.version()
            cipher = self.sock.cipher()
            if proto and cipher:
                self.logger.info('Started %s using %s', proto, cipher[0])
            if ocsp:
                if HAVE_CRYPTOGRAPHY:
                    der = self.sock.getpeercert(binary_form=True)
                    if not der:
                        raise TLSSoftwareError('no peer certificate')
                    cert = x509.load_der_x509_certificate(der)
                    if certrevoked(cert, logger=self.logger):
                        raise TLSSecurityError(f'{host}: certificate revoked')
                else:
                    self.logger.error('Module "cryptography" not found')
        finally:
            self.lock.release()

    def _withfollow(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Call `func` and follow referrals.

        For example:

        >>> mgr._withfollow(mgr.execute, 'listscripts')

        Arguments:
            func: Function to call.
            args: Positional arguments for `func`.
            kwargs: Keyword arguments for `func`.

        Returns:
            The return value of `func`.

        Raises:
            AppConnectionError: :attr:`sock` has died.
            AppOperationError: Another operation is already in progress.
            SieveConnectionError: Server said "BYE".
            SieveOperationError: Server said "NO".
            SieveProtocolError: Server violated the ManageSieve protocol.

        .. seealso::
            :rfc:`5804` (sec. 1.3)
                ManageSieve "REFERRAL" response codes
        """
        while True:
            try:
                return func(*args, **kwargs)
            except SieveConnectionError as err:
                if err.matches('REFERRAL'):
                    try:
                        url = err.code[1]
                    except IndexError as exc:
                        raise SieveProtocolError('unexpected data') from exc
                    if isinstance(url, Atom) or not isinstance(url, str):
                        # pylint: disable=raise-missing-from
                        raise SieveProtocolError('expected string')
                    self._follow(url)
                    continue
                raise
        # NOTREACHED

    def _withreopen(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Call `func` and retry if the connection is closed.

        For example:

        >>> mgr._withreopen(mgr.execute, 'listscripts')

        Arguments:
            func: Function to call.
            args: Positional arguments for `func`.
            kwargs: Keyword arguments for `func`.

        Raises:
            AppConnectionError: :attr:`sock` has died.
            AppOperationError: Another operation is already in progress.
            SieveConnectionError: Server said "BYE".
            SieveOperationError: Server said "NO".
            SieveProtocolError: Server violated the ManageSieve protocol.

        Returns:
            The return value of `func`.
        """
        (oargs, okwargs), (auth, kwauth) = self._getstate()
        try:
            return func(*args, **kwargs)
        except (ConnectionError, TimeoutError, socket.herror, socket.gaierror):
            self.close()
            self.open(*oargs, **okwargs)
            self.authenticate(*auth, **kwauth)
            return func(*args, **kwargs)

    @property
    def timeout(self) -> Optional[float]:
        """Connection timeout in seconds.

        Set timeout to 500 ms:

        >>> mgr.timeout = 0.5

        .. note::
            The timeout can only be set while a connection is open.
        """
        if self.sock:
            return self.sock.gettimeout()
        return None

    @timeout.setter
    def timeout(self, secs: Optional[float]):
        if self.sock:
            self.sock.settimeout(secs)

    @property
    def tls(self) -> Optional[str]:     # type: ignore[override]
        """TLS version."""
        if isinstance(self.sock, ssl.SSLSocket):
            return self.sock.version()
        return None

    capabilities: Optional[Capabilities] = None
    """Server capabilities."""

    file: Optional[Union[IO, io.BufferedRWPair, LogIOWrapper]] = None
    """File-like access to :attr:`sock`."""

    host: Optional[str] = None
    """Remote address."""

    lock: threading.Lock = threading.Lock()
    """Operation lock."""

    logger: logging.Logger = logging.getLogger(__name__)
    """Logger to use.

    Messages are logged with the following priorities:

    ======================  =====================================
    Priority                Used for
    ======================  =====================================
    :const:`logging.ERROR`  Non-fatal errors
    :const:`logging.INFO`   State changes
    :const:`logging.DEBUG`  Data sent to/received from the server
    ======================  =====================================

    Suppress logging:

    >>> from logging import getLogger
    >>> getLogger('sievemgr').setLevel(logging.CRITICAL)

    Use a custom logger:

    >>> from logging import getLogger
    >>> mgr.logger = getLogger('foo').addHandler(logging.NullHandler())

    Print data send to/received from the server to standard error:

    >>> from logging import getLogger
    >>> getLogger('sievemgr').setLevel(logging.DEBUG)
    >>> mgr.listscripts()
    C: LISTSCRIPTS
    S: "foo.sieve" ACTIVE
    S: "bar.sieve"
    S: "baz.sieve"
    S: OK "Listscripts completed"
    (Response(response=Atom('OK'), code=(), message=None),
     [('foo.sieve', True), ('bar.sieve', False), ('baz.sieve', False)])
    """

    login: str = ''
    """Login name (authentication ID)."""

    ocsp: bool
    """Check whether the server certificate was revoked?"""

    owner: str = ''
    """User whose scripts are managed (authorisation ID)."""

    poll: Optional[select.poll] = None
    """Polling object for :attr:`sock`."""

    port: Optional[int] = None
    """Remote port."""

    sock: Optional[socket.SocketType] = None
    """Underlying socket."""

    sslcontext: ssl.SSLContext = ssl.create_default_context()
    """Settings for negotiating Transport Layer Security (TLS).

    Disable workarounds for broken X.509 certificates:

    >>> with SieveManager() as mgr:
    >>>     mgr.sslcontext.verify_flags |= ssl.VERIFY_X509_STRICT
    >>>     mgr.open('imap.foo.example')
    >>>     ...

    Load client certificate/key pair:

    >>> with SieveManager() as mgr:
    >>>     mgr.sslcontext.load_cert_chain(cert='cert.pem')
    >>>     mgr.open('imap.foo.example')
    >>>     ...

    Use a custom certificate authority:

    >>> with SieveManager() as mgr:
    >>>     mgr.sslcontext.load_verify_locations(cafile='ca.pem')
    >>>     mgr.open('imap.foo.example')
    >>>     ...
    """

    warning: Optional[str] = None
    """Warning issued in response to the last "CHECKSCRIPT" or "PUTSCRIPT".

    For example:

    >>> with open('script.sieve', 'br') as file:
    >>>     mgr.execute('putscript', file, 'script.sieve')
    (Response(response=Atom('OK'), code=('warnings,'),
     message='line 7: may need to be frobnicated'), [])
    >>> mgr.warning
    'line 7: may need to be frobnicated'

    .. note::
        Only set by :meth:`collect`, :meth:`execute`,
        :meth:`checkscript`, and :meth:`putscript`.

    .. seealso::
        :rfc:`5804` (sec. 1.3)
            ManageSieve "WARNINGS" response code.
    """

    _auth: tuple = ()
    """Positional arguments for SASL mechanism constructors."""

    _kwauth: dict[str, Any] = {}
    """Keyword arguments for SASL mechanism constructors."""

    _logauth: bool
    """Log the authentication exchange?"""

    _sasl: Iterable[AuthMech] = ()
    """SASL mechanisms."""

    _source: tuple[str, int] = ('', 0)
    """Source address and port."""


class SieveManager(SieveConn, contextlib.AbstractContextManager):
    """Connection to a ManageSieve server.

    For example:

    >>> with SieveManager('imap.foo.example') as mgr:
    >>>     mgr.authenticate('user', 'password')
    >>>     with open('sieve.script', 'br') as script:
    >>>         mgr.putscript(script, 'sieve.script')
    >>>     mgr.setactive('sieve.script')

    .. warning::
        :class:`SieveManager` is not thread-safe.
    """

    # pylint: disable=redefined-outer-name
    def __init__(self, *args, backup: int = 0,
                 memory: int = 524_288, **kwargs):
        """Create a :class:`SieveManager` object.

        If `args` or `kwargs` are given, they are passed to :meth:`open`.
        Otherwise, no connection is established.

        Arguments:
            backup: How many backups to keep by default.
            memory: See `max_size` in :class:`tempfile.SpooledTemporaryFile`.
            args: Positional arguments for :meth:`open`.
            kwargs: Keyword arguments for :meth:`open`.

        Raises:
            AppConnectionError: :attr:`sock` has died.
            SieveCapabilityError: "STARTTLS" not supported.
            SieveProtocolError: Server violated the ManageSieve protocol.
            TLSSecurityError: Server certificate has been revoked.
        """
        super().__init__(*args, **kwargs)
        self.backup: int = backup
        self.memory: int = memory

    def __exit__(self, _exctype, excvalue, _traceback):
        """Exit the context and close the connection appropriately."""
        if isinstance(excvalue, (ConnectionError, TimeoutError)):
            self.close()
        elif isinstance(excvalue, ProtocolError):
            self.shutdown()
        else:
            try:
                self.logout()
            except AppOperationError:
                try:
                    self.shutdown()
                except OSError:
                    self.close()

    def backupscript(self, script: str, keep: int = 1):
        """Make an Emacs-style backup of `script`.

        `keep` = 0
            Do nothing.

        `keep` = 1
            :file:`script` is backed up as :file:`script~`.

        `keep` > 1
            :file:`script` is backed up as :file:`script.~{n}~`.
            `n` starts with 1 and increments with each backup.
            Old backups are deleted if there are more than `keep` backups.

        For example:

        >>> mgr.listscripts()
        [('script.sieve', True)]
        >>> mgr.backupscript('script.sieve', keep=0)
        >>> mgr.listscripts()
        [('script.sieve', True)]

        >>> mgr.listscripts()
        [('script.sieve', True)]
        >>> mgr.backupscript('script.sieve', keep=1)
        >>> mgr.listscripts()
        [('script.sieve', True), ('script.sieve~', False)]

        >>> mgr.listscripts()
        [('script.sieve', True)]
        >>> mgr.backupscript('script.sieve', keep=2)
        >>> mgr.listscripts()
        [('script.sieve', True), ('script.sieve.~1~', False)]
        >>> mgr.backupscript('script.sieve', keep=2)
        >>> mgr.listscripts()
        [('script.sieve', True),
         ('script.sieve.~1~', False),
         ('script.sieve.~2~', False)]
        >>> mgr.backupscript('script.sieve', keep=2)
        >>> mgr.listscripts()
        [('script.sieve', True),
         ('script.sieve.~2~', False),
         ('script.sieve.~3~', False)]

        Arguments:
            script: Script name.
            keep: How many backups to keep.

        Raises:
            AppConnectionError: :attr:`sock` has died.
            AppOperationError: Another operation is already in progress.
            SieveConnectionError: Server has closed the connection.
            SieveProtocolError: Server violated the ManageSieve protocol.
        """
        def getfiles() -> Iterator[str]:
            for script, _ in self.listscripts():
                yield script

        def copy(src: str, targ: str):
            self.copyscript(src, targ, backup=0)

        backup(script, keep, getfiles, copy, self.deletescript)

    def checkscript(self, script: Union[str, IO]):
        """Check whether `script` is valid.

        Syntax errors trigger a :exc:`SieveOperationError`.
        Semantic errors are reported in :attr:`warning`.

        For example:

        >>> checkscript('foo')
        Traceback (most recent call last):
            [...]
        SieveOperationError: line 1: error: expected end of command ';'
        error: parse failed.

        >>> checkscript('# foo')
        >>>

        Arguments:
            script: Script (*not* script name).

        Raises:
            AppConnectionError: :attr:`sock` has died.
            AppOperationError: Another operation is already in progress.
            SieveCapabilityError: "CHECKSCRIPT" not supported.
            SieveConnectionError: Server has closed the connection.
            SieveOperationError: `Script` contains syntax errors.
            SieveProtocolError: Server violated the ManageSieve protocol.

        .. important::
            Sieve scripts must be encoded in UTF-8.
        """
        assert self.capabilities
        if not self.capabilities.version:
            raise SieveCapabilityError('CHECKSCRIPT: not supported')
        self.execute('CHECKSCRIPT', script)

    def copyscript(self, source: str, target: str,
                   backup: Optional[int] = None):
        """Download `source` and re-upload it as `target`.

        Arguments:
            source: Source name.
            target: Target name.
            backup: How many backups to keep (default: :attr:`backup`).

        Raises:
            AppConnectionError: :attr:`sock` has died.
            AppOperationError: Another operation is already in progress.
            SieveConnectionError: Server has closed the connection.
            SieveProtocolError: Server violated the ManageSieve protocol.
        """
        with SpooledTemporaryFile(max_size=self.memory, mode='bw+') as temp:
            temp.write(self.getscript(source).encode('utf8'))
            temp.seek(0)
            self.putscript(temp, target, backup=backup)

    def deletescript(self, script: str):
        """Delete `script`.

        Raises:
            AppConnectionError: :attr:`sock` has died.
            AppOperationError: Another operation is already in progress.
            SieveConnectionError: Server has closed the connection.
            SieveProtocolError: Server violated the ManageSieve protocol.
        """
        self._scripts = None
        self.validname(script, check=True)
        self.execute('DELETESCRIPT', script)
        self.logger.info('Removed %s', script)

    def editscripts(self, command: list[str], scripts: list[str], *args,
                    catch: Optional[Callable[[Exception, str], bool]] = None,
                    check: bool = True, create: bool = True,
                    **kwargs) -> subprocess.CompletedProcess:
        """Download `scripts`, edit them with `command`, and re-upload them.

        The `scripts` are appended to the `command`, which is then passed
        to :func:`subprocess.run`. Scripts that have been changed are then
        re-uploaded to the server. If the server has closed the connection
        in the meantime, the connection is re-established automatically.

        If :meth:`putscript` raises an error and `catch` has been given,
        then the error and the name of the offending script are passed to
        `catch`, which should return `True` if the `command` should be
        re-invoked for that script and `False` otherwise. Either way,
        the error will be suppressed.

        For example:

        >>> mgr.editscripts(['vi'], ['foo.sieve'])

        >>> cp = mgr.editscripts(['cmp'], ['a.sieve', 'b.sieve'], check=False)
        >>> if cp.returncode != 0:
        >>>     print('a.sieve and b.sieve differ')

        Arguments:
            command: Command to run.
            scripts: Scripts to edit.
            catch: Error handler.
            check: See :func:`subprocess.run`.
            create: Create scripts that do not exist?
            args: Positional arguments for :func:`subprocess.run`.
            kwargs: Keywords arguments for :func:`subprocess.run`.

        Raises:
            AppConnectionError: :attr:`sock` has died.
            AppOperationError: Another operation is already in progress.
            SieveConnectionError: Server has closed the connection.
            SieveOperationError: At least one script contains a syntax error.
                [#editscripts-catch]_
            SieveProtocolError: Server violated the ManageSieve protocol.
            ValueError: Script name contains path separator.

        .. [#editscripts-catch] Only raised if `catch` has *not* been given.
        """
        for script in scripts:
            self.validname(script, check=True)
            if path.sep in script:
                raise ValueError(f'{script}: contains {path.sep}')
        with TemporaryDirectory() as tmpdir:
            fnames = []
            ctimes = []
            for script in scripts:
                fname = path.join(tmpdir, script)
                with open(fname, 'w', encoding='utf8') as file:
                    try:
                        file.write(self.getscript(script))
                    except SieveOperationError as err:
                        if not create:
                            raise
                        if not err.code:
                            if self.scriptexists(script):
                                raise
                        elif not err.matches('NONEXISTENT'):
                            raise
                fnames.append(fname)
                ctimes.append(os.stat(fname).st_ctime)
            while True:
                cp = subprocess.run(command + fnames, *args,
                                    check=check, **kwargs)
                retry: list[tuple[str, str, float]] = []
                for script, fname, ctime in zip(scripts, fnames, ctimes):
                    if os.stat(fname).st_ctime > ctime:
                        with open(fname, 'rb') as file:
                            try:
                                self._withreopen(self.putscript, file, script)
                            except SieveOperationError as err:
                                if catch is None:
                                    raise
                                if catch(err, script):
                                    retry.append((script, fname, ctime))
                if not retry:
                    return cp
                scripts, fnames, ctimes = map(list, zip(*retry))
        # NOTREACHED

    def getactive(self) -> Optional[str]:
        """Get the name of the active script.

        Raises:
            AppConnectionError: :attr:`sock` has died.
            AppOperationError: Another operation is already in progress.
            SieveConnectionError: Server has closed the connection.
            SieveProtocolError: Server violated the ManageSieve protocol.
        """
        for name, active in self.listscripts():
            if active:
                return name
        return None

    def getscript(self, script: str) -> str:
        """Download `script`.

        For example:

        >>> with open('foo.sieve', 'w', encoding='utf8') as file:
        >>>     file.write(mgr.getscript('foo.sieve'))

        Arguments:
            script: Script name.

        Raises:
            AppConnectionError: :attr:`sock` has died.
            AppOperationError: Another operation is already in progress.
            SieveConnectionError: Server has closed the connection.
            SieveProtocolError: Server violated the ManageSieve protocol.
        """
        self.validname(script, check=True)
        try:
            # pylint: disable=unbalanced-tuple-unpacking
            _, ((content,),) = self.execute('GETSCRIPT', script)
        except ValueError as err:
            raise SieveProtocolError('unexpected data') from err
        if isinstance(content, Atom):
            raise SieveProtocolError('unexpected atom')
        if isinstance(content, str):
            return content
        raise SieveProtocolError('unexpected ' + type(content).__name__)

    def havespace(self, script: str, size: int):
        """Check whether there is enough space for `script`.

        Arguments:
            script: Script name.
            size: Script size in bytes.

        Raises:
            AppConnectionError: :attr:`sock` has died.
            AppOperationError: Another operation is already in progress.
            SieveConnectionError: Server has closed the connection.
            SieveOperationError: There is *not* enough space.
            SieveProtocolError: Server violated the ManageSieve protocol.
        """
        self.validname(script, check=True)
        self.execute('HAVESPACE', script, size)

    def listscripts(self, cached: bool = False) -> list[tuple[str, bool]]:
        """List scripts and whether they are the active script.

        For example:

        >>> mgr.listscripts()
        [('foo.sieve', False), ('bar.sieve', True)]

        >>> scripts = [script for script, _ in mgr.listscripts()]

        Arguments:
            cached: Return cached response? [#cached]_

        Returns:
            A list of script name/status tuples.

        Raises:
            AppConnectionError: :attr:`sock` has died.
            AppOperationError: Another operation is already in progress.
            SieveConnectionError: Server has closed the connection.
            SieveProtocolError: Server violated the ManageSieve protocol.

        .. [#cached] The cache is cleared after :meth:`copyscript`,
                     :meth:`deletescript`, :meth:`putscript`,
                     :meth:`renamescript`, :meth:`setactive`, and
                     :meth:`unsetactive`.
        """
        if not cached or self._scripts is None:
            self._scripts = []
            for line in self.execute('LISTSCRIPTS')[1]:
                try:
                    name = line[0]
                except IndexError as err:
                    raise SieveProtocolError('no data') from err
                if not isinstance(name, str):
                    raise SieveProtocolError('expected string')
                try:
                    status = line[1]
                    if not isinstance(status, str):
                        raise SieveProtocolError('expected string')
                    active = status.casefold() == 'active'
                except IndexError:
                    active = False
                self._scripts.append((name, active))
        return self._scripts

    def logout(self):
        """Log out.

        .. note::
            :meth:`logout` should be called to close the connection
            unless :class:`SieveManager` is used as a context manager.

        .. warning::
            Logging out is unsafe after a :exc:`ProtocolError`.
            Use :meth:`shutdown` instead.
        """
        if self.sock is not None:
            try:
                self.execute('LOGOUT')
                self.logger.info('Logged out')
            except (OperationError, ProtocolError):
                with suppress(OSError):
                    self.shutdown()
            except ConnectionError:
                pass
        self.close()

    def noop(self, tag: Optional[str] = None) -> Optional[str]:
        """Request a no-op.

        For example:

        >>> mgr.noop('foo')
        'foo'

        Arguments:
            tag: String for the server to echo back.

        Returns:
            Server echo.

        Raises:
            AppConnectionError: :attr:`sock` has died.
            AppOperationError: Another operation is already in progress.
            SieveCapabilityError: "NOOP" not supported.
            SieveConnectionError: Server has closed the connection.
            SieveProtocolError: Server violated the ManageSieve protocol.
        """
        assert self.capabilities
        if not self.capabilities.version:
            raise SieveCapabilityError('NOOP: not supported')
        args = () if tag is None else (tag,)
        res, _ = self.execute('NOOP', *args)
        try:
            data = res.code[1]
        except IndexError:
            return None
        if isinstance(data, Atom) or not isinstance(data, str):
            raise SieveProtocolError('expected string')
        return data

    def putscript(self, source: Union[str, IO], target: str,
                  backup: Optional[int] = None):
        """Upload `source` to the server as `target`.

        The server should reject syntactically invalid scripts.
        It may issue a :attr:`warning` for semantically invalid scripts,
        but should accept them nonetheless. Updates are atomic.

        For example:

        >>> mgr.putscript('# empty', 'foo.sieve')

        >>> with open('foo.sieve', 'br') as file:
        >>>     mgr.putscript(file, 'foo.sieve')

        Arguments:
            source: Script (*not* script name).
            target: Script name.
            backup: How many backups to keep (default: :attr:`backup`).

        Raises:
            AppConnectionError: :attr:`sock` has died.
            AppOperationError: Another operation is already in progress.
            SieveConnectionError: Server has closed the connection.
            SieveOperationError: `Script` contains syntax errors.
            SieveProtocolError: Server violated the ManageSieve protocol.

        .. important::
            Sieve scripts must be encoded in UTF-8.
        """
        self.validname(target, check=True)
        try:
            keep = self.backup if backup is None else backup
            self.backupscript(target, keep=keep)
        except SieveOperationError as err:
            if not err.code:
                for script, _ in self.listscripts():
                    if script == target:
                        raise
            elif not err.matches('NONEXISTENT'):
                raise
        self._scripts = None
        self.execute('PUTSCRIPT', target, source)
        self.logger.info('Uploaded %s', target)

    def renamescript(self, source: str, target: str, emulate: bool = True):
        """Rename `source` to `target`.

        Some servers do not the support the "RENAMESCRIPT" command.
        On such servers, renaming is emulated by downloading `source`,
        re-uploading it as `target`, marking `target` as the active script
        if `source` is the active script, and then deleting `source`.

        For example:

        >>> mgr.renamescript('foo.sieve', 'bar.sieve', emulate=False)

        Arguments:
            source: Script name.
            target: Script name.
            emulate: Emulate "RENAMESCRIPT" if the server does not support it?

        Raises:
            SieveCapabilityError: "RENAMESCRIPT" not supported. [#emulate]_
            SieveOperationError: `source` does not exist or `target` exists.

        .. [#emulate] Only raised if `emulate` is `False`.
        """
        assert self.capabilities
        self.validname(source, check=True)
        self.validname(target, check=True)
        if self.capabilities.version:
            self._scripts = None
            self.execute('RENAMESCRIPT', source, target)
            self.logger.info('Renamed %s to %s', source, target)
        elif emulate:
            sourceactive: Optional[bool] = None
            for script, active in self.listscripts():
                if script == source:
                    sourceactive = active
                if script == target:
                    raise SieveOperationError(
                        code=(Atom('alreadyexists'),),
                        message=f'{target}: {os.strerror(EEXIST)}'
                    )
            if sourceactive is None:
                raise SieveOperationError(
                    code=(Atom('nonexistent'),),
                    message=f'{source}: {os.strerror(ENOENT)}'
                )
            self.copyscript(source, target, backup=0)
            if sourceactive:
                self.setactive(target)
            self.deletescript(source)
        else:
            raise SieveCapabilityError('RENAMESCRIPT: not supported')

    def scriptexists(self, script: str, cached: bool = False) -> bool:
        """Check if `script` exists.

        Arguments:
            script: Script name.
            cached: Return cached response? [#cached]_

        Raises:
            AppConnectionError: :attr:`sock` has died.
            AppOperationError: Another operation is already in progress.
            SieveConnectionError: Server has closed the connection.
            SieveProtocolError: Server violated the ManageSieve protocol.
        """
        self.validname(script, check=True)
        return any(s == script for s, _ in self.listscripts(cached=cached))

    def setactive(self, script: str):
        """Mark `script` as the active script.

        Raises:
            AppConnectionError: :attr:`sock` has died.
            AppOperationError: Another operation is already in progress.
            SieveConnectionError: Server has closed the connection.
            SieveProtocolError: Server violated the ManageSieve protocol.
        """
        self.validname(script, check=True)
        self._scripts = None
        self.execute('SETACTIVE', script)
        self.logger.info('Activated %s', script)

    def unauthenticate(self):
        """Unauthenticate.

        Raises:
            AppConnectionError: :attr:`sock` has died.
            AppOperationError: Another operation is already in progress.
            SieveCapabilityError: "UNAUTHENTICATE" not supported.
            SieveConnectionError: Server has closed the connection.
            SieveProtocolError: Server violated the ManageSieve protocol.
        """
        assert self.capabilities
        if not self.capabilities.unauthenticate:
            raise SieveCapabilityError('UNAUTHENTICATE: not supported')
        self.execute('UNAUTHENTICATE')
        self.login = ''
        self.owner = ''
        self.logger.info('Un-authenticated')

    def unsetactive(self):
        """Deactivate the active script.

        Raises:
            AppConnectionError: :attr:`sock` has died.
            AppOperationError: Another operation is already in progress.
            SieveConnectionError: Server has closed the connection.
            SieveProtocolError: Server violated the ManageSieve protocol.
        """
        self._scripts = None
        self.execute('SETACTIVE', '')
        self.logger.info('Deactivated active script')

    @classmethod
    def validname(cls, script: str, check: bool = False) -> bool:
        """Check whether `script` is a valid script name.

        Arguments:
            script: Script name
            check: Raise an error if `script` is not a valid script name?

        Raises:
            ValueError: `script` is *not* valid. [#validname-check]_

        .. [#validname-check] Only raised if `check` is `True`.
        """
        if cls._isname(script):
            return True
        if check:
            raise ValueError(escapectrl(script) + ': bad name')
        return False

    backup: int = 0
    """How many backups to keep."""

    _isname: Callable[..., Optional[re.Match]] = re.compile(
            '[^\u0000-\u001f\u0080-\u009f\u2028\u2029]+'
    ).fullmatch
    """Check whether a string is a valid script name.

    .. seealso::
        :rfc:`5198` (sec. 2)
            Definition of unicode format for network interchange.
        :rfc:`5804` (sec. 1.6)
            ManageSieve script names.
    """

    _scripts: Optional[list[tuple[str, bool]]] = None
    """Scripts returned by the last :meth:`listscripts`."""


class SieveSASLAdapter(AbstractSASLAdapter):
    """Adapter to send SASL messages over a :class:`SieveConn`."""

    def __init__(self, connection: 'SieveConn'):
        """Initialise the adapter."""
        self.conn = connection

    def abort(self):
        self.send(b'*')
        self.end()

    def begin(self, name: str, data: Optional[bytes] = None):
        assert self.conn
        args: list[Any] = [Atom('AUTHENTICATE'), name.upper()]
        if data is not None:
            args.append(b64encode(data))
        self.conn.sendline(*args)   # type: ignore[arg-type]

    def end(self):
        assert self.conn
        try:
            res = Response.fromline(self.conn.receiveline())
        except ValueError as err:
            raise SieveProtocolError(str(err)) from err
        if res.response != 'OK':
            raise res.toerror()

    def send(self, data: bytes):
        assert self.conn
        conn = self.conn
        conn.sendline(b64encode(data))  # type: ignore[arg-type]

    def receive(self) -> bytes:
        assert self.conn
        try:
            line = self.conn.receiveline()
        except ValueError as err:
            raise SieveProtocolError(str(err)) from err
        if isinstance(line[0], Atom):
            res = Response.fromline(line)
            raise res.toerror()
        try:
            word, = line
        except ValueError as err:
            raise SieveProtocolError('unexpected data') from err
        if isinstance(word, Atom) or not isinstance(word, str):
            raise SieveProtocolError('expected string')
        return b64decode(word)

    @property
    def sock(self) -> Union[socket.SocketType, ssl.SSLSocket]:
        assert self.conn
        assert self.conn.sock
        return self.conn.sock

    @sock.setter
    def sock(self, sock: Union[socket.SocketType, ssl.SSLSocket]):
        assert self.conn
        self.conn.sock = sock

    conn: Optional[SieveConn] = None
    """Underlying connection."""


CapabilitiesT = TypeVar('CapabilitiesT', bound='Capabilities')
""":class:`Capabilities` type variable."""


@dataclass
class Capabilities():
    """Server capabilities."""

    @classmethod
    def fromlines(cls: type[CapabilitiesT],
                  lines: Iterable[Line]) -> CapabilitiesT:
        """Create a :class:`Capabilities` object from a server response."""
        def getvalue(words: Line) -> str:
            try:
                value, = words[1:]
            except ValueError as err:
                raise SieveProtocolError('expected word') from err
            if not isinstance(value, str):
                raise SieveProtocolError('expected string')
            return value

        obj = cls()
        for words in lines:
            try:
                key = words[0].casefold()   # type: ignore[union-attr]
            except IndexError as err:
                raise SieveProtocolError('expected word') from err
            except AttributeError as err:
                raise SieveProtocolError('expected string') from err
            if key in ('implementation', 'language', 'owner', 'version'):
                setattr(obj, key, getvalue(words))
            elif key in ('notify', 'sasl', 'sieve'):
                setattr(obj, key, tuple(getvalue(words).casefold().split()))
            elif key == 'maxredirects':
                setattr(obj, key, int(getvalue(words)))
            elif key in ('starttls', 'unauthenticate'):
                setattr(obj, key, True)
            else:
                try:
                    obj.notunderstood[key] = words[1]
                except IndexError:
                    obj.notunderstood[key] = True
        return obj

    implementation: Optional[str] = None
    """Server application."""

    sieve: tuple[str, ...] = ()
    """Supported Sieve modules."""

    language: Optional[str] = None
    """Language."""

    maxredirects: Optional[int] = None
    """Maximum number of redirect operations permitted in a script."""

    notify: tuple[str, ...] = ()
    """URI schema parts for supported notification methods."""

    owner: str = ''
    """Canonical name of the user whose scripts are managed."""

    sasl: tuple[str, ...] = ()
    """Supported authentication methods."""

    starttls: bool = False
    """Is "STARTTLS" available?"""

    unauthenticate: bool = False
    """Is "UNAUTHENTICATE" available?"""

    version: Optional[str] = None
    """ManageSieve protocol version."""

    notunderstood: dict = dataclasses.field(default_factory=dict)
    """Capabilities not understood by SieveManager."""


ResponseT = TypeVar('ResponseT', bound='Response')
"""Type variable for :class:`Response`."""


@dataclass(frozen=True)
class Response():
    """Server response to a command.

    .. seealso::
        :rfc:`5804` (secs. 1.2, 1.3, 4, 6.4, and passim)
            ManageSieve responses
    """

    @classmethod
    def fromline(cls: type[ResponseT], line: Line) -> ResponseT:
        """Create a :class:`Response` object from a :class:`Line`."""
        # pylint: disable=redefined-outer-name
        code = cls.code
        message = cls.message
        response = None
        for i, word in enumerate(line):
            if isinstance(word, Atom):
                if i == 0:
                    response = word
                    continue
            elif isinstance(word, str):
                if 1 <= i <= 2:
                    message = word
                    continue
            elif isinstance(word, Sequence):
                if i == 1:
                    code = tuple(word)
                    continue
            raise SieveProtocolError('malformed response')
        if response is None:
            raise SieveProtocolError('expected atom')
        return cls(response=response, code=code, message=message)

    def __str__(self) -> str:
        """:attr:`message` or, if no message was returned, a stub message."""
        return self.message if self.message else f'server says {self.response}'

    def matches(self, *categories: str) -> bool:
        """Check if :attr:`code` matches any of the given `categories`.

        Returns `False` if :attr:`code` is empty.
        Matching is case-insensitive.

        For example:

        >>> with open('script.sieve') as script:
        >>>     try:
        >>>         mgr.putscript(script, script.name)
        >>>     except SieveOperationError as err:
        >>>         if err.matches('QUOTA'):
        >>>             print('over quota')

        Print more informative messages:

        >>> with open('script.sieve') as script:
        >>>     try:
        >>>         mgr.putscript(script, script.name)
        >>>     except SieveOperationError as err:
        >>>         if err.matches('QUOTA/MAXSCRIPTS'):
        >>>             print('too many scripts')
        >>>         elif err.matches('QUOTA/MAXSIZE'):
        >>>             print(f'{script.name} is too large')
        >>>         elif err.matches('QUOTA'):
        >>>             print('over quota')
        """
        try:
            rescode = self.code[0]
        except IndexError:
            return False
        assert isinstance(rescode, str)
        for cat in categories:
            pattern = re.escape(cat.removesuffix('/')) + r'(/|$)'
            if re.match(pattern, rescode, flags=re.IGNORECASE):
                return True
        return False

    def toerror(self) -> 'SieveError':
        """Convert a :class:`Response` into an error."""
        cls = (SieveConnectionError if self.response == 'BYE' else
               SieveOperationError)
        return cls(self.response, self.code, self.message)

    response: Atom
    """'OK', 'NO', or 'BYE'.

    ========  ===========================
    Response   Meaning
    ========  ===========================
    'OK'      Success
    'NO'      Failure
    'BYE'     Connection closed by server
    ========  ===========================
    """

    code: tuple[Word, ...] = ()
    """Response code.

    ManageSieve response codes are lists of categories, separated by
    slashes ("/"), where each category is the super-category of the
    next (e.g., "quota/maxsize").

    Some response codes carry data (e.g., ``TAG "SYNC-123"``).

    See :rfc:`5804` (sec. 1.3) for a list of response codes.

    .. warning::
        Servers need *not* return response codes.
    """

    message: Optional[str] = None
    """Human-readable message.

    .. warning::
        Servers need *not* return a message.
    """


@dataclass(frozen=True)
class SRV():
    """DNS SRV record.

    .. seealso::
        :rfc:`2782`
            DNS SRV
    """

    priority: int
    weight: int
    host: str
    port: int


URLT = TypeVar('URLT', bound='URL')
"""Type variable for :class:`URL`."""


@dataclass(frozen=True)
class URL():
    """Sieve URL.

    .. seealso::
        :rfc:`5804` (sec. 3)
            Sieve URL Scheme
    """

    @classmethod
    def fromstr(cls: type[URLT], url: str) -> URLT:
        """Create a :class:`URL` object from a URL string.

        For example:

        >>> URL.fromstr('sieve://user@imap.foo.example')
        URL(hostname='imap.foo.example', scheme='sieve',
            username='user', password=None, port=None,
            owner=None, scriptname=None)

        Raises:
            ValueError: Not a valid Sieve URL.
        """
        if not re.match(r'([a-z][a-z0-9+.-]*:)?//', url):
            url = 'sieve://' + url
        parts = urllib.parse.urlsplit(url)
        if parts.query or parts.fragment:
            raise ValueError(f'{url}: not a Sieve URL')
        if not parts.hostname:
            raise ValueError(f'{url}: no host')
        if not (isinetaddr(parts.hostname) or ishostname(parts.hostname)):
            raise ValueError(f'{parts.hostname}: neither address nor hostname')
        try:
            owner, scriptname = parts.path.split('/', maxsplit=2)[1:]
        except ValueError:
            owner, scriptname = parts.path[1:], None
        return cls(
            scheme=parts.scheme,
            username=parts.username,
            password=parts.password,
            hostname=parts.hostname,
            port=parts.port,
            owner=owner if owner else None,
            scriptname=scriptname if scriptname else None
        )

    def __str__(self):
        """Get a string representation of the URL."""
        url = ''
        if self.scheme:
            url += f'{self.scheme}://'
        else:
            url += 'sieve://'
        if self.username:
            url += self.username
            if self.password is not None:
                url += f':{self.password}'
            url += '@'
        if self.hostname:
            url += self.hostname
        else:
            url += 'localhost'
        if self.port is not None:
            url += f':{self.port}'
        if self.owner:
            url += f'/{self.owner}'
        if self.scriptname:
            url += f'/{self.scriptname}'
        return url

    hostname: str
    scheme: str = 'sieve'
    username: Optional[str] = None
    password: Optional[str] = None
    port: Optional[int] = None
    owner: Optional[str] = None
    scriptname: Optional[str] = None


#
# Authentication
#

class BaseAuth(AbstractAuth, ABC):
    """Base class for authentication mechanisms.

    :class:`BaseAuth` provides methods to prepare strings
    according to :rfc:`3454` and :rfc:`4013` and a layer over
    the underlying :class:`AbstractSASLAdapter` object that
    calls :meth:`AbstractSASLAdapter.begin` and
    :meth:`AbstractSASLAdapter.end` transparently.

    Credentials must be prepared in :meth:`__init__`. Subclasses
    should pass `connection`, `authcid`, `authzid`, and `prepare`
    to :code:`super().__init__` and use :meth:`prepare` to prepare
    the remaining credentials. For example:

    .. literalinclude:: ../sievemgr.py
        :pyobject: BasePwdAuth.__init__
        :dedent: 4

    The SASL exchange must be implemented in :meth:`exchange`.
    Subclasses should use :meth:`send` and :meth:`receive` to
    exchange SASL messages. For example:

    .. literalinclude:: ../sievemgr.py
        :pyobject: PlainAuth.exchange
        :dedent: 4
    """

    @staticmethod
    # pylint: disable=redefined-outer-name (string)
    def prepare(string: str) -> str:
        """Prepare `string` according to :rfc:`3454` and :rfc:`4013`.

        Returns:
            Prepared `string`.

        Raises:
            ValueError: `String` is malformed.
        """
        if any(rlcat := list(map(stringprep.in_table_d1, string))):
            if not (rlcat[0] and rlcat[-1]):
                raise ValueError(f'{string}: malformed RandLCat string')
            if any(map(stringprep.in_table_d2, string)):
                raise ValueError(f'{string}: mixes RandLCat and LCat')
        prep = ''
        for i, char in enumerate(string, start=1):
            if stringprep.in_table_b1(char):
                pass
            elif stringprep.in_table_c12(char):
                prep += ' '
            elif stringprep.in_table_c21_c22(char):
                raise ValueError(f'{string}:{i}: control character')
            elif stringprep.in_table_c3(char):
                raise ValueError(f'{string}:{i}: private use character')
            elif stringprep.in_table_c4(char):
                raise ValueError(f'{string}:{i}: non-character code point')
            elif stringprep.in_table_c5(char):
                raise ValueError(f'{string}:{i}: surrogate code point')
            elif stringprep.in_table_c6(char):
                raise ValueError(f'{string}:{i}: not plain text')
            elif stringprep.in_table_c7(char):
                raise ValueError(f'{string}:{i}: not canonical')
            elif stringprep.in_table_c8(char):
                raise ValueError(f'{string}:{i}: changes display/deprecated')
            elif stringprep.in_table_c9(char):
                raise ValueError(f'{string}:{i}: tagging character')
            elif stringprep.in_table_a1(char):
                raise ValueError(f'{string}:{i}: unassigned code point')
            else:
                prep += char
        return unicodedata.ucd_3_2_0.normalize('NFKC', prep)

    def __init__(self, adapter: AbstractSASLAdapter,
                 authcid: str, authzid: str = '',
                 prepare: SASLPrep = SASLPrep.ALL):
        """Prepare authentication.

        `authcid` and `authzid` are prepared according to :rfc:`3454` and
        :rfc:`4013` if ``prepare & SASLPrep.USERNAMES`` evaluates as true.

        Arguments:
            conn: Connection over which to authenticate.
            authcid: Authentication ID (user to login as).
            authzid: Authorisation ID (user whose rights to acquire).
            prepare: Which credentials to prepare.

        Raises:
            ValueError: Bad characters in username.
        """
        prepare &= SASLPrep.USERNAMES   # type: ignore[assignment]
        self.adapter = adapter
        self.authcid = self.prepare(authcid) if prepare else authcid
        self.authzid = self.prepare(authzid) if prepare else authzid

    # pylint: disable=useless-return
    def __call__(self) -> Optional[Any]:
        """Authenticate as :attr:`authcid`.

        :attr:`authcid` is authorised as :attr:`authzid`
        if :attr:`authzid` is set (proxy authentication).

        Returns:
            Data returned by the server, if any.

        Raises:
            ConnectionError: Server has closed the connection.
            OperationError: Authentication failed.
            SASLCapabilityError: Some feature is not supported.
            SASLProtocolError: Server violated the SASL protocol.
            SASLSecurityError: Server verification failed.
            TLSCapabilityError: Channel-binding is not supported.

        .. note::
            Calls :meth:`exchange` and :meth:`end`.
        """
        self.exchange()
        if self.state == AuthState.RECEIVED:
            self.send(b'')
        self.end()
        return None

    def abort(self):
        """Abort authentication.

        Raises:
            ProtocolError: Protocol violation.
        """
        self.adapter.abort()
        self.state = AuthState.DONE

    def begin(self, data: Optional[bytes] = None):
        """Begin authentication.

        Arguments:
            data: Optional client-first message.

        Raises:
            ConnectionError: Connection was closed.
            ProtocolError: Protocol violation.
        """
        if self.state == AuthState.PREAUTH:
            self.adapter.begin(self.name, data)
            self.state = AuthState.SENT
        else:
            raise SASLProtocolError(f'SASL state {self.state}: unexpected')

    def end(self):
        """Conclude authentication.

        Raises:
            ConnectionError: Connection was closed.
            OperationError: Authentication failed.
            ProtocolError: Protocol violation.
        """
        if self.state == AuthState.SENT:
            self.adapter.end()
        else:
            raise SASLProtocolError(f'SASL state {self.state}: unexpected')

    @abstractmethod
    def exchange(self):
        """Exchange SASL messages."""

    def send(self, data: bytes):
        """Encode and send an SASL message.

        Raises:
            ConnectionError: Connection was closed.
            ProtocolError: Protocol violation.

        .. note::
            Calls :meth:`begin` if needed.
        """
        if self.state == AuthState.PREAUTH:
            self.begin(data)
        elif self.state == AuthState.RECEIVED:
            self.adapter.send(data)
            self.state = AuthState.SENT
        else:
            raise SASLProtocolError(f'SASL state {self.state}: unexpected')

    # pylint: disable=missing-raises-doc
    def receive(self) -> bytes:
        """Receive and decode an SASL message.

        Raises:
            ConnectionError: Connection was closed.
            OperationError: Authentication failed.
            ProtocolError: Protocol violation.

        .. note::
            Calls :meth:`begin` if needed.
        """
        if self.state == AuthState.PREAUTH:
            self.begin()
        if self.state == AuthState.SENT:
            try:
                data = self.adapter.receive()
                self.state = AuthState.RECEIVED
            except SieveOperationError as err:
                if err.response != 'OK':
                    raise
                if not err.matches('SASL'):
                    # pylint: disable=raise-missing-from
                    raise SASLProtocolError('expected data')
                try:
                    word = err.code[1]
                except ValueError as valuerr:
                    raise SASLProtocolError('unexpected data') from valuerr
                if isinstance(word, Atom) or not isinstance(word, str):
                    # pylint: disable=raise-missing-from
                    raise SASLProtocolError('expected string')
                data = b64decode(word)
                self.state = AuthState.DONE
            return data
        raise SASLProtocolError(f'SASL state {self.state}: unexpected')

    @property
    def sock(self) -> Union[socket.SocketType, ssl.SSLSocket]:
        """Underlying socket."""
        assert self.adapter
        return self.adapter.sock

    @sock.setter
    def sock(self, sock: Union[socket.SocketType, ssl.SSLSocket]):
        assert self.adapter
        self.adapter.sock = sock

    adapter: AbstractSASLAdapter
    """Underlying SASL adapter."""

    state: AuthState = AuthState.PREAUTH
    """Current authentication state."""


class BasePwdAuth(BaseAuth, ABC):
    """Base class for password-based authentication mechanisms.

    Prepares credentials, so that subclasses need only
    implement :meth:`exchange`. For example:

    .. literalinclude:: ../sievemgr.py
        :pyobject: PlainAuth
    """

    def __init__(self, connection: AbstractSASLAdapter,
                 authcid: str, password: str, authzid: str = '',
                 prepare: SASLPrep = SASLPrep.ALL):
        """Prepare authentication.

        `authcid`, `password`, and `authzid` are prepared according to
        :rfc:`3454` and :rfc:`4013` if ``prepare & SASLPrep.USERNAMES``
        and/or ``prepare & SASLPrep.PASSWORDS`` are non-zero.

        Arguments:
            conn: Connection over which to authenticate.
            authcid: Authentication ID (user to login as).
            password: Password.
            authzid: Authorisation ID (user whose rights to acquire).
            prepare: Which credentials to prepare.

        Raises:
            ValueError: Bad characters in username or password.
        """
        super().__init__(connection, authcid, authzid, prepare)
        prepare &= SASLPrep.PASSWORDS   # type: ignore[assignment]
        self.password = self.prepare(password) if prepare else password

    password: str
    """Password."""


class BaseScramAuth(BasePwdAuth, ABC):
    """Base class for SCRAM authentication mechanisms.

    Implements :meth:`exchange`, so that subclasses need only define a digest.
    For example:

    .. literalinclude:: ../sievemgr.py
        :pyobject: ScramSHA1Auth

    .. seealso::
        :rfc:`5802`
            Salted Challenge Response Authentication Mechanism (SCRAM).
        :rfc:`7677`
            SCRAM-SHA-256 and SCRAM-SHA-256-PLUS.
        https://datatracker.ietf.org/doc/html/draft-melnikov-scram-bis
            Updated recommendations for implementing SCRAM.
        https://datatracker.ietf.org/doc/html/draft-melnikov-scram-sha-512-03
            SCRAM-SHA-512 and SCRAM-SHA-512-PLUS.
        https://datatracker.ietf.org/doc/html/draft-melnikov-scram-sha3-512-03
            SCRAM-SHA3-512 and SCRAM-SHA3-512-PLUS.
        https://csb.stevekerrison.com/post/2022-01-channel-binding
            Discussion of TLS channel binding.
        https://csb.stevekerrison.com/post/2022-05-scram-detail
            Discussion of SCRAM.
    """

    def exchange(self):
        # Compare to
        # * https://github.com/stevekerrison/auth-examples
        # * https://github.com/horazont/aiosasl

        def todict(msg: bytes) -> dict[bytes, bytes]:
            return dict([a.split(b'=', maxsplit=1) for a in msg.split(b',')])

        def escape(b: bytes) -> bytes:
            return b.replace(b'=', b'=3D').replace(b',', b'=2C')

        # Parameters
        authcid = self.authcid.encode('utf8')
        authzid = self.authzid.encode('utf8')
        password = self.password.encode('utf8')
        chan_bind_type = self.cbtype.encode('utf8')
        chan_bind_data = self.cbdata
        c_nonce_len = self.noncelen
        digest = self.digest

        # Send client-first message
        chan_bind_attr = b'p=%s' % chan_bind_type if chan_bind_type else b'n'
        c_first_prefix = chan_bind_attr + b',' + escape(authzid)
        c_nonce = b64encode(secrets.token_bytes(c_nonce_len))
        c_first_bare = b'n=%s,r=%s' % (escape(authcid), c_nonce)
        c_first = c_first_prefix + b',' + c_first_bare
        self.send(c_first)

        # Receive server-first message
        try:
            s_first = self.receive()
        except SieveOperationError as err:
            # pylint: disable=bad-exception-cause (???)
            raise SASLCapabilityError(f'{self.name}: {err}') from err
        s_first_dict = todict(s_first)
        iters = int(s_first_dict[b'i'])
        s_nonce = s_first_dict[b'r']
        salt = b64decode(s_first_dict[b's'])

        # Send client-final message
        salted_pwd = hashlib.pbkdf2_hmac(digest, password, salt, iters)
        c_key = hmac.digest(salted_pwd, b'Client Key', digest)
        stored_key = hashlib.new(digest, c_key).digest()
        chan_bind = b64encode(c_first_prefix + b',' + chan_bind_data)
        c_final_prefix = b'c=%s,r=%s' % (chan_bind, s_nonce)
        auth_message = b','.join((c_first_bare, s_first, c_final_prefix))
        c_signature = hmac.digest(stored_key, auth_message, digest)
        c_proof = b64encode(bytes(a ^ b for a, b in zip(c_key, c_signature)))
        c_final = c_final_prefix + b',p=%s' % c_proof
        self.send(c_final)

        # Receive server-final message
        s_final = self.receive()
        s_key = hmac.digest(salted_pwd, b'Server Key', digest)
        s_signature = hmac.digest(s_key, auth_message, digest)
        s_final_dict = todict(s_final)
        if s_signature != b64decode(s_final_dict[b'v']):
            host = self.sock.getpeername()[0]
            raise SASLSecurityError(f'{host}: verification failed')

    @property
    @abstractmethod
    def digest(self) -> str:
        """Digest name as used by :mod:`hashlib` and :mod:`hmac`."""

    cbtype: str = ''
    """TLS channel-binding type."""

    cbdata: bytes = b''
    """TLS channel-binding data."""

    noncelen: int = 18
    """Client nonce length in bytes."""


class BaseScramPlusAuth(BaseScramAuth, ABC):
    """Base class for SCRAM mechanisms with channel binding.

    For example:

    .. literalinclude:: ../sievemgr.py
        :pyobject: ScramSHA1PlusAuth
    """

    # Channel-binding is, for the most part, implemented in BaseScramAuth.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not isinstance(self.sock, ssl.SSLSocket):
            raise SASLProtocolError('non-TLS channel cannot be bound')
        for cbtype in ('tls-exporter', 'tls-unique', 'tls-server-endpoint'):
            if cbtype in ssl.CHANNEL_BINDING_TYPES:
                if cbdata := self.sock.get_channel_binding(cbtype):
                    self.cbtype = cbtype
                    self.cbdata = cbdata
                    break
        else:
            raise TLSCapabilityError('no supported channel-binding type')


class AuthzUnsupportedMixin():
    """Mixin for SASL mechanisms that do not support authorisation.

    For example:

    .. literalinclude: ../sievemgr.py
        :pyobject: LoginAuth
    """

    def __init__(self, *args, **kwargs):
        """Prepare authentication.

        Raises:
            SASLCapabilityError: :attr:`authzid` is set."""
        assert isinstance(self, BaseAuth)
        super().__init__(*args, **kwargs)
        if self.authzid:
            raise SASLCapabilityError(f'{self.name}: no authorisation')


class CramMD5Auth(AuthzUnsupportedMixin, BasePwdAuth):
    """CRAM-MD5 authentication.

    .. seealso::
        :rfc:`2195` (sec. 2)
            Definition of CRAM-MD5.
    """

    def exchange(self):
        challenge = self.receive()
        password = self.password.encode('utf8')
        digest = hmac.new(password, challenge, hashlib.md5)
        data = ' '.join((self.authcid, digest.hexdigest()))
        self.send(data.encode('utf8'))

    obsolete = True
    name = 'CRAM-MD5'


class ExternalAuth(BaseAuth):
    """EXTERNAL authentication.

    .. seealso::
        :rfc:`4422` (App. A)
            Definition of the EXTERNAL mechanism.
    """

    def __call__(self):
        """Authenticate."""
        args = (self.authzid.encode('utf8'),) if self.authzid else ()
        self.begin(*args)
        self.receive()
        self.send(b'')
        self.end()

    def exchange(self):
        """No-op."""

    name = 'EXTERNAL'


class LoginAuth(AuthzUnsupportedMixin, BasePwdAuth):
    """LOGIN authentication.

    .. seealso::
        https://datatracker.ietf.org/doc/draft-murchison-sasl-login
            Definition of the LOGIN mechanism.
    """

    def __init__(self, *args, **kwargs):
        """Prepare authentication.

        Arguments:
            conn: Connection over which to authenticate.
            authcid: Authentication ID (user to login as).
            password: Password.
            authzid: Authorisation ID (user whose rights to acquire).
            prepare: Which credentials to prepare.

        Raises:
            ValueError: Password contains CR, LF, or NUL.
        """
        super().__init__(*args, **kwargs)
        if {self.password} & {'\r', '\n', '\0'}:
            raise ValueError('password: contains CR, LF, or NUL')

    def exchange(self):
        self.receive()
        self.send(self.authcid.encode('utf8'))
        self.receive()
        self.send(self.password.encode('utf8'))

    obsolete = True
    name = 'LOGIN'


class PlainAuth(BasePwdAuth):
    """PLAIN authentication.

    .. seealso::
        :rfc:`4616`
            PLAIN authentication mechanism.
    """

    def exchange(self):
        data = '\0'.join((self.authzid, self.authcid, self.password))
        self.send(data.encode('utf8'))

    name = 'PLAIN'


class ScramSHA1Auth(BaseScramAuth):
    """SCRAM-SHA-1 authentication."""

    @property
    def digest(self) -> str:
        return 'sha1'

    name = 'SCRAM-SHA-1'
    order = -10


class ScramSHA1PlusAuth(BaseScramPlusAuth, ScramSHA1Auth):
    """SCRAM-SHA-1-PLUS authentication."""
    name = 'SCRAM-SHA-1-PLUS'
    order = -1000


class ScramSHA224Auth(BaseScramAuth):
    """SCRAM-SHA-224 authentication."""

    @property
    def digest(self) -> str:
        return 'sha224'

    name = 'SCRAM-SHA-224'
    order = -20


class ScramSHA224PlusAuth(BaseScramPlusAuth, ScramSHA224Auth):
    """SCRAM-SHA-224-PLUS authentication."""
    name = 'SCRAM-SHA-224-PLUS'
    order = -2000


class ScramSHA256Auth(BaseScramAuth):
    """SCRAM-SHA-256 authentication."""

    @property
    def digest(self) -> str:
        return 'sha256'

    name = 'SCRAM-SHA-256'
    order = -30


class ScramSHA256PlusAuth(BaseScramPlusAuth, ScramSHA256Auth):
    """SCRAM-SHA-256-PLUS authentication."""
    name = 'SCRAM-SHA-256-PLUS'
    order = -3000


class ScramSHA384Auth(BaseScramAuth):
    """SCRAM-SHA-384 authentication."""

    @property
    def digest(self) -> str:
        return 'sha384'

    name = 'SCRAM-SHA-384'
    order = -40


class ScramSHA384PlusAuth(BaseScramPlusAuth, ScramSHA384Auth):
    """SCRAM-SHA-384-PLUS authentication."""
    name = 'SCRAM-SHA-384-PLUS'
    order = -4000


class ScramSHA512Auth(BaseScramAuth):
    """SCRAM-SHA-512 authentication."""

    @property
    def digest(self):
        return 'sha512'

    name = 'SCRAM-SHA-512'
    order = -50


class ScramSHA512PlusAuth(BaseScramPlusAuth, ScramSHA512Auth):
    """SCRAM-SHA-512-PLUS authentication."""
    name = 'SCRAM-SHA-512-PLUS'
    order = -5000


# pylint: disable=invalid-name
class ScramSHA3_512Auth(BaseScramAuth):
    """SCRAM-SHA-512 authentication."""

    @property
    def digest(self):
        return 'sha3_512'

    name = 'SCRAM-SHA3-512'
    order = -60


# pylint: disable=invalid-name
class ScramSHA3_512PlusAuth(BaseScramPlusAuth, ScramSHA3_512Auth):
    """SCRAM-SHA-512-PLUS authentication."""
    name = 'SCRAM-SHA3-512-PLUS'
    order = -6000


#
# SieveManager Shell
#

class BaseShell():
    """Base class for interactive shells.

    :class:`BaseShell` is similar-ish to :class:`cmd.Cmd`. However, lines read
    from standard input are :meth:`expanded <expand>` before being passed to
    methods that implement commands. :class:`BaseShell` also provides an
    extensible :meth:`completion system <complete>` as well as a built-in
    :meth:`help system <do_help>`. :attr:`aliases` can be extended, too.

    Define a :samp:`do_{command}` method to add `command`.

    For example:

    >>> class Calculator(BaseShell):
    >>>     def do_add(self, n, m):
    >>>         \"\"\"add n m - add n and m\"\"\"
    >>>         print(n + m)
    >>>
    >>>     def do_sum(self, *numbers):
    >>>         \"\"\"sum [n ...] - \"\"\"
    >>>         print sum(numbers)
    >>>
    >>>     aliases = {
    >>>         '+': 'sum'
    >>>     }
    >>>
    >>> calc = Calculator()
    >>> calc.executeline('add 0 1')
    1
    >>> calc.executeline('sum 0 1 2')
    3
    >>> calc.executeline('+ 0 1 2 3')
    6
    >>> calc.executeline('add 0')
    usage: add n m
    >>> calc.executeline('help add')
    add n m - add n and m
    """

    # Shell behaviour
    def __init__(self):
        """Initialise a :class:`BaseShell` object."""
        self.commands = tuple(self.getcommands())

    @staticmethod
    def columnise(words: Sequence[str], file: TextIO = sys.stdout,
                  width: int = shutil.get_terminal_size().columns):
        """Print `words` in columns to `file`.

        Arguments:
            words: Words.
            file: Output file.
            width: Terminal width in chars.
        """
        if (nwords := len(words)) > 0:
            colwidth = max(map(len, words)) + 1
            maxncols = max((width + 1) // colwidth, 1)
            nrows = math.ceil(nwords / maxncols)
            rows: tuple[list[str], ...] = tuple([] for _ in range(nrows))
            for i, word in enumerate(words):
                rows[i % nrows].append(word)
            for row in rows:
                line = ''.join([col.ljust(colwidth) for col in row])
                print(line.rstrip(), file=file)

    def complete(self, text: str, n: int) -> Optional[str]:
        """Completion function for :func:`readline.set_completer`.

        Tab-completion for command names (e.g., "exit") is built in. To
        enable tab-completion for the arguments of some `command`, define
        a method :samp:`complete_{command}`, which takes the index of the
        argument that should be completed and the given `text` and returns
        a sequence of :class:`str`-:class:`bool` pairs, where the string
        is a completion and the boolean indicates whether a space should
        be appended to that completion.

        For example:

        >>> class Foo(BaseShell)
        >>>     def do_cmd(self, arg1, arg2):
        >>>         pass
        >>>
        >>>     def complete_cmd(self, argidx, text):
        >>>         if argidx == 1:
        >>>             return [(s, True) for s in ('foo', 'bar', 'baz')]
        >>>         if argidx == 2:
        >>>             return [('quux/', False)]
        >>>         return []
        >>>
        >>> foo = Foo()
        >>> foo.complete('', 0)
        'cmd '
        >>> foo.complete('', 1)
        None
        >>> foo.complete('cmd ', 0)
        'foo '
        >>> foo.complete('cmd ', 1)
        'bar '
        >>> foo.complete('cmd ', 2)
        'baz '
        >>> foo.complete('cmd ', 3)
        None
        >>> foo.complete('cmd b', 0)
        'bar '
        >>> foo.complete('cmd b', 1)
        'baz '
        >>> foo.complete('cmd b', 2)
        None
        >>> foo.complete('cmd bar ', 0)
        'quux/'
        >>> foo.complete('cmd bar ', 1)
        None

        Arguments:
            text: Possibly partial word to be completed.
            n: Index of the completion to return.

        Returns:
            Either the `n`-th completion for `text` or
            ``None`` if there is no such completion.

        .. admonition:: Side-effects

            * Logging of messages with a priority lower than
              :data:`logging.ERROR` is suppressed during tab-completion.
            * A BEL is printed to the controlling terminal if
              no completion for `text` is found.
        """
        if n == 0:
            logger = self.logger
            loglevel = logger.level
            if loglevel < logging.ERROR:
                logger.setLevel(logging.ERROR)
            try:
                if args := self.getargs():
                    command = self.aliases.get(args[0], args[0])
                    try:
                        complete = getattr(self, f'complete_{command}')
                    except AttributeError:
                        complete = None
                    self._completions = []
                    self._completions = sorted(
                        shlex.quote(word) + (' ' if space else '')
                        for word, space in complete(len(args), text)
                        if fnmatch.fnmatchcase(word, text + '*')
                    ) if complete else []
                else:
                    self._completions = sorted(c + ' ' for c in self.commands
                                               if c.startswith(text))
                if text and not self._completions:
                    bell()
            finally:
                logger.setLevel(loglevel)
        try:
            return self._completions[n]
        except IndexError:
            return None

    @staticmethod
    def confirm(prompt: str, default: ConfirmEnum = ConfirmEnum.NO,
                multi: bool = False, attempts: int = 3) -> ConfirmEnum:
        """Prompt the user for confirmation.

        Arguments:
            prompt: Prompt.
            default: Default.
            multi: Give choices "all" and "none"?
            attempts: How often to try before raising a :exc:`ValueError`.

        Raises:
            ValueError: Unrecognised answer.
        """
        assert attempts > 0
        with TermIO() as tty:
            for _ in range(attempts):
                tty.write(prompt + ' ')
                answer = tty.readline().strip().casefold()
                if answer == '':
                    return default
                if answer in ('y', 'yes'):
                    return ConfirmEnum.YES
                if answer in ('n', 'no'):
                    return ConfirmEnum.NO
                if multi:
                    if answer == 'all':
                        return ConfirmEnum.ALL
                    if answer == 'none':
                        return ConfirmEnum.NONE
                    tty.write('Enter "yes", "no", "all", or "none"\n')
                else:
                    tty.write('Enter "yes" or "no"\n')
            raise ValueError('too many retries')
            # NOTREACHED

    def enter(self) -> int:
        """Start reading commands from standard input.

        Reading stops at the end-of-file marker or when
        a command raises :exc:`StopIteration`.

        .. admonition:: Side-effects

            Entering the shell binds :kbd:`Tab` to :func:`readline.complete`.
        """
        hasatty = self.hasatty()
        if hasatty:
            oldcompleter = readline.get_completer()
            olddelims = readline.get_completer_delims()
            readline.set_auto_history(True)
            readline.set_completer(self.complete)
            readline.set_completer_delims(' ')
            readline.parse_and_bind('tab: complete')
            if readline.__doc__ and 'libedit' in readline.__doc__:
                readline.parse_and_bind('python:bind ^I rl_complete')
        try:
            while True:
                try:
                    prompt = self.getprompt() if hasatty else None
                    line = input(prompt).strip()
                except EOFError:
                    break
                try:
                    self.retval = self.executeline(line)
                except StopIteration:
                    break
        finally:
            if hasatty:
                readline.set_completer(oldcompleter)
                readline.set_completer_delims(olddelims)
        return self.retval

    def execute(self, command: str, *args: str) -> int:
        """Execute `command`.

        For example:

        >>> shell.execute('ls', 'foo', 'bar')
        0

        Arguments:
            command: Command name.
            args: Arguments to the command.

        Returns:
            Return value.

        Raises:
            ShellUsageError: Command not found or arguments invalid.
        """
        try:
            method = getattr(self, f'do_{command}')
        except AttributeError as err:
            raise ShellUsageError(f'{command}: no such command') from err
        try:
            inspect.signature(method).bind(*args)
        except TypeError as err:
            raise ShellUsageError(self.getusage(method)) from err
        self.retval = 0 if (retval := method(*args)) is None else retval
        return self.retval

    def executeline(self, line: str) -> int:
        """:meth:`Split <split>` `line` and :meth:`execute` it.

        For example:

        >>> shell.executeline('ls foo bar')
        0

        Returns:
            Return value.

        Raises:
            ShellUsageError: Command not found or arguments invalid.
        """
        for alias, command in self.aliases.items():
            prefixlen = len(alias)
            if (stripped := line.strip()).startswith(alias):
                args = self.expand(stripped[prefixlen:])
                break
        else:
            try:
                command, *args = self.expand(line)
            except ValueError:
                return 0
        return self.execute(command, *args)

    def executescript(self, script: TextIO) -> int:
        """Split `script` into lines and :meth:`execute <excuteline>` them.

        For example:

        >>> with open('scriptfile') as scriptfile:
        >>>     shell.executescript(scriptfile)
        0

        Returns:
            Return value.

        Raises:
            ShellUsageError: Command not found or arguments invalid.
        """
        for line in script:
            self.retval = self.executeline(line)
        return self.retval

    def expand(self, line: str) -> list[str]:
        """Expand the words that comprise `line`.

        Similar to :manpage:`wordexp(3)`. Patterns are expanded using
        :func:`fnmatch.fnmatchcase`, with filenames being provided by
        the :meth:`completion system <complete>`.

        For example:

        >>> class Foo(BaseShell)
        >>>     def complete_cmd(self, _, text):
        >>>         return [(s, True) for s in ('foo', 'bar', 'baz')]
        >>>
        >>> foo = Foo()
        >>> foo.expand('cmd *')
        ['cmd', 'foo', 'bar', 'baz']
        """
        fnmatchcase = fnmatch.fnmatchcase
        expanded: list[str] = []
        unescpattern: re.Pattern = re.compile(r'\\([*?\[\]])')
        words = self.split(line)
        try:
            gettokens = getattr(self, f'complete_{words[0]}')
        except (IndexError, AttributeError):
            gettokens = None
        for i, word in enumerate(words):
            if gettokens and isinstance(word, ShellPattern):
                matches = sorted(token for token, _ in gettokens(i, '')
                                 if (not token.startswith('.')
                                     and fnmatchcase(token, word)))
                if not matches:
                    raise ValueError(f'{word}: no matches')
                expanded.extend(matches)
            else:
                expanded.append(unescpattern.sub(r'\1', word))
        return expanded

    @classmethod
    def getargs(cls) -> list[ShellWord]:
        """:meth:`Split <split>` line before current completion scope."""
        begin = readline.get_begidx()
        buffer = readline.get_line_buffer()
        return cls.split(buffer[:begin])

    @classmethod
    def getcommands(cls) -> Iterator[str]:
        """Get the shell commands provided by `cls`.

        For example:

        >>> class Foo(BaseShell)
        >>>     def do_cmd(self, arg1, arg2):
        >>>         pass
        >>>
        >>> tuple(Foo.getcommands())
        ('cmd', 'exit', 'help')
        >>> foo = Foo()
        >>> foo.commands
        ('cmd', 'exit', 'help')
        """
        for attr in dir(cls):
            with suppress(ValueError):
                prefix, name = attr.split('_', maxsplit=1)
                if prefix == 'do' and name:
                    yield name

    def getprompt(self) -> str:
        """Get a shell prompt."""
        return '> '

    @staticmethod
    def getusage(func: Callable) -> Optional[str]:
        """Derive a usage message from `func`'s docstring.

        :func:`getusage` assumes that the docstring has the form
        :samp:`{command} {args} - {description}`. The usage message
        is either the text up to the last dash ("-") or, if the
        docstring does not contain a dash, the whole docstring.
        Leading and trailing whitespace is stripped.

        For example:

        >>> def frobnicate(foo, bar):
        >>>     \"\"\"frobnicate foo bar - frobnicate foo with bar\"\"\"
        >>>     ...
        >>>
        >>> BaseShell.getusage(frobnicate)
        'frobnicate foo bar'
        """
        if (doc := func.__doc__) and (syn := doc.rsplit('-', 1)[0].strip()):
            return 'usage: ' + syn
        return None

    @staticmethod
    def hasatty() -> bool:
        """Is standard input a terminal?"""
        return os.isatty(sys.stdin.fileno())

    @staticmethod
    def split(line: str) -> list['ShellWord']:
        """Split `line` into words as a POSIX-compliant shell would."""
        buffer: ShellWord = ''
        escape: bool = False
        quotes: list[str] = []
        tokens: list[ShellWord] = []

        unquotepattern = re.compile(r'\[(.)\]')
        def addtoken(token: ShellWord):
            if not isinstance(token, ShellPattern):
                token, _ = unquotepattern.subn(r'\1', token)
            tokens.append(token)

        for i, char in enumerate(line):
            if escape:
                buffer += f'[{char}]' if char in '*?[' else char
                escape = False
            elif quotes:
                if char in '\'"':
                    if char == quotes[-1]:
                        del quotes[-1]
                    else:
                        quotes.append(char)
                    if quotes:
                        buffer += char
                elif char == '\\':
                    escape = True
                else:
                    buffer += f'[{char}]' if char in '*?[' else char
            elif char == '\\':
                escape = True
            elif char in '\'"':
                quotes.append(char)
            elif char.isspace():
                if i > 0 and not line[i - 1].isspace():
                    addtoken(buffer)
                    buffer = ''
            elif char == '#':
                break
            else:
                if char in '*?[':
                    buffer = ShellPattern(buffer)
                buffer += char
        if buffer:
            addtoken(buffer)
        return tokens

    # Basic commands
    def do_exit(self):
        """exit - exit the shell"""
        raise StopIteration()

    def do_help(self, name: Optional[str] = None):
        """help [command] - list commands/show help for command"""
        if name:
            try:
                print(getattr(self, f'do_{name}').__doc__)
            except AttributeError:
                self.logger.error('%s: Unknown command', name)
        else:
            self.columnise(self.commands)

    # Completers
    def complete_help(self, *_) -> tuple[tuple[str, bool], ...]:
        """Completer for help."""
        return tuple((c, True) for c in self.commands)

    # Attributes
    aliases: dict[str, str] = {
        '!': 'sh',
        '?': 'help'
    }
    """Mapping of aliases to :attr:`commands`."""

    commands: tuple[str, ...]
    """Shell commands. Populated by :meth:`__init__`."""

    logger: logging.Logger = logging.getLogger(__name__)
    """Logger.

    Messages are logged with the following priorities:

    ======================  ======================================
    Priority                Used for
    ======================  ======================================
    :const:`logging.INFO`   Help message when the shell is entered
    ======================  ======================================
    """

    retval: int = 0
    """Return value of the most recently completed command."""

    _completions: list[str] = []
    """Most recent completions."""


# pylint: disable=too-many-public-methods
class SieveShell(BaseShell):
    """Shell around a `SieveManager` connection."""

    def __init__(self, manager: 'SieveManager', clobber: bool = True,
                 confirm: ShellCmd = ShellCmd.ALL):
        """Initialise a :class:`SieveShell` object.

        Arguments:
            manager: Connection to a ManageSieve server.
            clobber: Overwrite files?
            confirm: Shell commands that require confirmation.
        """
        super().__init__()
        self.clobber = clobber
        self.reqconfirm = confirm
        self.manager = manager

    # Methods
    def getprompt(self, *args, **kwargs):
        prompt = super().getprompt(*args, **kwargs)
        mgr = self.manager
        if mgr and (url := mgr.geturl()) is not None:
            prompt = ('' if mgr.tls else '(insecure) ') + str(url) + prompt
        return prompt

    def enter(self) -> int:
        # pylint: disable=redefined-outer-name
        error = self.logger.error
        info = self.logger.info
        if self.hasatty():
            info('Enter "? [command]" for help and "exit" to exit')
        while True:
            try:
                return super().enter()
            except (ConnectionError, DNSError, ProtocolError, SecurityError):
                raise
            # pylint: disable=broad-exception-caught
            except Exception as err:
                if not self.hasatty():
                    raise
                if isinstance(err, (GetoptError, UsageError)):
                    error('%s', err)
                    self.retval = 2
                elif isinstance(err, subprocess.CalledProcessError):
                    error('%s exited with status %d',
                          err.cmd[0], err.returncode)
                    self.retval = 1
                elif isinstance(err, (FileNotFoundError, FileExistsError)):
                    error('%s: %s', err.filename, os.strerror(err.errno))
                    self.retval = 1
                # pylint: disable=no-member
                elif isinstance(err, OSError) and err.errno:
                    error('%s', os.strerror(err.errno))
                    self.retval = 1
                elif isinstance(err, (Error, OSError, ValueError)):
                    for line in str(err).splitlines():
                        error('%s', line)
                    self.retval = 1
                else:
                    raise
        # NOTREACHED

    def execute(self, *args, **kwargs) -> int:
        retval = super().execute(*args, **kwargs)
        if warning := self.manager.warning:
            for line in warning.splitlines():
                self.logger.warning('%s', escapectrl(line))
        return retval

    def editscripts(self, editor: list[str], *args: str):
        """Edit scripts with the given `editor`."""
        mgr = self.manager

        def retry(err: Exception, script: str) -> bool:
            print(str(err).rstrip('\r\n'), file=sys.stderr)
            return bool(self.confirm(f'Re-edit {script}?',
                        default=ConfirmEnum.YES))

        (opts, scripts) = getopt(list(args), 'a')
        for opt, _ in opts:
            if opt == '-a':
                scripts = [active] if (active := mgr.getactive()) else []
        if scripts:
            mgr.editscripts(editor, list(scripts), catch=retry)
        else:
            self.logger.error('No scripts given')

    # Shell commands
    @staticmethod
    def do_about():
        """about - show information about SieveManager"""
        print(ABOUT.strip())

    def do_activate(self, script: str):
        """activate script - mark script as active"""
        self.manager.setactive(script)

    # pylint: disable=redefined-loop-name
    def do_caps(self):
        """caps - show server capabilities"""
        print('---')
        if (caps := self.manager.capabilities) is not None:
            for key, value in caps.__dict__.items():
                if not value:
                    continue
                if key in ('implementation', 'language',
                           'maxredirects', 'owner', 'version'):
                    if isinstance(value, str):
                        value = yamlescape(value)
                    print(f'{key}: {value}')
                elif key in ('notify', 'sasl', 'sieve'):
                    items = [yamlescape(i) if isinstance(i, str) else str(i)
                             for i in value]
                    # pylint: disable=consider-using-f-string
                    print('{}: [{}]'.format(key, ', '.join(items)))
                elif key in ('starttls', 'unauthenticate'):
                    print(f'{key}: yes')
            for key, value in caps.notunderstood.items():
                if value is not None:
                    if isinstance(value, str):
                        value = yamlescape(value)
                    print(f'{key}: {value}')
        print('...')

    def do_cat(self, *scripts: str):
        """cat [script ...] - concatenate scripts on standard output"""
        for script in scripts:
            sys.stdout.write(self.manager.getscript(script))

    def do_cd(self, localdir: str = HOME):
        """cd [localdir] - change local directory"""
        os.chdir(localdir)
        self.logger.info('Changed directory to %s', localdir)

    # pylint: disable=redefined-loop-name
    def do_cert(self):
        """cert - show the server's TLS certificate."""
        indent = ' ' * 4
        mgr = self.manager
        if not isinstance(mgr.sock, ssl.SSLSocket):
            raise ShellUsageError('not a secure connection')
        cert = mgr.sock.getpeercert()
        assert cert
        value: Any
        print('---')
        for key, value in sorted(cert.items()):
            if key in ('OCSP', 'caIssuers', 'crlDistributionPoints'):
                print(f'{key}:')
                for item in sorted(value):
                    if isinstance(item, str):
                        item = yamlescape(item)
                    print(f'{indent}- {item}')
            elif key in ('issuer', 'subject'):
                print(f'{key}:')
                for pairs in sorted(value):
                    print(f'{indent}- ', end='')
                    for i, (k, v) in enumerate(pairs):
                        if isinstance(v, str):
                            v = yamlescape(v)
                        if i == 0:
                            print(f'{k}: {v}')
                        else:
                            print(f'{indent}  {k}: {v}\n')
            elif key == 'subjectAltName':
                print(f'{key}:')
                for k, v in sorted(value):
                    v = yamlescape(v)
                    print(f'{indent}- {k}: {v}')
            elif isinstance(value, str):
                value = yamlescape(value)
                print(f'{key}: {value}')
            elif isinstance(value, int):
                print(f'{key}: {value}')
        print('...')

    def do_check(self, localscript: str):
        """check localscript - check whether localscript is valid"""
        with open(localscript, 'rb', encoding='utf8') as file:
            # checkscript performs a blocking send/sendline,
            # but holding a lock should be okay in an interactive app.
            fcntl.flock(file.fileno(), LOCK_SH | LOCK_NB)
            self.manager.checkscript(file)
        self.logger.info('%s is valid', localscript)

    def do_cmp(self, *args: str) -> int:
        """cmp [-s] script1 [...] scriptN - compare scripts"""
        silent = False
        opts, scripts = getopt(list(args), 's')
        for opt, _ in opts:
            if opt == '-s':
                silent = True
        if len(scripts) < 2:
            message = self.getusage(self.do_cmp)
            assert message
            raise ShellUsageError(message)
        prefix = ', '.join(scripts)
        contents = map(self.manager.getscript, scripts)
        iters = map(str.splitlines, contents)
        for i, lines in enumerate(itertools.zip_longest(*iters), start=1):
            for j, chars in enumerate(itertools.zip_longest(*lines), start=1):
                char1 = chars[0]
                for char2 in chars[1:]:
                    if char1 != char2:
                        if not silent:
                            print(f'{prefix}: line {i}, column {j} differs')
                        return 1
        if not silent:
            print(f'{prefix}: equal')
        return 0

    def do_cp(self, *args: str):
        """cp [-f|-i] source target - re-upload source as target"""
        clobber = self.clobber
        confirm = bool(self.reqconfirm & ShellCmd.CP)
        opts, scripts = getopt(list(args), 'Cfi')
        for opt, _ in opts:
            if opt == '-f':
                clobber = True
                confirm = False
            elif opt == '-i':
                clobber = True
                confirm = True
        try:
            source, target = scripts
        except ValueError as err:
            message = self.getusage(self.do_cp)
            assert message
            raise ShellUsageError(message) from err
        if self.manager.scriptexists(target):
            if not clobber:
                raise FileExistsError(EEXIST, os.strerror(EEXIST), target)
            if confirm and not self.confirm(f'Overwrite {target}?'):
                return
        self.manager.copyscript(source, target)

    def do_deactivate(self):
        """deactivate - deactivate the active script"""
        self.manager.unsetactive()

    def do_diff(self, *args: str) -> int:
        """diff <options> script1 script2 - show how scripts differ"""
        pairs, scripts = getopt(list(args), 'C:U:bcu')
        opts = tuple(filter(bool, itertools.chain(*pairs)))
        if len(scripts) != 2:
            message = self.getusage(self.do_diff)
            assert message
            raise ShellUsageError(message)
        cp = self.manager.editscripts(['diff', *opts], scripts, check=False)
        return cp.returncode

    def do_echo(self, *args: str):
        """echo word [...] - print words to standard output."""
        print(*args)

    def do_ed(self, *args: str):
        """ed [-a] script [...] - edit scripts with a line editor"""
        self.editscripts(EDITOR, *args)

    def do_get(self, *args: str):
        """get [-a] [-f|-i] [-o file] [script ...] - download script"""
        mgr = self.manager
        opts, sources = getopt(list(args), 'afio:')
        output = ''
        clobber = self.clobber
        confirm = bool(self.reqconfirm & ShellCmd.GET)
        multi = len(sources) > 1
        for opt, arg in opts:
            if opt == '-a':
                sources = [active] if (active := mgr.getactive()) else []
            elif opt == '-f':
                clobber = True
                confirm = False
            elif opt == '-i':
                clobber = True
                confirm = True
            elif opt == '-o':
                if multi:
                    raise ShellUsageError('-o: too many sources')
                output = arg
        answer = ConfirmEnum.NO if confirm else ConfirmEnum.ALL
        keep = mgr.backup
        for src in sources:
            # Try not to make a backup if the source doesn't exist.
            # Writing to a temporary file would create a worse race condition.
            if keep > 0:
                if not mgr.scriptexists(src):
                    raise FileNotFoundError(ENOENT, os.strerror(ENOENT), src)
            targ = output if output else src
            flags = O_CREAT | O_EXCL | O_WRONLY | O_TRUNC
            if path.exists(targ):
                if not clobber:
                    raise FileExistsError(EEXIST, os.strerror(EEXIST), targ)
                if answer not in (ConfirmEnum.ALL, ConfirmEnum.NONE):
                    answer = self.confirm(f'Overwrite {targ}?', multi=multi)
                if answer:
                    def getfiles() -> Iterator[str]:
                        # pylint: disable=cell-var-from-loop
                        return readdir(path.dirname(targ), path.isfile)
                    backup(targ, keep, getfiles, shutil.copy, os.remove)
                    flags &= ~O_EXCL
                else:
                    continue
            fd = os.open(targ, flags, mode=0o644)
            # getscript performs a blocking read,
            # but holding a lock should be okay in an interactive app.
            fcntl.flock(fd, LOCK_SH | LOCK_NB)
            with os.fdopen(fd, 'w', encoding='utf8') as file:
                file.write(mgr.getscript(src))
            self.logger.info('Downloaded %s as %s', src, targ)

    def do_ls(self, *args: str):
        """ls [-1al] [script ...] - list scripts"""
        active = False
        long = False
        one = not self.hasatty()
        (opts, fnames) = getopt(list(args), '1al')
        for opt, _ in opts:
            if opt == '-1':
                one = True
            elif opt == '-a':
                active = True
            elif opt == '-l':
                long = True
        if active:
            if script := self.manager.getactive():
                print(script)
            else:
                self.logger.warning('no active script')
        else:
            scripts = self.manager.listscripts()
            if fnames:
                existing = {fname for fname, _ in scripts}
                for name in set(fnames) - existing:
                    raise FileNotFoundError(ENOENT, os.strerror(ENOENT), name)
                scripts = [s for s in scripts if s[0] in fnames]
            scripts.sort()
            if long:
                for fname, active in scripts:
                    print('a' if active else '-', fname)
                print('e')
            elif one:
                for script, _ in scripts:
                    print(script)
            else:
                words = [f + ('*' if a else '') for f, a in scripts]
                self.columnise(words)

    def do_more(self, *args: str):
        """more <options> script [...] - display scripts page-by-page."""
        mgr = self.manager
        pairs, scripts = getopt(list(args), 'aceis')
        opts = list(filter(bool, itertools.chain(*pairs)))
        if '-a' in opts:
            active = mgr.getactive()
            if active is None:
                self.logger.warning('no active script')
                return
            scripts = [active]
            opts.remove('-a')
        elif not scripts:
            message = self.getusage(self.do_more)
            assert message
            raise ShellUsageError(message)
        mgr.editscripts(PAGER + opts, list(scripts))

    def do_mv(self, *args: str):
        """mv [-f|-i] source target - rename source to target"""
        clobber = self.clobber
        confirm = bool(self.reqconfirm & ShellCmd.MV)
        mgr = self.manager
        opts, scripts = getopt(list(args), 'Cfi')
        for opt, _ in opts:
            if opt == '-f':
                clobber = True
                confirm = False
            elif opt == '-i':
                clobber = True
                confirm = True
        try:
            source, target = scripts
        except ValueError as err:
            message = self.getusage(self.do_mv)
            assert message
            raise ShellUsageError(message) from err
        if mgr.scriptexists(target):
            if not clobber:
                raise FileExistsError(EEXIST, os.strerror(EEXIST), target)
            if confirm and not self.confirm(f'Overwrite {target}?'):
                return
            mgr.backupscript(target)
            mgr.deletescript(target)
        mgr.renamescript(source, target, emulate=True)

    def do_put(self, *args: str):
        """put [-f|-i] [-a] [-o name] [localscript ...] - upload scripts"""
        active: Optional[str] = None
        clobber: bool = self.clobber
        confirm: bool = bool(self.reqconfirm & ShellCmd.PUT)
        mgr: SieveManager = self.manager
        output: str = ''
        activate: bool = False
        opts, sources = getopt(list(args), 'Cafio:')
        multi = len(sources) > 1
        for opt, arg in opts:
            if opt == '-a':
                if multi:
                    raise ShellUsageError('-a: only one script can be active')
                active = mgr.getactive()
                activate = True
                if active:
                    output = active
            elif opt == '-f':
                clobber = True
                confirm = False
            elif opt == '-i':
                clobber = True
                confirm = True
            elif opt == '-o':
                if multi:
                    raise ShellUsageError('-o: too many sources')
                output = arg
        answer = ConfirmEnum.NO if confirm else ConfirmEnum.ALL
        for src in sources:
            targ = output if output else src
            if mgr.scriptexists(targ):
                if not clobber:
                    raise FileExistsError(EEXIST, os.strerror(EEXIST), targ)
                if answer not in (ConfirmEnum.ALL, ConfirmEnum.NONE):
                    answer = self.confirm(f'Overwrite {targ}?', multi=multi)
                if not answer:
                    continue
            with open(src, encoding='utf8') as file:
                # checkscript performs a blocking send/sendline,
                # but holding a lock should be okay in an interactive app.
                fcntl.flock(file.fileno(), LOCK_SH | LOCK_NB)
                mgr.putscript(file, targ)
            if activate and targ != active:
                mgr.setactive(targ)

    def do_python(self):
        """python - enter Python read-evaluate-print loop"""
        hasatty = self.hasatty()
        wrapper = ObjWrapper(self.manager)
        if hasatty:
            oldcompleter = readline.get_completer()
            readline.set_completer(rlcompleter.Completer(wrapper).complete)
            with suppress(AttributeError):
                readline.clear_history()
            readline.set_auto_history(True)
        try:
            with suppress(SystemExit):
                banner = (f'Python {sys.version}\n'
                           'Enter "help()" for help and "exit()" to exit')
                code.interact(local=wrapper, banner=banner, exitmsg='')
        finally:
            if hasatty:
                readline.set_completer(oldcompleter)
                with suppress(AttributeError):
                    readline.clear_history()

    def do_rm(self, *args: str):
        """rm [-f|-i] [script ...] - remove script"""
        confirm = bool(self.reqconfirm & ShellCmd.RM)
        opts, scripts = getopt(list(args), 'fi')
        for opt, _ in opts:
            if opt == '-f':
                confirm = False
            elif opt == '-i':
                confirm = True
        answer = ConfirmEnum.NO if confirm else ConfirmEnum.ALL
        multi = len(scripts) > 1
        for script in scripts:
            if answer is not ConfirmEnum.ALL:
                answer = self.confirm(f'Remove {script}?', multi=multi)
                if answer is ConfirmEnum.NONE:
                    self.logger.info('Stopped')
                    break
            if answer:
                self.manager.deletescript(script)

    def do_sh(self, *args: str):
        """sh [command] [argument ...] - run system command or system shell"""
        if not args:
            args = (pwd.getpwuid(os.getuid()).pw_shell,)
        subprocess.run(args, check=True)

    def do_su(self, user: str):
        """su user - manage scripts of user."""
        mgr = self.manager
        # pylint: disable=protected-access
        _, (args, kwargs) = mgr._getstate()
        kwargs['owner'] = user
        if mgr.login:
            mgr.unauthenticate()
        # Some ManageSieve servers reject the first
        # "AUTHENTICATE" after an "UNAUTHENTICATE".
        for i in range(2):
            try:
                mgr.authenticate(*args, **kwargs)
            except SieveOperationError:
                if i:
                    raise
                continue
            break

    def do_vi(self, *args: str):
        """vi [-a] script [...] - edit scripts with a visual editor"""
        self.editscripts(VISUAL, *args)

    def do_xargs(self, command: str, *args: str):
        """xargs cmd [arg ...] - call cmd with arguments from standard input"""
        try:
            func = getattr(self, f'do_{command}')
        except AttributeError as err:
            raise ShellUsageError(f'{command}: no such command') from err
        lines = []
        with suppress(EOFError):
            while line := sys.stdin.readline().rstrip('\n'):
                lines.append(line)
        return func(*args, *lines)

    # Globbing and tab-completion
    @staticmethod
    def complete_dirs(_: int, text: str) -> list[tuple[str, bool]]:
        """Complete local directory names."""
        return [(d + '/', False)
                for d in readdir(path.dirname(text), path.isdir)]

    @staticmethod
    def complete_files(_: int, text: str) -> list[tuple[str, bool]]:
        """Complete local filenames."""
        return [(f + '/', False) if path.isdir(f) else (f, True)
                for f in readdir(path.dirname(text))]

    def complete_scripts(self, *_) -> list[tuple[str, bool]]:
        """Complete script names."""
        return [(s, True) for s, _ in self.manager.listscripts(cached=True)]

    complete_activate = complete_scripts
    """Completer for activate."""

    complete_cat = complete_scripts
    """Completer for cat."""

    complete_cd = complete_dirs
    """Completer for cd."""

    complete_cmp = complete_scripts
    """Completer for cmp."""

    complete_cp = complete_scripts
    """Completer for cp."""

    complete_check = complete_files
    """Completer for check."""

    complete_diff = complete_scripts
    """Completer for diff."""

    complete_ed = complete_scripts
    """Completer for ed."""

    complete_get = complete_scripts
    """Completer for get."""

    complete_ls = complete_scripts
    """Completer for ls."""

    complete_more = complete_scripts
    """Completer for more."""

    complete_mv = complete_scripts
    """Completer for mv."""

    complete_put = complete_files
    """Completer for put."""

    complete_rm = complete_scripts
    """Completer for rm."""

    complete_vi = complete_scripts
    """Completer for vi."""

    # Properties
    clobber: bool
    """Overwrite files?"""

    reqconfirm: ShellCmd
    """Commands that require confirmation."""

    manager: SieveManager
    """Connection to a ManageSieve server."""


class ObjWrapper(dict):
    """Object wrapper for use with :func:`code.interact`.

    Arguments:
        obj: Object to wrap.
    """

    def __init__(self, obj: Any):
        """Initialise a proxy."""
        pairs: dict[str, Any] = {}
        for key, value in globals().items():
            pairs[key] = value
        for cls in obj.__class__.__mro__:
            pairs |= cls.__dict__
        for name in dir(obj):
            pairs[name] = getattr(obj, name)
        for name in dir(self):
            pairs[name] = getattr(self, name)
        super().__init__(pairs)

    @staticmethod
    def exit():
        """Exit the Python read-evaluate-print loop."""
        raise SystemExit()

    # Needed, or else `help` ignores the wrapper.
    @staticmethod
    def help(*args, **kwargs):
        """Show help."""
        help(*args, **kwargs)


#
# Configuration
#

BaseConfigT = TypeVar('BaseConfigT', bound='BaseConfig')
"""Type variable for :class:`BaseConfig`."""


class BaseConfig(UserDict):
    """Base class for configurations."""

    def __or__(self: BaseConfigT, other) -> BaseConfigT:
        obj = self.__class__()
        obj.__ior__(self)
        obj.__ior__(other)
        return obj

    def __ior__(self: BaseConfigT, other) -> BaseConfigT:
        super().__ior__(other)
        with suppress(AttributeError):
            for key, value in other._sections.items():
                UserDict.__ior__(self._sections[key], value)
        return self

    def loadfile(self, fname: str):
        """Read configuration variables from `fname`.

        Raises:
            AppConfigError: Syntax error.
        """
        ptr = self
        cwd = os.getcwd()
        with open(fname) as file:
            if basedir := path.dirname(fname):
                os.chdir(basedir)
            try:
                for i, line in enumerate(file, start=1):
                    if (pair := line.strip()) and not pair.startswith('#'):
                        try:
                            key, value = pair.split(maxsplit=1)
                            if key == self._section:
                                if value not in self._sections:
                                    self._sections[value] = self.__class__()
                                ptr = self._sections[value]
                            else:
                                ptr.set(key, value)
                        except (AttributeError, TypeError, ValueError) as err:
                            message = f'{fname}:{i}: {err}'
                            raise AppConfigError(message) from err
            finally:
                os.chdir(cwd)

    def parse(self, expr: str):
        """Split `expr` into a name and a value and set the variable.

        `Expr` is split at the first equals sign ("=").
        :samp:`{var}` is equivalent to :samp:`{var}=yes`.
        :samp:`no{var}` is equivalent to :samp:`{var}=no`.
        """
        value: Union[bool, str]
        try:
            name, value = expr.split('=', maxsplit=1)
        except ValueError:
            if expr.startswith('no'):
                name, value = expr[2:], False
            else:
                name, value = expr, True
        if value == '':
            raise ValueError(f'{name}: empty')
        self.set(name, value)

    def set(self, name: str, value):
        """Set the configuration variable `name` to `value`.

        raises:
            AttributeError: Bad variable.
        """
        if name.startswith('_'):
            raise AttributeError(f'{name}: private variable')
        try:
            attr = getattr(self, name)
        except AttributeError as err:
            raise AttributeError(f'{name}: no such variable') from err
        if callable(attr):
            raise AttributeError(f'{name}: not a variable')
        try:
            setattr(self, name, value)
        except AttributeError as err:
            raise AttributeError(f'{name}: read-only variable') from err
        except (TypeError, ValueError) as err:
            raise err.__class__(f'{name}: {err}')

    @property
    def sections(self: BaseConfigT) -> dict[str, BaseConfigT]:
        """Sections in the loaded configuration files."""
        return self._sections

    _section: ClassVar[str]
    """Name of the statement that starts a section."""

    _sections: dict[str, Any] = {}
    """Sections in the loaded configuration files."""


class BaseVar(ABC):
    """Base class for :class:`BaseConfig` attributes.

    For example:

    >>> @dataclasses.dataclass
    >>> class FooConfig(BaseConfig):
    >>>     foo = BoolVar(default=False)
    >>>     bar = NumVar(cls=int, default=0)
    >>>
    >>> foo = FooConfig(bar=1)
    >>> foo.foo
    False
    >>> foo.bar
    1
    >>> foo.foo = 'yes'
    >>> foo.foo
    True
    >>> foo.bar = '2'
    >>> foo.bar
    2
    """

    def __init__(self, default: Any = None):
        """Initialise a configuration variable."""
        self.default = default

    def __get__(self, obj: BaseConfig, _: type) -> Any:
        try:
            return obj[self.name]
        except KeyError:
            return self.default

    def __set__(self, obj: BaseConfig, value: Any):
        if value is None:
            with suppress(KeyError):
                del obj[self.name]
        else:
            obj[self.name] = value

    def __set_name__(self, _: object, name: str):
        self.name = name

    name: str
    """Variable name."""

    default: Any
    """Default value."""


class ExpandingVarMixin():
    """Mixin for variables that do word expansion."""

    def expand(self, obj: BaseConfig, value: str) -> str:
        """Expand '~' and configuration variables."""
        assert isinstance(self, BaseVar)
        template = string.Template(value)
        # template.get_identifiers is only available in Python >= v3.11.
        varnames: set[str] = set()
        # pylint: disable=consider-using-f-string
        for pattern in (r'\$(%s)' % template.idpattern,
                        r'\$\{(%s)\}' % template.idpattern):
            for match in re.finditer(pattern, value, flags=re.IGNORECASE):
                varnames.add(match.group(1))
        variables = {}
        for name in varnames:
            try:
                var = getattr(obj, name)
            except AttributeError as err:
                raise ValueError(f'${name}: no such variable') from err
            if var is None:
                raise ValueError(f'${name}: not set')
            if not isinstance(var, (int, str)):
                raise ValueError(f'${name}: not a scalar')
            variables[name] = var
        return path.expanduser(template.substitute(variables))


class ListVarMixin():
    """Mixin for lists."""

    splititems: Callable = re.compile(r'\s*,\s*').split
    """Split a comma-separated list into items."""


class BoolVar(BaseVar):
    """Convert "yes" and "no" to :class:`bool`."""

    def __set__(self, obj: BaseConfig, value: Union[bool, str]):
        if value in (True, 'yes'):
            super().__set__(obj, True)
        elif value in (False, 'no'):
            super().__set__(obj, False)
        else:
            raise ValueError(f'{value}: not a boolean')


class CmdVar(BaseVar, ExpandingVarMixin):
    """Split up value into a list using :func:`shlex.split`."""

    def __set__(self, obj: BaseConfig, value: str):
        super().__set__(obj, shlex.split(value, posix=True))

    def __get__(self, obj: BaseConfig, objtype: type) -> Optional[list[str]]:
        return (None if (value := super().__get__(obj, objtype)) is None else
                [self.expand(obj, word) for word in value])


class EnumVar(BaseVar):
    """Convert comma-separated values to an :class:`enum.Enum`."""

    def __init__(self, *args, cls: type[enum.Enum], **kwargs):
        """Initialise the variable.

        Arguments:
            name: Variable name.
            cls: Enumeration type.
            default: Default value.
        """
        assert issubclass(cls, enum.Enum)
        super().__init__(*args, **kwargs)
        self.cls = cls

    def __set__(self, obj: BaseConfig, value: Union[enum.Enum, str]):
        if isinstance(value, enum.Enum):
            super().__set__(obj, value)
        elif isinstance(value, str):  # type: ignore
            for member in self.cls:
                if member.name.casefold() == value.casefold():
                    super().__set__(obj, member)
                    break
            else:
                raise ValueError(f'{value}: no such item')
        else:
            raise TypeError(f'{type(value)}: not an enumeration')


class FilenameVar(BaseVar):
    """Expand ``~user`` and make filenames absolute."""

    def __set__(self, obj: BaseConfig, value: Optional[str]):
        if value is None:
            super().__set__(obj, None)
        if isinstance(value, str):
            super().__set__(obj, path.abspath(path.expanduser(value)))
        raise TypeError('{value}: not a str')


class FlagVar(BaseVar, ListVarMixin):
    """Convert comma-separated values to an :class:`int`."""

    def __init__(self, *args, cls: type[enum.IntEnum], **kwargs):
        assert issubclass(cls, enum.IntEnum)
        super().__init__(*args, **kwargs)
        self.cls = cls

    def __set__(self, obj: BaseConfig, value: Union[str, int, enum.IntEnum]):
        if isinstance(value, (int, enum.IntFlag)):
            super().__set__(obj, value)
        elif isinstance(value, str):  # type: ignore
            flag = 0
            for name in self.splititems(value):
                for member in self.cls:
                    if name.casefold() == member.name.casefold():
                        flag |= member.value
                        break
                else:
                    raise ValueError(f'{name}: no such item')
            super().__set__(obj, flag)
        else:
            raise TypeError(f'{value}: neither an int nor a str')

    cls: type[enum.IntEnum]
    """Enumeration type"""


class HostVar(BaseVar):
    """Check whether value is a valid hostname."""

    def __set__(self, obj: BaseConfig, value: Optional[str]):
        if isinstance(value, str):
            if not (isinetaddr(value) or ishostname(value)):
                raise ValueError(f'{value}: neither hostname nor address')
            super().__set__(obj, value)
        elif value is None:
            super().__set__(obj, value)
        else:
            raise TypeError(f'{value}: not a string')


class NumVar(BaseVar):
    """Convert value to a number of type :attr:`cls`."""

    def __init__(self, *args, cls: type = int,
                 minval: Optional[Union[float, int]] = None,
                 maxval: Optional[Union[float, int]] = None,
                 **kwargs):
        """Initialise the variable.

        Arguments:
            name: Variable name.
            cls: Number type.
            minval: Smallest permissible value.
            maxval: Greatest permissible value.
            default: Default value.
        """
        super().__init__(*args, **kwargs)
        self.cls = cls
        self.minval = minval
        self.maxval = maxval

    def __set__(self, obj: BaseConfig, value: Union[int, float, str]):
        try:
            num = self.cls(value)
        except ValueError as err:
            raise ValueError(f'{value}: not a number') from err
        if self.minval is not None and num < self.minval:
            raise ValueError(f'{value} < {self.minval}')
        if self.maxval is not None and num > self.maxval:
            raise ValueError(f'{value} > {self.maxval}')
        super().__set__(obj, num)

    cls: type
    """Number type."""

    minval: Optional[Union[float, int]]
    """Minimum value."""

    maxval: Optional[Union[float, int]]
    """Maximum value."""


class SASLMechVar(BaseVar, ListVarMixin):
    """Convert SASL mechanism names to :class:`BaseAuth` subclasses."""

    def __set__(self, obj: BaseConfig,
                value: Union[Iterable[type[BaseAuth]], str]):
        if isinstance(value, str):
            classes = AbstractAuth.getmechs(obsolete=True)
            mechs = []
            for name in self.splititems(value.casefold()):
                matches = []
                for cls in classes:
                    if fnmatch.fnmatchcase(cls.name.casefold(), name):
                        if cls in mechs:
                            raise ValueError(f'{cls.name}: duplicate')
                        matches.append(cls)
                if not matches:
                    raise ValueError(f'{name}: no matches')
                mechs.extend(matches)
        elif isinstance(value, Sequence):
            mechs = value     # type: ignore[assignment]
        else:
            raise TypeError(f'{value}: not an SASL mechanism')
        super().__set__(obj, mechs)


class UniqueVar(BaseVar):
    """Variable the value of which must be unique."""

    def __set__(self, obj: BaseConfig, value: str):
        values = self.__class__.values
        if value in values:
            raise ValueError(f'{value}: already in use')
        super().__set__(obj, value)
        values.add(value)

    values: ClassVar[set] = set()


SieveConfigT = TypeVar('SieveConfigT', bound='SieveConfig')


class SieveConfig(BaseConfig):
    """Configuration for the SieveManager command-line client."""

    @classmethod
    def fromfiles(cls: type[SieveConfigT], *fnames: str) -> SieveConfigT:
        """Create a new configuration from `fnames`.

        Arguments:
            fnames: Filenames (default: :data:`CONFIGFILES`)

        Raises:
            FileNotFoundError: A given file could not be found.
        """
        obj = cls()
        for fname in (fnames if fnames else CONFIGFILES):
            try:
                obj.loadfile(fname)
            except FileNotFoundError:
                if fnames:
                    raise
        return obj

    def __init__(self, *args, **kwargs):
        """Create a new configuration.

        Arguments:
            args: Positional arguments used to initialise the back-end.
            kwargs: Keyword arguments used as initial configuration values.
        """
        super().__init__(*args)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def getmanager(self, **variables) -> SieveManager:
        """Open a :class:`SieveManager` connection with this configuration.

        Arguments:
            variables: Configuration variables.

        Raises:
            ShellOperationError: Authentication failed.
            netrc.NetrcParseError: :file:`.netrc` could not be parsed.
        """

        conf = self | self.__class__(**variables)
        mgr = SieveManager(backup=conf.backups, memory=conf.memory)

        # Helper to obtain passwords and passphrases
        def getpass_(passmgr: Optional[list[str]], prompt: str) -> str:
            if passmgr and (pass_ := readoutput(*passmgr, logger=mgr.logger)):
                return pass_
            return askpass(prompt)

        # Logging level
        mgr.logger.setLevel(conf.verbosity)

        # TLS
        sslcontext = mgr.sslcontext
        if (cadir := conf.cadir) or (cafile := conf.cafile):
            sslcontext.load_verify_locations(cafile, cadir)
        if cert := conf.cert:
            def getpassphrase():
                return getpass_(conf.getpassphrase, 'Certificate passphrase: ')
            sslcontext.load_cert_chain(cert, conf.key, getpassphrase)
        if conf.x509strict:
            sslcontext.verify_flags |= ssl.VERIFY_X509_STRICT

        # Connect
        mgr.open(conf.host, port=conf.port, timeout=conf.timeout,
                 tls=conf.tls, ocsp=conf.ocsp)

        # Authenticate
        logauth = conf.verbosity <= LogLevel.AUTH
        if (sasl := [s for s in conf.saslmechs if ExternalAuth in s.__mro__]):
            with suppress(SASLCapabilityError):
                mgr.authenticate(conf.login, owner=conf.owner,
                                 prepare=conf.saslprep, sasl=sasl,
                                 logauth=logauth)
                return mgr
        if (sasl := [s for s in conf.saslmechs if BasePwdAuth in s.__mro__]):
            password = (conf.password if conf.password else
                        getpass_(conf.getpassword, 'Password: '))
            with suppress(SASLCapabilityError):
                mgr.authenticate(conf.login, password, owner=conf.owner,
                                 prepare=conf.saslprep, sasl=sasl,
                                 logauth=logauth)
                return mgr
        raise ShellOperationError('SASL mechanisms exhausted')

    def getshell(self, manager: SieveManager, **variables):
        """Get a configured :class:`SieveShell` that wraps `manager`."""
        conf = self | self.__class__(**variables)
        return SieveShell(manager, clobber=conf.clobber, confirm=conf.confirm)

    def loadfile(self, fname: str):
        """Read configuration from `fname`.

        Raises:
            AppConfigError: Syntax error.
            AppSecurityError: Permissions are insecure.
        """
        super().loadfile(fname)
        mode = os.stat(fname).st_mode
        if mode & 0o22:
            raise AppSecurityError(f'{fname}: is group- or world-writable')
        if mode & 0o44:
            for account in (self, *self._sections.values()):
                if 'password' in account:
                    message = f'{fname}: is group- or world-readable'
                    raise AppSecurityError(message)

    def loadaccount(self, host: str = 'localhost',
                    login: Optional[str] = None):
        """Load the section for `login` on `host`."""
        self |= self.__class__(host=host, login=login)
        hosts = readnetrc(self.netrc)

        # Host
        for name, section in self.sections.items():
            if section.alias == self.host:
                try:
                    self.host = section['host']
                except KeyError:
                    self.host = name.rsplit('@', maxsplit=1)[-1]
                break
        with suppress(KeyError):
            self |= self.sections[self.host]

        # Login
        if not self.login:
            try:
                self.login = hosts[self.host][0]
            except KeyError:
                self.login = getpass.getuser()
        with suppress(KeyError):
            self |= self.sections[f'{self.login}@{self.host}']

        # Password
        if not self.password:
            with suppress(KeyError):
                self.password = hosts[self.host][2]

    alias: UniqueVar = UniqueVar()
    """Alias for a host."""

    backups = NumVar(cls=int, default=0, minval=0)
    """How many backups to keep."""

    cadir = FilenameVar()
    """Custom CA directory."""

    cafile = FilenameVar()
    """Custom CA file."""

    clobber = BoolVar(default=True)
    """Overwrite files?"""

    confirm = FlagVar(default=ShellCmd.ALL, cls=ShellCmd)
    """Which shell commands have to be confirmed?"""

    cert = FilenameVar()
    """Client TLS certificate."""

    getpassphrase = CmdVar()
    """Command that prints the passphrase for the TLS key."""

    getpassword = CmdVar()
    """Command that prints a password."""

    host = HostVar(default='localhost')
    """Host to connect to by default."""

    key = FilenameVar()
    """Client TLS key."""

    login = BaseVar()
    """User to login as (authentication ID)."""

    memory = NumVar(default=524_288, minval=0)
    """How much memory to use for temporary data."""

    netrc: Optional[str] = os.getenv('NETRC')
    """Filename of the .netrc file."""

    ocsp = BoolVar(default=True)
    """Check whether server certificate was revoked?"""

    owner = BaseVar(default='')
    """User whose scripts to manage (authorisation ID)."""

    password = BaseVar()
    """Password to login with."""

    port = NumVar(default=4190, minval=0, maxval=65535)
    """Port to connect to by default."""

    saslmechs = SASLMechVar(default=BasePwdAuth.getmechs())
    """How to authenticate."""

    saslprep = FlagVar(default=SASLPrep.ALL, cls=SASLPrep)
    """Which credentials to prepare."""

    timeout = NumVar(default=socket.getdefaulttimeout(), cls=float, minval=0)
    """Network timeout."""

    tls = BoolVar(default=True)
    """Use TLS?"""

    verbosity = EnumVar(default=LogLevel.INFO, cls=LogLevel)
    """Logging level."""

    x509strict = BoolVar(default=True)
    """Be strict when verifying TLS certificates?"""

    _section = 'account'


#
# Terminal I/O
#

class TermIO(io.TextIOWrapper):
    """I/O for the controlling terminal."""

    def __init__(self, *args, **kwargs):
        """Open the controlling terminal."""
        super().__init__(io.FileIO('/dev/tty', 'r+'), *args, **kwargs)


#
# Logging
#

LogIOWrapperT = TypeVar('LogIOWrapperT', bound='LogIOWrapper')
"""Type variable for :class:`LogIOWrapper`."""


class LogIOWrapper():
    """Logger for file-like objects."""

    @classmethod
    def wrap(cls: type[LogIOWrapperT],
             file: Union[BinaryIO, io.BufferedRWPair],
             logger: logging.Logger = logging.getLogger(__name__),
             level: int = logging.DEBUG,
             formats: tuple[str, str] = ('S: %s', 'C: %s'),
             encoding: str = 'utf8') \
                -> Union[BinaryIO, io.BufferedRWPair, LogIOWrapperT]:
        """Wrap a file in a :class:`LogIOWrapper` if logging is enabled.

        Takes the same arguments as :meth:`__init__`.

        Returns:
            The file or a :class:`LogIOWrapper` that wraps the file.
        """
        if logger.isEnabledFor(level):
            return cls(file, encoding, level, logger, formats)
        return file

    def __init__(self, file: Union[BinaryIO, io.BufferedRWPair],
                 encoding: str = 'utf8', level: int = logging.DEBUG,
                 logger: logging.Logger = logging.getLogger(__name__),
                 formats: tuple[str, str] = ('S: %s', 'C: %s')):
        """Log I/O to `file`.

        Arguments:
            file: File-like object opened in binary mode.
            encoding: `file`'s encoding.
            level: Logging priority.
            logger: Logger.
            formats: Message formats; '%s' is replaced with I/O.
        """
        splitlines = re.compile(rb'\r?\n').split
        buffers = (bytearray(), bytearray())

        def extv(buf: bytearray, vec: Iterable[Iterable[int]]) -> None:
            for elem in vec:
                buf.extend(elem)

        def getdecorator(
                buf: bytearray, fmt: str, arg=None,
                ext: Callable[[bytearray, Iterable], None] = bytearray.extend
                ) -> Callable[[Callable[..., T]], Callable[..., T]]:
            def decorator(func: Callable[..., T]) -> Callable[..., T]:
                def wrapper(*args, **kwargs) -> T:
                    retval = func(*args, **kwargs)
                    if not self.quiet:
                        data = retval if arg is None else args[arg]
                        ext(buf, data)  # type: ignore[reportArgumentType]
                        ptr: Union[bytes, bytearray] = buf
                        while True:
                            try:
                                line, ptr = splitlines(ptr, maxsplit=1)
                            except ValueError:
                                break
                            self.log(line, fmt)
                        buf[:] = ptr
                    return retval
                return wrapper
            return decorator

        logread = getdecorator(buffers[0], formats[0])
        logreadinto = getdecorator(buffers[0], formats[0], arg=0)
        logreadv = getdecorator(buffers[0], formats[0], ext=extv)
        logwrite = getdecorator(buffers[1], formats[1], arg=0)
        logwritev = getdecorator(buffers[1], formats[1], arg=0, ext=extv)

        self.read = logread(file.read)
        self.readline = logread(file.readline)
        self.readlines = logreadv(file.readlines)
        self.write = logwrite(file.write)
        self.writelines = logwritev(file.writelines)

        if isinstance(file, io.RawIOBase):
            self.readall = logread(file.readall)
            self.readinto = logreadinto(file.readinto)  # type: ignore

        if isinstance(file, io.BufferedIOBase):
            self.read1 = logread(file.read1)
            self.readinto1 = logread(file.readinto1)
            self.readinto = logreadinto(file.readinto)

        self.buffers = buffers
        self.encoding = encoding
        self.formats = formats
        self.file = file
        self.level = level
        self.logger = logger

    def __del__(self):
        file = self.file
        if not file.closed:
            file.flush()
            file.close()
        if not self.quiet:
            for buf, fmt in zip(self.buffers, self.formats):
                if buf:
                    self.log(buf, fmt)

    def __getattr__(self, name):
        return getattr(self.file, name)

    def __iter__(self):
        return self

    def __next__(self):
        if line := self.readline():
            return line
        raise StopIteration()

    def log(self, line: Union[bytearray, bytes], fmt: str):
        """Log `line` with `fmt`."""
        decoded = escapectrl(line.rstrip(b'\r\n').decode(self.encoding))
        self.logger.log(self.level, fmt, decoded)

    buffers: tuple[bytearray, bytearray]
    """Logging buffers."""

    encoding: str
    """:attr:`file`'s encoding."""

    file: Union[BinaryIO, io.BufferedRWPair]
    """Underlying file-like object."""

    formats: tuple[str, str]
    """Logging formats."""

    level: int
    """Logging level."""

    logger: logging.Logger
    """Logger."""

    quiet: bool = False
    """Log I/O?"""

    read: Callable[..., bytes]
    """Read from :attr:`file`."""

    readinto: Callable[..., int]
    """Read from :attr:`file` into a buffer."""

    readline: Callable[..., bytes]
    """Read a line from :attr:`file`."""

    readlines: Callable[..., list[bytes]]
    """Read all lines from :attr:`file`."""

    write: Callable[..., int]
    """Write to :attr:`file`."""

    writelines: Callable[..., None]
    """Write lines to :attr:`file`."""


#
# Signal handling
#

SignalHandlingFunc = Callable[[int, Union[types.FrameType, None]], Any]
"""Alias for signal handling functions."""


SignalHandler = Union[SignalHandlingFunc, int, None]
"""Alias for signal handlers."""


@dataclass(frozen=True)
class SignalCaught(Exception):
    """Signal was caught."""

    @classmethod
    def throw(cls, signo: int, frame: Optional[types.FrameType]):
        """Raise a :exc:`SignalCaught` exception."""
        raise cls(signo, frame)

    @classmethod
    def register(cls, signals: Iterable[int]) -> tuple[SignalHandler, ...]:
        """Register :meth:`throw` as handler for the given `signals`.

        Arguments:
            signals: Signals to register :meth:`throw` as handler for.

        Returns:
            Old signal handlers.
        """
        return tuple(signal.signal(s, cls.throw) for s in signals)

    @classmethod
    def catch(cls, *signals: int) -> \
            Callable[[Callable[..., T]], Callable[..., T]]:
        """Decorator that :meth:`handles <handle>` `signals`.

        If one of the given `signals` is caught, :exc:`SignalCaught` is raised.
        If that exception is not caught, the process group is terminated,
        the signal handler reset, and the signal re-raised.
        """
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            # pylint: disable=inconsistent-return-statements
            def wrapper(*args, **kwargs) -> T:  # type: ignore[return]
                handlers = cls.register(signals)
                try:
                    return func(*args, **kwargs)
                except cls as exc:
                    logging.critical(exc)
                    signal.signal(SIGTERM, SIG_IGN)
                    os.killpg(os.getpgrp(), SIGTERM)
                    signal.signal(exc.signo, SIG_DFL)
                    signal.raise_signal(exc.signo)
                finally:
                    for signo, handler in zip(signals, handlers):
                        signal.signal(signo, handler)
                # NOTREACHED
            for name in dir(func):
                with suppress(AttributeError, TypeError, ValueError):
                    setattr(wrapper, name, getattr(func, name))
            return wrapper
        return decorator

    def __str__(self):
        desc = signal.strsignal(self.signo)
        return desc.split(':')[0] if desc else f'caught signal {self.signo}'

    signo: int
    """Signal number."""

    frame: Optional[types.FrameType] = None
    """Stack frame."""


#
# Errors
#

# Error types
class Error(Exception):
    """Base class for errors."""


class CapabilityError(Error):
    """Base class for capability errors."""


class ConfigError(Error):
    """Base class for configuration errors."""


class DataError(Error):
    """Base class for data errors."""


class OperationError(Error):
    """Base class for operation errors."""


class ProtocolError(Error):
    """Base class for protocol errors.

    .. danger::
        Continuing after a :exc:`ProtocolError` may cause undefined behaviour.
    """


class SecurityError(Error):
    """Base class for security errors.

    .. danger::
        Continuing after a :exc:`SecurityError` compromises the connection.
    """


class SoftwareError(Error):
    """Base class for software errors."""


class UsageError(Error):
    """Base class for usage errors."""


# Client errors
class AppError(Error):
    """Base class for application errors."""


class AppConfigError(AppError, ConfigError):
    """Applicaiton configuration error."""


class AppConnectionError(AppError, ConnectionError):
    """Client-side connection error."""


class AppOperationError(AppError, OperationError):
    """Client-side operation error."""


class AppSecurityError(AppError, SecurityError):
    """Client security error."""


class AppSoftwareError(AppError, SoftwareError):
    """Client software error (aka a bug)."""


# DNS errors
class DNSError(Error):
    """Base class for DNS errors."""


class DNSDataError(Error):
    """DNS data error."""


class DNSOperationError(DNSError, OperationError):
    """DNS operation error."""


class DNSSoftwareError(DNSError, SoftwareError):
    """DNS software error."""


# HTTP errors
class HTTPError(Error):
    """Base class for HTTP errors."""


class HTTPOperationError(HTTPError, OperationError):
    """HTTP operation error."""


class HTTPUsageError(HTTPError, ProtocolError):
    """HTTP usage error."""


# OCSP errors
class OCSPError(Error):
    """Base class for OCSP errors."""


class OCSPDataError(OCSPError, DataError):
    """OCSP data error."""


class OCSPOperationError(OCSPError, OperationError):
    """OCSP operation error."""


# SASL errors
class SASLError(Error):
    """Base class for SASL errors."""


class SASLCapabilityError(Error):
    """SASL capability error."""


class SASLProtocolError(SASLError, ProtocolError):
    """Server violated the SASL protocol."""


class SASLSecurityError(SASLError, SecurityError):
    """SASL security error."""


# Shell errors
class ShellError(Error):
    """Base class for shell errors."""


class ShellOperationError(ShellError, OperationError):
    """Shell operation error."""


class ShellUsageError(ShellError, UsageError):
    """Shell usage error."""


# ManageSieve errors
class SieveError(Error):
    """Base class for ManageSieve errors."""


class SieveCapabilityError(SieveError, CapabilityError):
    """Capability not supported by the server."""


class SieveConnectionError(Response, SieveError, ConnectionError):
    """Server said "BYE"."""

    # pylint: disable=redefined-outer-name
    def __init__(self, response: Atom = Atom('BYE'),
                 code: tuple[Word, ...] = (),
                 message: Optional[str] = None):
        super().__init__(response=response, code=code, message=message)


class SieveOperationError(Response, SieveError, OperationError):
    """Server said "NO"."""

    # pylint: disable=redefined-outer-name
    def __init__(self, response: Atom = Atom('NO'),
                 code: tuple[Word, ...] = (),
                 message: Optional[str] = None):
        super().__init__(response=response, code=code, message=message)


class SieveProtocolError(SieveError, ProtocolError):
    """Server violated the ManageSieve protocol error."""


# TLS errors
class TLSError(Error):
    """Base class for TLS errors."""


class TLSCapabilityError(TLSError, CapabilityError):
    """TLS capability error."""


class TLSSecurityError(TLSError, OperationError):
    """TLS security error."""


class TLSSoftwareError(TLSError, SoftwareError):
    """TLS software error."""


#
# Helpers
#

def askpass(prompt: str) -> str:
    """Prompt for a password on the controlling terminal."""
    with TermIO() as tty:
        return getpass.getpass(prompt, stream=tty)


def backup(file: str, keep: int, getfiles: Callable[[], Iterable[str]],
           copy: Callable[[str, str], Any], remove: Callable[[str], Any]):
    """Make an Emacs-style backup of `file`.

    `keep` = 1
        :file:`file` is backed up as :file:`file~`.

    `keep` > 1
        :file:`file` is backed up as :file:`file.~{n}~`, where
        `n` starts with 1 and increments with each backup.

    Arguments:
        file: File to back up.
        keep: How many copies to keep.
        copy: Function that copies the file.
        getfiles: Function that returns a list of files.
        remove: Function that removes a file.

    Raises:
        ValueError: `keep` is < 0.
    """
    if keep < 0:
        raise ValueError('keep: must be >= 0')
    if keep == 0:
        return
    if keep == 1:
        copy(file, file + '~')
    else:
        backupexpr = re.escape(file) + r'\.~(\d+)~'
        matchbackup = re.compile(backupexpr).fullmatch
        backups = sorted((int(match.group(1)), file) for file in getfiles()
                         if (match := matchbackup(file)))
        for _, bak in backups[:-(keep - 1)]:
            remove(bak)
        counter = backups[-1][0] + 1 if backups else 1
        copy(file, f'{file}.~{counter}~')


def bell():
    """Print a BEL to the controlling terminal, if there is one."""
    try:
        with TermIO() as tty:
            print('\a', end='', file=tty)
    except FileNotFoundError:
        pass


def certrevoked(cert, logger: logging.Logger = logging.getLogger(__name__)) \
        -> bool:
    """Check if `cert` has been revoked.

    Raises:
        OCSPDataError: `cert` contains no authority information.
        OCSPOperationError: no authoritative response.

    .. seealso::
        :rfc:`5019`
            Lightweight OCSP Profile
        :rfc:`6960`
            Online Certificate Status Protocol (OCSP)
    """
    try:
        issuers, responders = getcertauthinfo(cert)
    except ExtensionNotFound as err:
        raise OCSPDataError('no authority information') from err
    for caurl in issuers:
        try:
            der = httpget(caurl)
        except (urllib.error.URLError, HTTPError) as err:
            logger.error(err)
            continue
        ca = x509.load_der_x509_certificate(der)
        builder = ocsp.OCSPRequestBuilder()
        # SHA1 is mandated by RFC 5019.
        req = builder.add_certificate(cert, ca, SHA1()).build()  # nosec B303
        # pylint: disable=redefined-outer-name
        path = b64encode(req.public_bytes(Encoding.DER)).decode('ascii')
        for responder in responders:
            statusurl = urllib.parse.urljoin(responder, path)
            try:
                res = ocsp.load_der_ocsp_response(httpget(statusurl))
            except HTTPError as err:
                logger.error(err)
                continue
            if res.response_status == OCSPResponseStatus.SUCCESSFUL:
                try:
                    now = datetime.datetime.now(tz=datetime.UTC)  # novermin
                    end = res.next_update_utc       # type: ignore
                    if now < res.this_update_utc:   # type: ignore
                        continue
                    if end is not None and now >= end:
                        continue
                except AttributeError:
                    now = datetime.datetime.now()
                    if now < res.this_update:
                        continue
                    if (end := res.next_update) is not None and now >= end:
                        continue
                if res.certificate_status == OCSPCertStatus.REVOKED:
                    return True
                if res.certificate_status == OCSPCertStatus.GOOD:
                    return False
    raise OCSPOperationError('no authoritative OCSP response')


def escapectrl(chars: str) -> str:
    """Escape control characters."""
    categories = map(unicodedata.category, chars)
    escaped = [fr'\u{ord(char):04x}' if cat.startswith('C') else char
               for char, cat in zip(chars, categories)]
    return ''.join(escaped)


def httpget(url: str) -> bytes:
    """Download a file from `url` using HTTP.

    Raises:
        HTTPUsageError: `url` is not an HTTP URL.
        HTTPOperationError: "GET" failed.
    """
    while True:
        if not url.startswith('http://'):
            raise HTTPUsageError(f'{url}: not an HTTP URL')
        with urllib.request.urlopen(url) as res:  # nosec B310
            if res.status == 200:
                return res.read()
            if res.status in (301, 302, 303, 307, 308):
                if url := res.getheader('Location'):
                    continue
        raise HTTPOperationError(f'GET {url}: {res.reason}')
    # NOTREACHED


def getcertauthinfo(cert) -> tuple[list[str], list[str]]:
    """Get information about the authority that issued `cert`.

    Returns:
        CA issuer URLs and OCSP responder base URLs.
    """
    exts = cert.extensions.get_extension_for_class(AuthorityInformationAccess)
    issuers = []
    responders = []
    for field in exts.value:
        oid = field.access_method
        if oid == AuthorityInformationAccessOID.CA_ISSUERS:
            issuers.append(field.access_location.value)
        elif oid == AuthorityInformationAccessOID.OCSP:
            responders.append(field.access_location.value)
    return issuers, responders


def getfilesize(file: IO) -> int:
    """Get the size of file-like object relative to the current position."""
    try:
        pos = file.tell()
    except io.UnsupportedOperation:
        pos = 0
    try:
        size = os.fstat(file.fileno()).st_size - pos
    except io.UnsupportedOperation:
        size = file.seek(0, SEEK_END) - pos
        file.seek(pos, SEEK_SET)
    return size


def isdnsname(name: str) -> bool:
    """Check whether `name` is a valid DNS name.

    .. seealso::
        :rfc:`1035` (sec. 2.3.1)
            Domain names - Preferred name syntax
        :rfc:`2181` (sec. 11)
            Clarifications to the DNS Specification - Name syntax
    """
    return (all(0 < len(x) <= 63 for x in name.removesuffix('.').split('.'))
            and len(name) <= 253)


def ishostname(name: str) -> bool:
    """Check whether `name` is a valid hostname.

    .. seealso::
        :rfc:`921`
            Domain Name System Implementation Schedule
        :rfc:`952`
            Internet host table specification
        :rfc:`1123` (sec. 2.1)
            Host Names and Numbers
    """
    return (bool(re.fullmatch(r'((?!-)[a-z0-9-]+(?<!-)\.?)+', name, re.I))
            and isdnsname(name))


def isinetaddr(addr: str) -> bool:
    """Check whether `addr` is an internet address."""
    try:
        ipaddress.ip_address(addr)
    except ValueError:
        return False
    return True


def nwise(iterable: Iterable, n: Any) -> Iterator[tuple]:
    """Iterate over n-tuples."""
    iterator = iter(iterable)
    ntuple = deque(itertools.islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        ntuple.append(x)
        yield tuple(ntuple)


def randomise(elems: Sequence[T], weights: Iterable[int]) -> list[T]:
    """Randomise the order of `elems`."""
    nelems = len(elems)
    weights = list(weights)
    indices = list(range(len(elems)))
    randomised = []
    for _ in range(nelems):
        i, = random.choices(indices, weights, k=1)  # noqa DUO102 # nosec B311
        randomised.append(elems[i])
        weights[i] = 0
    return randomised


def readdir(dirname: str, predicate: Optional[Callable[[str], bool]] = None) \
        -> Iterator[str]:
    """Get every filename in `dirname` that matches `predicate`."""
    for dirent in os.listdir(dirname if dirname else '.'):
        fname = path.join(dirname, dirent)
        if predicate is None or predicate(fname):
            yield fname


def readnetrc(fname: Optional[str]) -> dict[str, tuple[str, str, str]]:
    """Read a .netrc file.

    Arguments:
        fname: Filename (default: :file:`~/.netrc`)

    Returns:
        Mapping from hosts to login-account-password 3-tuples.

    Raises:
        FileNotFoundError: `fname` was given but not found.
        netrc.NetrcParseError: Syntax error.
    """
    try:
        if fname:
            return netrc.netrc(fname).hosts
        with suppress(FileNotFoundError):
            return netrc.netrc().hosts
    except netrc.NetrcParseError as err:
        if sys.version_info < (3, 10):
            logging.error(err)
        else:
            raise
    return {}


def readoutput(*command: str, encoding: str = ENCODING,
               logger: logging.Logger = logging.getLogger(__name__)) -> str:
    """Decode and return the output of `command`.

    Returns:
        Decoded output or, if `command` exited with a non-zero status,
        the empty string.

    Raises:
        subprocess.CalledProcessError: `command` exited with a status >= 127.
    """
    logger.debug('exec: %s', ' '.join(command))
    try:
        cp = subprocess.run(command, capture_output=True, check=True)
    except subprocess.CalledProcessError as err:
        if err.returncode >= 127:
            raise
        logger.debug('%s exited with status %d', command[0], err.returncode)
        return ''
    return cp.stdout.rstrip().decode(encoding)


# pylint: disable=redundant-returns-doc
def resolvesrv(host: str) -> Iterator[SRV]:
    """Resolve a DNS SRV record.

    Arguments:
        host: Hostname (e.g., :samp:`_sieve._tcp.imap.foo.example`)

    Returns:
        An iterator over `SRV` records sorted by their priority
        and randomised according to their weight.

    Raises:
        DNSDataError: `host` is not a valid DNS name.
        DNSOperationError: Lookup error.
        DNSSoftwareError: dnspython_ is not available.

    .. note::
        Requires dnspython_.
    """
    if not HAVE_DNSPYTHON:
        raise DNSSoftwareError('dnspython unavailable')
    if not isdnsname(host):
        raise DNSDataError('hostname or label is too long')
    try:
        answer = dns.resolver.resolve(host, 'SRV')
        hosts: dict[str, list] = defaultdict(list)
        byprio: dict[int, list[SRV]] = defaultdict(list)
        for rec in answer.response.additional:
            name = rec.name.to_text()
            addrs = [i.address for i in rec.items
                     if i.rdtype == dns.rdatatype.A]
            hosts[name].extend(addrs)
        for rec in answer:                  # type: ignore
            name = rec.target.to_text()     # type: ignore
            priority = rec.priority         # type: ignore
            weight = rec.weight             # type: ignore
            port = rec.port                 # type: ignore
            if addrs := hosts.get(name):    # type: ignore
                srvs = [SRV(priority, weight, a, port) for a in addrs]
                byprio[priority].extend(srvs)
            else:
                srv = SRV(priority, weight, name.rstrip('.'), port)
                byprio[priority].append(srv)
        for prio in sorted(byprio.keys()):
            srvs = byprio[prio]
            weights = [s.weight for s in srvs]
            if sum(weights) > 0:
                yield from randomise(srvs, weights)
            else:
                yield from srvs
    except DNSException as err:
        raise DNSOperationError(str(err)) from err


def yamlescape(data: str):
    """Strip and quote `data` for use as YAML scalar if needed."""
    indicators = ('-', '?', ':', ',', '[', ']', '{', '}', '#', '&',
                  '*', '!', '|', '>', "'", '"', '%', '@', '`')
    data = data.strip()
    if not data:
        return '""'
    if data.casefold() == 'no':
        return '"' + data + '"'
    if data[0] in indicators or ': ' in data or ' #' in data:
        return '"' + data.replace('\\', '\\\\').replace('"', '\\\"') + '"'
    return data


#
# Main
#

# pylint: disable=too-many-branches, too-many-statements
@SignalCaught.catch(SIGHUP, SIGINT, SIGTERM)
def main() -> NoReturn:
    """sievemgr - manage remote Sieve scripts

    Usage:  sievemgr [server] [command] [argument ...]
            sievemgr -e expression [...] [server]
            sievemgr -s file [server]

    Options:
        -C             Do not overwrite existing files.
        -c file        Read configuration from file.
        -d             Enable debugging mode.
        -e expression  Execute expression on the server.
        -f             Overwrite and remove files without confirmation.
        -i             Confirm removing or overwriting files.
        -o key=value   Set configuration key to value.
        -q             Be quieter.
        -s file        Execute expressions read from file.
        -v             Be more verbose.

        -e, -o, -q, and -v can be given multiple times.
        See sievemgr(1) for the complete list.

    Report bugs to: <https://github.com/odkr/sievemgr/issues>
    Home page: <https://odkr.codeberg.page/sievemgr>
    """
    progname = os.path.basename(sys.argv[0])
    logging.basicConfig(format=f'{progname}: %(message)s')

    # Options
    try:
        opts, args = getopt(sys.argv[1:], 'CN:Vc:de:fhio:qs:v',
                            ['help', 'version'])
    except GetoptError as err:
        error('%s', err, status=2)

    optconf = SieveConfig()
    debug = False
    exprs: list[str] = []
    configfiles: list[str] = []
    script: Optional[TextIO] = None
    volume = 0
    for opt, arg in opts:
        try:
            if opt in ('-h', '--help'):
                showhelp(main)
            elif opt in ('-V', '--version'):
                showversion()
            elif opt == '-C':
                optconf.clobber = False
            elif opt == '-N':
                optconf.netrc = arg
            elif opt == '-c':
                configfiles.append(arg)
            elif opt == '-d':
                optconf.verbosity = LogLevel.DEBUG
            elif opt == '-e':
                exprs.append(arg)
            elif opt == '-f':
                optconf.confirm = ShellCmd.NONE
            elif opt == '-i':
                optconf.confirm = ShellCmd.ALL
            elif opt == '-o':
                optconf.parse(arg)
            elif opt == '-q':
                volume -= 1
            elif opt == '-s':
                # pylint: disable=consider-using-with
                script = open(arg)
            elif opt == '-v':
                volume += 1
        except (AttributeError, TypeError, ValueError) as err:
            error('option %s: %s', opt, err, status=2)

    # Arguments
    url = URL.fromstr(args.pop(0)) if args else None
    command = args.pop(0) if args else ''

    if script:
        if command:
            error('-s cannot be used together with a command', status=2)
        if exprs:
            error('-e and -s cannot be combined', status=2)

    # Configuration
    try:
        conf = SieveConfig().fromfiles(*configfiles) | optconf
    except FileNotFoundError as err:
        error('%s: %s', err.filename, os.strerror(err.errno))
    except (ConfigError, SecurityError) as err:
        error('%s', err)
    conf.loadaccount(host=url.hostname if url else conf.host,
                     login=url.username if url else None)
    conf |= optconf

    if url:
        if url.username:
            conf.login = url.username
        if url.password:
            conf.password = url.password
        if url.owner:
            conf.owner = url.owner

    # Logging
    conf.verbosity = conf.verbosity.fromdelta(volume)
    logger = logging.getLogger()
    logger.setLevel(conf.verbosity)

    # Infos
    for line in ABOUT.strip().splitlines():
        logging.info('%s', line)

    # Shell
    try:
        with conf.getmanager() as mgr:
            shell = conf.getshell(mgr)
            if exprs:
                for expr in exprs:
                    shell.executeline(expr)
            elif script:
                shell.executescript(script)
            elif command:
                shell.execute(command, *args)
            else:
                shell.enter()
    except (socket.herror, socket.gaierror, ConnectionError) as err:
        error('%s', err.args[1])
    except (MemoryError, ssl.SSLError) as err:
        error('%s', err)
    except OSError as err:
        error('%s', os.strerror(err.errno) if err.errno else err)
    except subprocess.CalledProcessError as err:
        error('%s exited with status %d', err.cmd[0], err.returncode)
    except Error as err:
        if debug:
            raise
        error('%s', err)
    sys.exit(shell.retval)


def error(*args, status: int = 1, **kwargs) -> NoReturn:
    """Log an err and :func:`exit <sys.exit>` with `status`.

    Arguments:
        args: Positional arguments for :func:`logging.error`.
        status: Exit status.
        kwargs: Keyword arguments for :func:`logging.error`.
    """
    logging.error(*args, **kwargs)
    sys.exit(status)


def showhelp(func: Callable) -> NoReturn:
    """Print the docstring of `func` and :func:`exit <sys.exit>`."""
    assert func.__doc__
    lines = func.__doc__.splitlines()
    indented = re.compile(r'\s+').match
    prefix = os.path.commonprefix(list(filter(indented, lines)))
    for line in lines[:-1]:
        print(line.removeprefix(prefix))
    sys.exit()


def showversion() -> NoReturn:
    """Print :attr:`ABOUT` and :func:`exit <sys.exit>`."""
    print(ABOUT.strip())
    sys.exit()


#
# Boilerplate
#

logging.getLogger(__name__).addHandler(logging.NullHandler())

if __name__ == '__main__':
    main()
