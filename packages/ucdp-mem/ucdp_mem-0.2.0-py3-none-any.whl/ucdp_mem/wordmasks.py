#
# MIT License
#
# Copyright (c) 2024 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""
Word Masks.
"""

from typing import TypeAlias

import ucdp as u
from humannum import bytesize_, hex_
from icdutil.num import calc_next_power_of2, is_power_of
from ucdp_addr.util import calc_depth_size

Wordmasks: TypeAlias = tuple[u.Hex, ...]


def cast_wordmasks(wordmasks: Wordmasks, width: int | None = None) -> Wordmasks:
    """
    Cast `wordmasks` and check compatibility to `width`.

    >>> cast_wordmasks((0x3F, 0x3F, 0x3F, 0x3F))
    (Hex('0x3F'), Hex('0x3F'), Hex('0x3F'), Hex('0x3F'))

    >>> cast_wordmasks((0x3F, 0x3F, 0x3F))
    Traceback (most recent call last):
        ...
    ValueError: Number of wordmask elements of ((Hex('0x3F'), Hex('0x3F'), Hex('0x3F'))) MUST be a power of 2, not 3
    >>> cast_wordmasks((0x3F, 0x3F, 0x3F, 0x3F), width=27)
    Traceback (most recent call last):
        ...
    ValueError: The implied width of the wordmasks (Hex('0x3F'), ...) is 24 bit differs from intended width 27 bit.

    """
    masks = tuple(hex_(mask) for mask in wordmasks)
    maskslen = len(masks)
    if not is_power_of(maskslen, 2):
        raise ValueError(f"Number of wordmask elements of ({masks}) MUST be a power of 2, not {maskslen}")
    if width is not None:
        weight = sum(bin(mask).count("1") for mask in masks)
        if weight != width:
            msg = f"The implied width of the wordmasks {masks} is {weight} bit differs from intended width {width} bit."
            raise ValueError(msg)
    return masks


def width_to_wordmasks(width: int, buswidth: int = 32):
    """
    Calculate wordmasks for `width`.

    >>> width_to_wordmasks(24)
    (Hex('0xFFFFFF'),)
    >>> width_to_wordmasks(32)
    (Hex('0xFFFFFFFF'),)
    >>> width_to_wordmasks(48)
    (Hex('0xFFFFFF'), Hex('0xFFFFFF'))
    >>> width_to_wordmasks(64)
    (Hex('0xFFFFFFFF'), Hex('0xFFFFFFFF'))
    >>> width_to_wordmasks(65)
    (Hex('0x1FFFF'), Hex('0xFFFF'), Hex('0xFFFF'), Hex('0xFFFF'))
    >>> width_to_wordmasks(66)
    (Hex('0x1FFFF'), Hex('0x1FFFF'), Hex('0xFFFF'), Hex('0xFFFF'))
    >>> width_to_wordmasks(79)
    (Hex('0xFFFFF'), Hex('0xFFFFF'), Hex('0xFFFFF'), Hex('0x7FFFF'))
    >>> width_to_wordmasks(80)
    (Hex('0xFFFFF'), Hex('0xFFFFF'), Hex('0xFFFFF'), Hex('0xFFFFF'))
    >>> width_to_wordmasks(81)
    (Hex('0x1FFFFF'), Hex('0xFFFFF'), Hex('0xFFFFF'), Hex('0xFFFFF'))
    >>> width_to_wordmasks(120)
    (Hex('0x3FFFFFFF'), Hex('0x3FFFFFFF'), Hex('0x3FFFFFFF'), Hex('0x3FFFFFFF'))
    """
    minwords = ((width - 1) // buswidth) + 1
    words = calc_next_power_of2(minwords) if minwords > 1 else minwords
    rem = width % words
    wordmasks = []
    for _ in range(words):
        wordwidth = width // words
        if rem:
            rem -= 1
            wordwidth += 1
        wordmasks.append(2**wordwidth - 1)
    return cast_wordmasks(tuple(wordmasks), width=width)


def size_to_wordsize(
    width: int,
    depth: int | None = None,
    size: u.Bytes | None = None,
    wordmasks: Wordmasks | None = None,
    bytesperword: int = 4,
) -> u.Bytes:
    """
    Convert memory `size` into 32-bit word size.

    >>> size_to_wordsize(48, depth=1024)
    Bytesize('8 KB')
    >>> size_to_wordsize(48, size=3*1024)
    Bytesize('4 KB')

    >>> size_to_wordsize(48, depth=1024, wordmasks=(0xF0F0F0, 0xF0F0F0, 0xF0F0F0, 0xF0F0F0))
    Bytesize('16 KB')
    >>> size_to_wordsize(48, wordmasks=(0xF0F0F0, 0xF0F0F0, 0xF0F0F0, 0xF0F0F0), size=3*1024)
    Bytesize('8 KB')
    """
    depth_ = calc_depth_size(width, depth=depth, size=size)[0]
    wordmasks_ = cast_wordmasks(wordmasks, width) if wordmasks else width_to_wordmasks(width)
    return bytesize_(int(depth_ * len(wordmasks_) * bytesperword))
