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
"""Test sv.mako."""

import ucdp_mem as um
from pytest import raises
from ucdp_addr.addrspace import RO, RW, RWL


def test_rom():
    """ROM."""
    rom = um.RomMod(width=16, depth=128)
    assert rom.width == 16
    assert rom.depth == 128
    assert rom.size == 256
    assert rom.access == RO


def test_otp():
    """OTP."""
    otp = um.OtpMod(width=16, depth=128)
    assert otp.width == 16
    assert otp.depth == 128
    assert otp.size == 256
    assert otp.access == RWL


def test_ram():
    """RAM."""
    ram = um.RamMod(width=16, depth=128)
    assert ram.width == 16
    assert ram.depth == 128
    assert ram.size == 256
    assert ram.access == RW
    assert ram.retention is False


def test_ram_ret():
    """RAM with retention."""
    ram = um.RamMod(width=16, depth=128, retention=True)
    assert ram.width == 16
    assert ram.depth == 128
    assert ram.size == 256
    assert ram.access == RW
    assert ram.retention is True


def test_slicewidths():
    """Slice Widths."""
    ram = um.RamMod(width=16, depth=128, slicewidths=(4, 4, 8))
    assert ram.slicewidths == (4, 4, 8)

    ram = um.RamMod(width=16, depth=128, slicewidth=4)
    assert ram.slicewidths == (4, 4, 4, 4)

    with raises(ValueError):
        um.RamMod(width=16, depth=128, slicewidth=4, slicewidths=(4, 5))
