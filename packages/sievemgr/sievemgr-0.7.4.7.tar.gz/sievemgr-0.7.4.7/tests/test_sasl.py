#!/usr/bin/env python3
"""Tests for :class:`sievemgr.BaseAuth`."""

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

# pylint: disable=missing-class-docstring, missing-function-docstring


#
# Modules
#

import os
import pathlib
import sys
import unittest

from typing import Final, Iterator, TypeVar, Union
from unicodedata import normalize

sys.path.append(os.path.realpath(pathlib.Path(__file__).parents[1]))

from sievemgr import BaseAuth
from . import Test, makerunner


#
# Types
#

T = TypeVar('T')


#
# Helpers
#

def mapchars(first: int, last: int, obj: Union[T, type[Exception]]) \
        -> Iterator[Test[T]]:
    for i in range(first, last + 1):
        yield ((chr(i),), obj)


#
# Globals
#

USERNAMES: set[str] = {
    normalize(form, user)   # type: ignore[arg-type]
    for user in (
        '0123', 'user', 'UserName', 'user_name', 'tim',
        'user@localhost', 'user@foo.example', 'user@xn--bcher-kva.example',
        'فلان', 'فلانة', 'فلان الفلاني', 'فلانة الفلانية', 'علان',
        'ܐܸܢܵܐ', 'ܦܠܵܢ', 'ܦܠܵܢܝܼܬ݂ܵܐ',
        'ইয়ে', 'অমুক', 'ফলনা', 'ফলানা',
        'Иван', 'Драган', 'Петкан',
        '陳大文', '陳小明', '路人甲', 'Chris Wong',
        'mikälie',
        'Γιάννης Παπαδόπουλος',
        'מה-שמו', 'משה', 'יוֹסִי', 'כהן', 'ישראל ישראלי', 'ישראלה ישראלי',
        'פלוני', 'אלמוני', 'פלוני אלמוני', 'ראובן', 'שמעון',
        'Jón Jónsson', 'Jóna Jónsdóttir',
        '홍길동', '아무개', '철수', '영희', '某人',
        '李某', '张三', '張三', '李四', '王五',
        'فلانی', 'طرف', 'يارو',
        'такой-то', 'имярек', 'Пётр', 'Сидор',
        'Иван Петрович Сидоров', 'Вася Пупкин', 'Василий Пупкин',
        'Petar Petrović', 'Pera Perić',
        'askurđel',
        'Sarı Çizmeli Mehmet Ağa',
        'невідомий',
        'Nguyễn Văn A', 'Nguyễn Thị A'
    )
    for form in ('NFC', 'NFKC', 'NFD', 'NFKD')
}


STRINGS: Final[tuple[Test[str], ...]] = (
    # Simple tests
    (('',), ''),
    (('foo',), 'foo'),
    (('\n',), ValueError),
    (('\r',), ValueError),
    (('\0',), ValueError),

    # Edge cases
    ((' ',), ' '),
    (('  ',), '  '),
    (('0',), '0'),
    (('00',), '00'),

    # Usernames
    *[((u,), normalize('NFC', u)) for u in USERNAMES],

    # Unassigned code points
    ((chr(0x0221),), ValueError),
    *mapchars(0x0234, 0x024f, ValueError),
    *mapchars(0x02ae, 0x02af, ValueError),
    *mapchars(0x02ef, 0x02ff, ValueError),
    *mapchars(0x0350, 0x035f, ValueError),
    *mapchars(0x0370, 0x0373, ValueError),
    *mapchars(0x0376, 0x0379, ValueError),
    *mapchars(0x037b, 0x037d, ValueError),
    *mapchars(0x037f, 0x0383, ValueError),
    ((chr(0x038b),), ValueError),
    ((chr(0x038d),), ValueError),
    ((chr(0x03a2),), ValueError),
    ((chr(0x03cf),), ValueError),
    *mapchars(0x03f7, 0x03ff, ValueError),
    ((chr(0x0487),), ValueError),
    ((chr(0x04cf),), ValueError),
    *mapchars(0x04f6, 0x04f7, ValueError),
    *mapchars(0x04fa, 0x04ff, ValueError),
    *mapchars(0x0510, 0x0530, ValueError),
    *mapchars(0x0557, 0x0558, ValueError),
    ((chr(0x0560),), ValueError),
    ((chr(0x0588),), ValueError),
    *mapchars(0x058b, 0x0590, ValueError),
    ((chr(0x05a2),), ValueError),
    ((chr(0x05ba),), ValueError),
    *mapchars(0x05c5, 0x05cf, ValueError),
    *mapchars(0x05eb, 0x05ef, ValueError),
    *mapchars(0x05f5, 0x060b, ValueError),
    *mapchars(0x060d, 0x061a, ValueError),
    *mapchars(0x061c, 0x061e, ValueError),
    ((chr(0x0620),), ValueError),
    *mapchars(0x063b, 0x063f, ValueError),
    *mapchars(0x0656, 0x065f, ValueError),
    *mapchars(0x06ee, 0x06ef, ValueError),
    ((chr(0x06ff),), ValueError),
    ((chr(0x070e),), ValueError),
    *mapchars(0x072d, 0x072f, ValueError),
    *mapchars(0x074b, 0x077f, ValueError),
    *mapchars(0x07b2, 0x0900, ValueError),
    ((chr(0x0904),), ValueError),
    *mapchars(0x093a, 0x093b, ValueError),
    *mapchars(0x094e, 0x094f, ValueError),
    *mapchars(0x0955, 0x0957, ValueError),
    *mapchars(0x0971, 0x0980, ValueError),
    ((chr(0x0984),), ValueError),
    *mapchars(0x098d, 0x098e, ValueError),
    *mapchars(0x0991, 0x0992, ValueError),
    ((chr(0x09a9),), ValueError),
    ((chr(0x09b1),), ValueError),
    *mapchars(0x09b3, 0x09b5, ValueError),
    *mapchars(0x09ba, 0x09bb, ValueError),
    ((chr(0x09bd),), ValueError),
    *mapchars(0x09c5, 0x09c6, ValueError),
    *mapchars(0x09c9, 0x09ca, ValueError),
    *mapchars(0x09ce, 0x09d6, ValueError),
    *mapchars(0x09d8, 0x09db, ValueError),
    ((chr(0x09de),), ValueError),
    *mapchars(0x09e4, 0x09e5, ValueError),
    *mapchars(0x09fb, 0x0a01, ValueError),
    *mapchars(0x0a03, 0x0a04, ValueError),
    *mapchars(0x0a0b, 0x0a0e, ValueError),
    *mapchars(0x0a11, 0x0a12, ValueError),
    ((chr(0x0a29),), ValueError),
    ((chr(0x0a31),), ValueError),
    ((chr(0x0a34),), ValueError),
    ((chr(0x0a37),), ValueError),
    *mapchars(0x0a3a, 0x0a3b, ValueError),
    ((chr(0x0a3d),), ValueError),
    *mapchars(0x0a43, 0x0a46, ValueError),
    *mapchars(0x0a49, 0x0a4a, ValueError),
    *mapchars(0x0a4e, 0x0a58, ValueError),
    ((chr(0x0a5d),), ValueError),
    *mapchars(0x0a5f, 0x0a65, ValueError),
    *mapchars(0x0a75, 0x0a80, ValueError),
    ((chr(0x0a84),), ValueError),
    ((chr(0x0a8c),), ValueError),
    ((chr(0x0a8e),), ValueError),
    ((chr(0x0a92),), ValueError),
    ((chr(0x0aa9),), ValueError),
    ((chr(0x0ab1),), ValueError),
    ((chr(0x0ab4),), ValueError),
    *mapchars(0x0aba, 0x0abb, ValueError),
    ((chr(0x0ac6),), ValueError),
    ((chr(0x0aca),), ValueError),
    *mapchars(0x0ace, 0x0acf, ValueError),
    *mapchars(0x0ad1, 0x0adf, ValueError),
    *mapchars(0x0ae1, 0x0ae5, ValueError),
    *mapchars(0x0af0, 0x0b00, ValueError),
    ((chr(0x0b04),), ValueError),
    *mapchars(0x0b0d, 0x0b0e, ValueError),
    *mapchars(0x0b11, 0x0b12, ValueError),
    ((chr(0x0b29),), ValueError),
    ((chr(0x0b31),), ValueError),
    *mapchars(0x0b34, 0x0b35, ValueError),
    *mapchars(0x0b3a, 0x0b3b, ValueError),
    *mapchars(0x0b44, 0x0b46, ValueError),
    *mapchars(0x0b49, 0x0b4a, ValueError),
    *mapchars(0x0b4e, 0x0b55, ValueError),
    *mapchars(0x0b58, 0x0b5b, ValueError),
    ((chr(0x0b5e),), ValueError),
    *mapchars(0x0b62, 0x0b65, ValueError),
    *mapchars(0x0b71, 0x0b81, ValueError),
    ((chr(0x0b84),), ValueError),
    *mapchars(0x0b8b, 0x0b8d, ValueError),
    ((chr(0x0b91),), ValueError),
    *mapchars(0x0b96, 0x0b98, ValueError),
    ((chr(0x0b9b),), ValueError),
    ((chr(0x0b9d),), ValueError),
    *mapchars(0x0ba0, 0x0ba2, ValueError),
    *mapchars(0x0ba5, 0x0ba7, ValueError),
    *mapchars(0x0bab, 0x0bad, ValueError),
    ((chr(0x0bb6),), ValueError),
    *mapchars(0x0bba, 0x0bbd, ValueError),
    *mapchars(0x0bc3, 0x0bc5, ValueError),
    ((chr(0x0bc9),), ValueError),
    *mapchars(0x0bce, 0x0bd6, ValueError),
    *mapchars(0x0bd8, 0x0be6, ValueError),
    *mapchars(0x0bf3, 0x0c00, ValueError),
    ((chr(0x0c04),), ValueError),
    ((chr(0x0c0d),), ValueError),
    ((chr(0x0c11),), ValueError),
    ((chr(0x0c29),), ValueError),
    ((chr(0x0c34),), ValueError),
    *mapchars(0x0c3a, 0x0c3d, ValueError),
    ((chr(0x0c45),), ValueError),
    ((chr(0x0c49),), ValueError),
    *mapchars(0x0c4e, 0x0c54, ValueError),
    *mapchars(0x0c57, 0x0c5f, ValueError),
    *mapchars(0x0c62, 0x0c65, ValueError),
    *mapchars(0x0c70, 0x0c81, ValueError),
    ((chr(0x0c84),), ValueError),
    ((chr(0x0c8d),), ValueError),
    ((chr(0x0c91),), ValueError),
    ((chr(0x0ca9),), ValueError),
    ((chr(0x0cb4),), ValueError),
    *mapchars(0x0cba, 0x0cbd, ValueError),
    ((chr(0x0cc5),), ValueError),
    ((chr(0x0cc9),), ValueError),
    *mapchars(0x0cce, 0x0cd4, ValueError),
    *mapchars(0x0cd7, 0x0cdd, ValueError),
    ((chr(0x0cdf),), ValueError),
    *mapchars(0x0ce2, 0x0ce5, ValueError),
    *mapchars(0x0cf0, 0x0d01, ValueError),
    ((chr(0x0d04),), ValueError),
    ((chr(0x0d0d),), ValueError),
    ((chr(0x0d11),), ValueError),
    ((chr(0x0d29),), ValueError),
    *mapchars(0x0d3a, 0x0d3d, ValueError),
    *mapchars(0x0d44, 0x0d45, ValueError),
    ((chr(0x0d49),), ValueError),
    *mapchars(0x0d4e, 0x0d56, ValueError),
    *mapchars(0x0d58, 0x0d5f, ValueError),
    *mapchars(0x0d62, 0x0d65, ValueError),
    *mapchars(0x0d70, 0x0d81, ValueError),
    ((chr(0x0d84),), ValueError),
    *mapchars(0x0d97, 0x0d99, ValueError),
    ((chr(0x0db2),), ValueError),
    ((chr(0x0dbc),), ValueError),
    *mapchars(0x0dbe, 0x0dbf, ValueError),
    *mapchars(0x0dc7, 0x0dc9, ValueError),
    *mapchars(0x0dcb, 0x0dce, ValueError),
    ((chr(0x0dd5),), ValueError),
    ((chr(0x0dd7),), ValueError),
    *mapchars(0x0de0, 0x0df1, ValueError),
    *mapchars(0x0df5, 0x0e00, ValueError),
    *mapchars(0x0e3b, 0x0e3e, ValueError),
    *mapchars(0x0e5c, 0x0e80, ValueError),
    ((chr(0x0e83),), ValueError),
    *mapchars(0x0e85, 0x0e86, ValueError),
    ((chr(0x0e89),), ValueError),
    *mapchars(0x0e8b, 0x0e8c, ValueError),
    *mapchars(0x0e8e, 0x0e93, ValueError),
    ((chr(0x0e98),), ValueError),
    ((chr(0x0ea0),), ValueError),
    ((chr(0x0ea4),), ValueError),
    ((chr(0x0ea6),), ValueError),
    *mapchars(0x0ea8, 0x0ea9, ValueError),
    ((chr(0x0eac),), ValueError),
    ((chr(0x0eba),), ValueError),
    *mapchars(0x0ebe, 0x0ebf, ValueError),
    ((chr(0x0ec5),), ValueError),
    ((chr(0x0ec7),), ValueError),
    *mapchars(0x0ece, 0x0ecf, ValueError),
    *mapchars(0x0eda, 0x0edb, ValueError),
    *mapchars(0x0ede, 0x0eff, ValueError),
    ((chr(0x0f48),), ValueError),
    *mapchars(0x0f6b, 0x0f70, ValueError),
    *mapchars(0x0f8c, 0x0f8f, ValueError),
    ((chr(0x0f98),), ValueError),
    ((chr(0x0fbd),), ValueError),
    *mapchars(0x0fcd, 0x0fce, ValueError),
    *mapchars(0x0fd0, 0x0fff, ValueError),
    ((chr(0x1022),), ValueError),
    ((chr(0x1028),), ValueError),
    ((chr(0x102b),), ValueError),
    *mapchars(0x1033, 0x1035, ValueError),
    *mapchars(0x103a, 0x103f, ValueError),
    *mapchars(0x105a, 0x109f, ValueError),
    *mapchars(0x10c6, 0x10cf, ValueError),
    *mapchars(0x10f9, 0x10fa, ValueError),
    *mapchars(0x10fc, 0x10ff, ValueError),
    *mapchars(0x115a, 0x115e, ValueError),
    *mapchars(0x11a3, 0x11a7, ValueError),
    *mapchars(0x11fa, 0x11ff, ValueError),
    ((chr(0x1207),), ValueError),
    ((chr(0x1247),), ValueError),
    ((chr(0x1249),), ValueError),
    *mapchars(0x124e, 0x124f, ValueError),
    ((chr(0x1257),), ValueError),
    ((chr(0x1259),), ValueError),
    *mapchars(0x125e, 0x125f, ValueError),
    ((chr(0x1287),), ValueError),
    ((chr(0x1289),), ValueError),
    *mapchars(0x128e, 0x128f, ValueError),
    ((chr(0x12af),), ValueError),
    ((chr(0x12b1),), ValueError),
    *mapchars(0x12b6, 0x12b7, ValueError),
    ((chr(0x12bf),), ValueError),
    ((chr(0x12c1),), ValueError),
    *mapchars(0x12c6, 0x12c7, ValueError),
    ((chr(0x12cf),), ValueError),
    ((chr(0x12d7),), ValueError),
    ((chr(0x12ef),), ValueError),
    ((chr(0x130f),), ValueError),
    ((chr(0x1311),), ValueError),
    *mapchars(0x1316, 0x1317, ValueError),
    ((chr(0x131f),), ValueError),
    ((chr(0x1347),), ValueError),
    *mapchars(0x135b, 0x1360, ValueError),
    *mapchars(0x137d, 0x139f, ValueError),
    *mapchars(0x13f5, 0x1400, ValueError),
    *mapchars(0x1677, 0x167f, ValueError),
    *mapchars(0x169d, 0x169f, ValueError),
    *mapchars(0x16f1, 0x16ff, ValueError),
    ((chr(0x170d),), ValueError),
    *mapchars(0x1715, 0x171f, ValueError),
    *mapchars(0x1737, 0x173f, ValueError),
    *mapchars(0x1754, 0x175f, ValueError),
    ((chr(0x176d),), ValueError),
    ((chr(0x1771),), ValueError),
    *mapchars(0x1774, 0x177f, ValueError),
    *mapchars(0x17dd, 0x17df, ValueError),
    *mapchars(0x17ea, 0x17ff, ValueError),
    ((chr(0x180f),), ValueError),
    *mapchars(0x181a, 0x181f, ValueError),
    *mapchars(0x1878, 0x187f, ValueError),
    *mapchars(0x18aa, 0x1dff, ValueError),
    *mapchars(0x1e9c, 0x1e9f, ValueError),
    *mapchars(0x1efa, 0x1eff, ValueError),
    *mapchars(0x1f16, 0x1f17, ValueError),
    *mapchars(0x1f1e, 0x1f1f, ValueError),
    *mapchars(0x1f46, 0x1f47, ValueError),
    *mapchars(0x1f4e, 0x1f4f, ValueError),
    ((chr(0x1f58),), ValueError),
    ((chr(0x1f5a),), ValueError),
    ((chr(0x1f5c),), ValueError),
    ((chr(0x1f5e),), ValueError),
    *mapchars(0x1f7e, 0x1f7f, ValueError),
    ((chr(0x1fb5),), ValueError),
    ((chr(0x1fc5),), ValueError),
    *mapchars(0x1fd4, 0x1fd5, ValueError),
    ((chr(0x1fdc),), ValueError),
    *mapchars(0x1ff0, 0x1ff1, ValueError),
    ((chr(0x1ff5),), ValueError),
    ((chr(0x1fff),), ValueError),
    *mapchars(0x2053, 0x2056, ValueError),
    *mapchars(0x2058, 0x205e, ValueError),
    *mapchars(0x2064, 0x2069, ValueError),
    *mapchars(0x2072, 0x2073, ValueError),
    *mapchars(0x208f, 0x209f, ValueError),
    *mapchars(0x20b2, 0x20cf, ValueError),
    *mapchars(0x20eb, 0x20ff, ValueError),
    *mapchars(0x213b, 0x213c, ValueError),
    *mapchars(0x214c, 0x2152, ValueError),
    *mapchars(0x2184, 0x218f, ValueError),
    *mapchars(0x23cf, 0x23ff, ValueError),
    *mapchars(0x2427, 0x243f, ValueError),
    *mapchars(0x244b, 0x245f, ValueError),
    ((chr(0x24ff),), ValueError),
    *mapchars(0x2614, 0x2615, ValueError),
    ((chr(0x2618),), ValueError),
    *mapchars(0x267e, 0x267f, ValueError),
    *mapchars(0x268a, 0x2700, ValueError),
    ((chr(0x2705),), ValueError),
    *mapchars(0x270a, 0x270b, ValueError),
    ((chr(0x2728),), ValueError),
    ((chr(0x274c),), ValueError),
    ((chr(0x274e),), ValueError),
    *mapchars(0x2753, 0x2755, ValueError),
    ((chr(0x2757),), ValueError),
    *mapchars(0x275f, 0x2760, ValueError),
    *mapchars(0x2795, 0x2797, ValueError),
    ((chr(0x27b0),), ValueError),
    *mapchars(0x27bf, 0x27cf, ValueError),
    *mapchars(0x27ec, 0x27ef, ValueError),
    *mapchars(0x2b00, 0x2e7f, ValueError),
    ((chr(0x2e9a),), ValueError),
    *mapchars(0x2ef4, 0x2eff, ValueError),
    *mapchars(0x2fd6, 0x2fef, ValueError),
    *mapchars(0x2ffc, 0x2fff, ValueError),
    ((chr(0x3040),), ValueError),
    *mapchars(0x3097, 0x3098, ValueError),
    *mapchars(0x3100, 0x3104, ValueError),
    *mapchars(0x312d, 0x3130, ValueError),
    ((chr(0x318f),), ValueError),
    *mapchars(0x31b8, 0x31ef, ValueError),
    *mapchars(0x321d, 0x321f, ValueError),
    *mapchars(0x3244, 0x3250, ValueError),
    *mapchars(0x327c, 0x327e, ValueError),
    *mapchars(0x32cc, 0x32cf, ValueError),
    ((chr(0x32ff),), ValueError),
    *mapchars(0x3377, 0x337a, ValueError),
    *mapchars(0x33de, 0x33df, ValueError),
    ((chr(0x33ff),), ValueError),
    *mapchars(0x4db6, 0x4dff, ValueError),
    *mapchars(0x9fa6, 0x9fff, ValueError),
    *mapchars(0xa48d, 0xa48f, ValueError),
    *mapchars(0xa4c7, 0xabff, ValueError),
    *mapchars(0xd7a4, 0xd7ff, ValueError),
    *mapchars(0xfa2e, 0xfa2f, ValueError),
    *mapchars(0xfa6b, 0xfaff, ValueError),
    *mapchars(0xfb07, 0xfb12, ValueError),
    *mapchars(0xfb18, 0xfb1c, ValueError),
    ((chr(0xfb37),), ValueError),
    ((chr(0xfb3d),), ValueError),
    ((chr(0xfb3f),), ValueError),
    ((chr(0xfb42),), ValueError),
    ((chr(0xfb45),), ValueError),
    *mapchars(0xfbb2, 0xfbd2, ValueError),
    *mapchars(0xfd40, 0xfd4f, ValueError),
    *mapchars(0xfd90, 0xfd91, ValueError),
    *mapchars(0xfdc8, 0xfdcf, ValueError),
    *mapchars(0xfdfd, 0xfdff, ValueError),
    *mapchars(0xfe10, 0xfe1f, ValueError),
    *mapchars(0xfe24, 0xfe2f, ValueError),
    *mapchars(0xfe47, 0xfe48, ValueError),
    ((chr(0xfe53),), ValueError),
    ((chr(0xfe67),), ValueError),
    *mapchars(0xfe6c, 0xfe6f, ValueError),
    ((chr(0xfe75),), ValueError),
    *mapchars(0xfefd, 0xfefe, ValueError),
    ((chr(0xff00),), ValueError),
    *mapchars(0xffbf, 0xffc1, ValueError),
    *mapchars(0xffc8, 0xffc9, ValueError),
    *mapchars(0xffd0, 0xffd1, ValueError),
    *mapchars(0xffd8, 0xffd9, ValueError),
    *mapchars(0xffdd, 0xffdf, ValueError),
    ((chr(0xffe7),), ValueError),
    *mapchars(0xffef, 0xfff8, ValueError),
    *mapchars(0x10000, 0x102ff, ValueError),
    ((chr(0x1031f),), ValueError),
    *mapchars(0x10324, 0x1032f, ValueError),
    *mapchars(0x1034b, 0x103ff, ValueError),
    *mapchars(0x10426, 0x10427, ValueError),
    *mapchars(0x1044e, 0x1cfff, ValueError),
    *mapchars(0x1d0f6, 0x1d0ff, ValueError),
    *mapchars(0x1d127, 0x1d129, ValueError),
    *mapchars(0x1d1de, 0x1d3ff, ValueError),
    ((chr(0x1d455),), ValueError),
    ((chr(0x1d49d),), ValueError),
    *mapchars(0x1d4a0, 0x1d4a1, ValueError),
    *mapchars(0x1d4a3, 0x1d4a4, ValueError),
    *mapchars(0x1d4a7, 0x1d4a8, ValueError),
    ((chr(0x1d4ad),), ValueError),
    ((chr(0x1d4ba),), ValueError),
    ((chr(0x1d4bc),), ValueError),
    ((chr(0x1d4c1),), ValueError),
    ((chr(0x1d4c4),), ValueError),
    ((chr(0x1d506),), ValueError),
    *mapchars(0x1d50b, 0x1d50c, ValueError),
    ((chr(0x1d515),), ValueError),
    ((chr(0x1d51d),), ValueError),
    ((chr(0x1d53a),), ValueError),
    ((chr(0x1d53f),), ValueError),
    ((chr(0x1d545),), ValueError),
    *mapchars(0x1d547, 0x1d549, ValueError),
    ((chr(0x1d551),), ValueError),
    *mapchars(0x1d6a4, 0x1d6a7, ValueError),
    *mapchars(0x1d7ca, 0x1d7cd, ValueError),
    *mapchars(0x1d800, 0x1fffd, ValueError),
    *mapchars(0x2a6d7, 0x2f7ff, ValueError),
    *mapchars(0x2fa1e, 0x2fffd, ValueError),
    *mapchars(0x30000, 0x3fffd, ValueError),
    *mapchars(0x40000, 0x4fffd, ValueError),
    *mapchars(0x50000, 0x5fffd, ValueError),
    *mapchars(0x60000, 0x6fffd, ValueError),
    *mapchars(0x70000, 0x7fffd, ValueError),
    *mapchars(0x80000, 0x8fffd, ValueError),
    *mapchars(0x90000, 0x9fffd, ValueError),
    *mapchars(0xa0000, 0xafffd, ValueError),
    *mapchars(0xb0000, 0xbfffd, ValueError),
    *mapchars(0xc0000, 0xcfffd, ValueError),
    *mapchars(0xd0000, 0xdfffd, ValueError),
    ((chr(0xe0000),), ValueError),
    *mapchars(0xe0002, 0xe001f, ValueError),
    *mapchars(0xe0080, 0xefffd, ValueError),

    # Non-ASCII space
    (('\u0020',), ' '),
    (('\u00A0',), ' '),
    (('\u1680',), ' '),
    *mapchars(0x2000, 0x200a, ' '),
    (('\u202f',), ' '),
    (('\u205f',), ' '),
    (('\u3000',), ' '),

    # Mapped to nothing
    (('\u00ad',), ''),
    (('\u034f',), ''),
    (('\u1806',), ''),
    *mapchars(0x180b, 0x180d, ''),
    *mapchars(0x200b, 0x200d, ''),
    (('\u2060',), ''),
    *mapchars(0xfe00, 0xfe0f, ''),
    (('\ufeff',), ''),

    # ASCII control characters
    *mapchars(0x00, 0x1f, ValueError),
    (('\007f',), ValueError),

    # Non-ASCII control characters
    *mapchars(0x80, 0x9f, ValueError),
    (('\u06dd',), ValueError),
    (('\u070f',), ValueError),
    (('\u180e',), ValueError),
    (('\u200c',), ''),
    (('\u200d',), ''),
    (('\u2028',), ValueError),
    (('\u2029',), ValueError),
    (('\u2060',), ''),
    *mapchars(0x2061, 0x2063, ValueError),
    *mapchars(0x206a, 0x206f, ValueError),
    (('\ufeff',), ''),
    *mapchars(0xfff9, 0xfffc, ValueError),
    *mapchars(0x1d173, 0x1d17a, ValueError),

    # Private Use characters
    *mapchars(0xe000, 0xf8ff, ValueError),
    *mapchars(0xf0000, 0xffffd, ValueError),
    *mapchars(0x100000, 0x10fffd, ValueError),

    # Non-character code points
    *mapchars(0xfdd0, 0xfdef, ValueError),
    *mapchars(0x1fffe, 0x1ffff, ValueError),
    *mapchars(0x2fffe, 0x2ffff, ValueError),
    *mapchars(0x3fffe, 0x3ffff, ValueError),
    *mapchars(0x4fffe, 0x4ffff, ValueError),
    *mapchars(0x5fffe, 0x5ffff, ValueError),
    *mapchars(0x6fffe, 0x6ffff, ValueError),
    *mapchars(0x7fffe, 0x7ffff, ValueError),
    *mapchars(0x8fffe, 0x8ffff, ValueError),
    *mapchars(0x9fffe, 0x9ffff, ValueError),
    *mapchars(0xafffe, 0xaffff, ValueError),
    *mapchars(0xbfffe, 0xbffff, ValueError),
    *mapchars(0xcfffe, 0xcffff, ValueError),
    *mapchars(0xdfffe, 0xdffff, ValueError),
    *mapchars(0xefffe, 0xeffff, ValueError),
    *mapchars(0xffffe, 0xfffff, ValueError),
    *mapchars(0x10fffe, 0x10ffff, ValueError),

    # Surrogate code points
    *mapchars(0xd800, 0xdfff, ValueError),

    # Inappropriate for plain text characters
    *mapchars(0xfff9, 0xfffd, ValueError),

    # Inappropriate for canonical representation characters
    *mapchars(0x2ff0, 0x2ffb, ValueError),

    # Change display properties or deprecated characters
    *mapchars(0x0340, 0x0341, ValueError),
    *mapchars(0x200e, 0x200f, ValueError),
    *mapchars(0x202a, 0x202e, ValueError),
    *mapchars(0x206a, 0x206f, ValueError),

    # Tagging characters
    (chr(0xe0001), ValueError),
    *mapchars(0xe0020, 0xe007f, ValueError),

    # Bi-directional characters
    (('\u0627\u0031',), ValueError),
    (('\u0627\u0031\u0628',), '\u0627\u0031\u0628'),

    # Examples from RFC 4013
    (('I\u00adX',), 'IX'),
    (('user',), 'user'),
    (('USER',), 'USER'),
    (('\u00aa',), 'a'),
    (('\u2168',), 'IX'),
    (('\u0007',), ValueError),
    (('\u0627\u0031',), ValueError)
)


#
# Tests
#

class TestBaseAuth(unittest.TestCase):
    test_prepare = unittest.skipIf(os.getenv('QUICKTEST'), 'slow')(
        makerunner(BaseAuth.prepare, STRINGS)
    )


#
# Boilerplate
#

if __name__ == '__main__':
    unittest.main()
