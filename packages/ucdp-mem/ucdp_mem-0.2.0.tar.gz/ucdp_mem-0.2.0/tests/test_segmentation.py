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

import re

import ucdp as u
from pytest import raises
from ucdp import Slice
from ucdp_glbl.lane import Lane
from ucdp_mem import MemTechConstraints
from ucdp_mem.segmentation import Segment, Segmentation


def test_segmentation():
    """Segmentation."""
    s = Segmentation(depth=512, width=32)
    s.add_segment(0, 0, 256, 16)
    s.add_segment(1, 0, 256, 16)
    s.add_segment(0, 1, 128, 16)
    s.add_segment(1, 1, 128, 16)
    s.add_segment(0, 2, 128, 16)
    s.add_segment(1, 2, 128, 16)
    s.lock()

    assert s.depths == (256, 128, 128)
    assert s.widths == (16, 16)
    assert s.x_width == 2
    assert s.y_width == 3
    assert s.addrwidth == 9
    assert s.gcd_depth == 128
    assert s.phybits == 512 * 32

    assert s.rows == (
        (
            Segment(
                x=0,
                y=0,
                slice_=Slice("15:0"),
                offset=0,
                depth=256,
                phydepth=256,
                width=16,
                phywidth=16,
            ),
            Segment(
                x=1,
                y=0,
                slice_=Slice("31:16"),
                offset=0,
                depth=256,
                phydepth=256,
                width=16,
                phywidth=16,
            ),
        ),
        (
            Segment(
                x=0,
                y=1,
                slice_=Slice("15:0"),
                offset=256,
                depth=128,
                phydepth=128,
                width=16,
                phywidth=16,
            ),
            Segment(
                x=1,
                y=1,
                slice_=Slice("31:16"),
                offset=256,
                depth=128,
                phydepth=128,
                width=16,
                phywidth=16,
            ),
        ),
        (
            Segment(
                x=0,
                y=2,
                slice_=Slice("15:0"),
                offset=384,
                depth=128,
                phydepth=128,
                width=16,
                phywidth=16,
            ),
            Segment(
                x=1,
                y=2,
                slice_=Slice("31:16"),
                offset=384,
                depth=128,
                phydepth=128,
                width=16,
                phywidth=16,
            ),
        ),
    )

    seg0_0 = s.rows[0][0]
    assert seg0_0.wordslicewidth == 16


def test_segmentation_x_error():
    """Segmentation X-Error."""
    s = Segmentation(depth=512, width=32)
    msg = "Cannot forward to x=1. Segmentation must be filled sequentially from 0"
    with raises(ValueError, match=re.escape(msg)):
        s.add_segment(1, 0, 256, 16)


def test_segmentation_y_error():
    """Segmentation Y-Error."""
    s = Segmentation(depth=512, width=32)
    msg = "Cannot forward to y=1. Segmentation must be filled sequentially from 0"
    with raises(ValueError, match=re.escape(msg)):
        s.add_segment(0, 1, 256, 16)


def test_segmentation_x_width_error():
    """Segmentation X-Width-Error."""
    s = Segmentation(depth=512, width=32)
    s.add_segment(0, 0, 256, 16)
    msg = "Row x=0 width must be 16 not 8."
    with raises(ValueError, match=re.escape(msg)):
        s.add_segment(0, 1, 256, 8)


def test_segmentation_y_depth_error():
    """Segmentation Y-Depth-Error."""
    s = Segmentation(depth=512, width=32)
    s.add_segment(0, 0, 256, 16)
    msg = "Row y=0 depth must be 256 not 128."
    with raises(ValueError, match=re.escape(msg)):
        s.add_segment(1, 0, 128, 16)


def test_segmentation_alloc_error():
    """Segmentation Alloc-Error."""
    s = Segmentation(depth=512, width=32)
    s.add_segment(0, 0, 256, 16)
    msg = "Segment x=0 y=0 is already allocated"
    with raises(ValueError, match=re.escape(msg)):
        s.add_segment(0, 0, 256, 16)


def test_lock_missing_segments():
    """Segmentation."""
    s = Segmentation(depth=256 + 128, width=32)
    s.add_segment(0, 0, 256, 16)
    s.add_segment(0, 1, 128, 16)
    s.add_segment(1, 1, 128, 16)
    msg = "Row y=0 misses segments"
    with raises(ValueError, match=re.escape(msg)):
        s.lock()


def test_lock_depth_error():
    """Segmentation."""
    s = Segmentation(depth=512, width=32)
    s.add_segment(0, 0, 256, 16)
    s.add_segment(1, 0, 256, 16)
    s.add_segment(0, 1, 128, 16)
    s.add_segment(1, 1, 128, 16)
    msg = "Segment depths 384 dont sum-up to total depth 512"
    with raises(ValueError, match=re.escape(msg)):
        s.lock()


def test_lock_width_error():
    """Segmentation."""
    s = Segmentation(depth=256 + 128, width=32)
    s.add_segment(0, 0, 256, 16)
    s.add_segment(1, 0, 256, 8)
    s.add_segment(0, 1, 128, 16)
    s.add_segment(1, 1, 128, 8)
    msg = "Segment widths 24 dont sum-up to total width 32"
    with raises(ValueError, match=re.escape(msg)):
        s.lock()


def test_lock_empty():
    """Segmentation."""
    s = Segmentation(depth=256, width=32)
    with raises(ValueError):
        s.lock()


def test_relock():
    """Re-Lock."""
    s = Segmentation(depth=256, width=16)
    s.add_segment(0, 0, 256, 16)
    s.lock()
    with raises(u.LockError):
        s.lock()


def test_postlock():
    """Post-Lock."""
    s = Segmentation(depth=256, width=16)
    s.add_segment(0, 0, 256, 16)
    s.lock()
    with raises(u.LockError):
        s.add_segment(0, 0, 256, 16)


def test_create():
    """Create With Simple."""
    width = 64
    depth = 14 * 1024
    alanes = (Lane(name="a0", size="56k"), Lane(name="a1", size="56k"))
    blanes = (Lane(name="b0", size="40k"), Lane(name="b1", size="72k"))

    s = Segmentation.create(width=width, depth=depth)
    assert (
        s.get_overview()
        == """\
y/x     0
 0  14336x64/1
Total: 14336x64/1(112 KB)"""
    )

    constraints = MemTechConstraints(max_depth=2048, max_width=32)
    s = Segmentation.create(width=width, depth=depth, constraints=constraints)
    assert (
        s.get_overview()
        == """\
y/x     1         0
 0  2048x32/1 2048x32/1
 1  2048x32/1 2048x32/1
 2  2048x32/1 2048x32/1
 3  2048x32/1 2048x32/1
 4  2048x32/1 2048x32/1
 5  2048x32/1 2048x32/1
 6  2048x32/1 2048x32/1
Total: 14336x64/1(112 KB)"""
    )

    constraints = MemTechConstraints(max_depth=4096)
    s = Segmentation.create(width=width, depth=depth, constraints=constraints)
    assert (
        s.get_overview()
        == """\
y/x     0
 0  4096x64/1
 1  4096x64/1
 2  4096x64/1
 3  2048x64/1
Total: 14336x64/1(112 KB)"""
    )

    constraints = MemTechConstraints(max_depth=4096)
    s = Segmentation.create(width=width, depth=depth, constraints=constraints, accesslanes=alanes)
    assert (
        s.get_overview()
        == """\
y/x        0
 0  4096x64/1,acc=a0
 1  3072x64/1,acc=a0
 2  1024x64/1,acc=a1
 3  4096x64/1,acc=a1
 4  2048x64/1,acc=a1
Total: 14336x64/1(112 KB)"""
    )

    constraints = MemTechConstraints(max_depth=4096)
    s = Segmentation.create(width=width, depth=depth, constraints=constraints, accesslanes=blanes, powerlanes=alanes)
    assert (
        s.get_overview()
        == """\
y/x            0
 0  4096x64/1,pwr=a0,acc=b0
 1  1024x64/1,pwr=a0,acc=b0
 2  1024x64/1,pwr=a0,acc=b1
 3  1024x64/1,pwr=a0,acc=b1
 4  1024x64/1,pwr=a1,acc=b1
 5  4096x64/1,pwr=a1,acc=b1
 6  2048x64/1,pwr=a1,acc=b1
Total: 14336x64/1(112 KB)"""
    )
