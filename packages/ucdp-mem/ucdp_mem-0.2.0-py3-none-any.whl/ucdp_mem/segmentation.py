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
Segmentation.

`Segmentation` describes the physical split of a logical memory.

The memory and segmentation geometry need to be identical. Otherwise a `SegmentationError` is raised.
The method (`AMemMod.create_segmentation`) shall implement the specific construction of a segmentation.

A `Segmentation` instance can be created *explicitly*:

    >>> s = Segmentation(depth=512, width=32)
    >>> s.add_segment(0, 0, 256, 16)
    >>> s.add_segment(1, 0, 256, 16)
    >>> s.add_segment(0, 1, 128, 16)
    >>> s.add_segment(1, 1, 128, 16)
    >>> s.add_segment(0, 2, 128, 16)
    >>> s.add_segment(1, 2, 128, 16)
    >>> print(s.get_overview())
    y/x    1        0
     0  256x16/1 256x16/1
     1  128x16/1 128x16/1
     2  128x16/1 128x16/1
    Total: 512x32/1(2 KB)

"""

import math
from collections.abc import Iterator
from functools import cached_property
from itertools import chain

import ucdp as u
from aligntext import align, center
from defaultlist import defaultlist
from icdutil import num
from pydantic import NonNegativeInt, PositiveInt
from ucdp_addr import Addrspace, DefaultAddrspace, zip_addrspaces
from ucdp_addr.util import calc_depth_size
from ucdp_glbl.lane import DefaultLane, Lane, Lanes

from .memtechconstraints import MemTechConstraints
from .types import SliceWidths
from .util import gcd


class Segment(u.LightObject):
    """Memory Segment."""

    x: NonNegativeInt
    """X-Coordinate aka Horizontal-Coordinate in Segmentation Matrix. Starting at 0. Growing to the *LEFT*."""
    y: NonNegativeInt
    """Y-Coordinate aka Vertical-Coordinate in Segmentation Matrix. Starting at 0. Growing to the *BOTTOM*."""
    slice_: u.Slice
    """Word Horizontal-Split."""
    offset: NonNegativeInt
    """Word Vertical-Addressing Offset in Matrix. Sum Of All Depths Of Segments With Y Smaller Than This Segment."""
    depth: PositiveInt
    """Number of Words."""
    width: PositiveInt
    """Width of One Word."""
    phydepth: PositiveInt
    """Number of Words, maybe a little bit more, to meet tech constraints."""
    phywidth: PositiveInt
    """Width of One Word, maybe a little bit more, to meet tech constraints."""
    slicewidths: SliceWidths | None = None
    wordslices: PositiveInt = 1
    """Number of Access Slices to the Word."""
    pwrlane: Lane | None = None
    """Power Lane."""
    accesslane: Lane | None = None
    """Access Lane."""

    @property
    def wordslicewidth(self):
        """Word Slice Width."""
        return self.width // self.wordslices

    @property
    def phybits(self) -> int:
        """Number of Bits."""
        return self.phywidth * self.phydepth

    def get_overview(self) -> str:
        """Overview."""
        depth = self.depth if self.phydepth == self.depth else f"{self.depth}({self.phydepth})"
        width = self.width if self.phywidth == self.width else f"{self.width}({self.phywidth})"
        overview = f"{depth}x{width}/{self.wordslices}"
        if self.pwrlane:
            overview = f"{overview},pwr={self.pwrlane.name}"
        if self.accesslane:
            overview = f"{overview},acc={self.accesslane.name}"
        return overview


class Segmentation(u.Object):
    """Memory Segmentation."""

    depth: PositiveInt
    width: PositiveInt
    slicewidths: SliceWidths | None = None

    _rows: list[list[Segment]] = u.PrivateField(default_factory=lambda: defaultlist(defaultlist))
    _depths: list[Segment] = u.PrivateField(default_factory=defaultlist)
    _widths: list[Segment] = u.PrivateField(default_factory=defaultlist)
    _lock: bool = u.PrivateField(default=False)

    @property
    def segments(self) -> tuple[Segment, ...]:
        """Segments."""
        return tuple(chain(*self._rows))

    @property
    def rows(self) -> tuple[tuple[Segment, ...], ...]:
        """Rows And Their Segments."""
        return tuple(tuple(row) for row in self._rows)

    @property
    def depths(self) -> tuple[int, ...]:
        """Depths."""
        return tuple(self._depths)

    @property
    def widths(self) -> tuple[int, ...]:
        """Widths."""
        return tuple(self._widths)

    @property
    def x_width(self) -> PositiveInt:
        """Number of X-Segments."""
        return len(self._widths)

    @property
    def y_width(self) -> PositiveInt:
        """Number of Y-Segments."""
        return len(self._depths)

    @property
    def gcd_depth(self) -> PositiveInt:
        """Depths."""
        return gcd(self._depths)

    @property
    def wordslices(self) -> PositiveInt:
        """Wordslices."""
        if not self.slicewidths:
            return 1
        return len(self.slicewidths)

    @cached_property
    def size(self) -> u.Bytesize:
        """Size in Bytes."""
        return calc_depth_size(self.width, depth=self.depth)[1]

    @property
    def phybits(self) -> PositiveInt:
        """Physical Size In Bits."""
        return sum(segment.phybits for segment in self.segments)

    @property
    def addrwidth(self) -> PositiveInt:
        """Address width in bits."""
        return int(num.calc_unsigned_width(self.depth - 1))

    @property
    def is_trivial(self) -> bool:
        """Segmentation Is Just A Pass-Through."""
        if len(self._widths) != 1 or len(self._depths) != 1:
            return False
        segment = self._rows[0][0]
        if segment.width != segment.phywidth or segment.depth != segment.phydepth:
            return False
        return True

    def add_segment(
        self,
        x: NonNegativeInt,
        y: NonNegativeInt,
        depth: PositiveInt,
        width: PositiveInt,
        phydepth: PositiveInt | None = None,
        phywidth: PositiveInt | None = None,
        wordslices: PositiveInt = 1,
        pwrlane: Lane | None = None,
        accesslane: Lane | None = None,
    ):
        """
        Add memory segment.

        Args:
            x: x-coordinate, starting at 0, along the width.
            y: y-coordinate, starting at 0, along the depth.
            depth: depth in words.
            width: width in bits.
            phydepth: physical depth in words, maybe a little bit more, to meet tech constraints
            phywidth: physical width in bits, maybe a little bit more, to meet tech constraints
            wordslices: 'width' is cut into this number of slices.
            pwrlane: Power Lane.
            accesslane: Access Lane.

        Rules:

            * Segments with the same Y coordinate need to have the same depth.
            * The width of all segments with the same Y need to sum up to the total width.
            * The depth of all segments with the same X need to sum up to the total depth.
        """
        if self._lock:
            raise u.LockError("Cannot add segment anymore.")
        segments = self._rows
        # check Y-coordinate
        if len(segments) < y:
            raise ValueError(f"Cannot forward to y={y}. Segmentation must be filled sequentially from 0")
        row = segments[y]
        # check X-coordinate
        if len(row) < x:
            raise ValueError(f"Cannot forward to x={x}. Segmentation must be filled sequentially from 0")
        # check slice
        widths = self._widths
        if widths[x] is None:
            widths[x] = width  # type: ignore[call-overload]
        elif widths[x] != width:
            raise ValueError(f"Row x={x} width must be {widths[x]} not {width}.")
        # check depth
        depths = self._depths
        if depths[y] is None:
            depths[y] = depth  # type: ignore[call-overload]
        elif depths[y] != depth:
            raise ValueError(f"Row y={y} depth must be {depths[y]} not {depth}.")
        # add
        if row[x]:
            raise ValueError(f"Segment x={x} y={y} is already allocated")
        slice_ = u.Slice(right=sum(widths[:x]), width=width)
        offset = sum(depths[:y])
        row[x] = Segment(
            x=x,
            y=y,
            slice_=slice_,
            offset=offset,
            depth=depth,
            width=width,
            phydepth=phydepth or depth,
            phywidth=phywidth or width,
            wordslices=wordslices,
            pwrlane=pwrlane,
            accesslane=accesslane,
        )

    def lock(self) -> None:
        """Lock And Check."""
        if self._lock:
            raise u.LockError("Already locked.")
        self._lock = True
        # check width
        widths = sum(self.widths)
        if widths != self.width:
            raise ValueError(f"Segment widths {widths} dont sum-up to total width {self.width}")
        # check depth
        depths = sum(self.depths)
        if depths != self.depth:
            raise ValueError(f"Segment depths {depths} dont sum-up to total depth {self.depth}")
        # segments
        for y, row in enumerate(self._rows):
            if len(row) != len(self.widths):
                raise ValueError(f"Row y={y} misses segments")

    def get_overview(self) -> str:
        """Human readable summary."""
        rows = [["y/x", *range(self.x_width - 1, -1, -1)]]
        rows += [[y] + [seg.get_overview() for seg in reversed(segs)] for y, segs in enumerate(self._rows)]
        details = align(rows, alignments=(center,))
        return f"{details}\nTotal: {self.depth}x{self.width}/{self.wordslices}({self.size})"

    @staticmethod
    def create(
        width: PositiveInt,
        depth: PositiveInt,
        slicewidths: SliceWidths | None = None,
        accesslanes: Lanes | None = None,
        powerlanes: Lanes | None = None,
        constraints: MemTechConstraints | None = None,
    ) -> "Segmentation":
        """Create Segmentation."""
        constraints = constraints or MemTechConstraints()
        segmentation = Segmentation(width=width, depth=depth, slicewidths=slicewidths)

        depth_inc = constraints.depth_inc
        width_inc = constraints.width_inc

        segwidths = segmentation._split_width(constraints.max_width)
        segphywidths = [num.align(segwidth, align=width_inc) for segwidth in segwidths]
        segdepths = segmentation._split_depth(accesslanes, powerlanes, constraints.max_depth)
        for y, (segdepth, accesslane, powerlane) in enumerate(segdepths):
            segphydepth = num.align(segdepth, align=depth_inc)
            for x, (segwidth, segphywidth) in enumerate(zip(segwidths, segphywidths, strict=True)):
                segmentation.add_segment(
                    x,
                    y,
                    segdepth,
                    segwidth,
                    phydepth=segphydepth,
                    phywidth=segphywidth,
                    pwrlane=powerlane,
                    accesslane=accesslane,
                )
        segmentation.lock()
        return segmentation

    def _split_width(self, max_width: PositiveInt | None) -> tuple[PositiveInt, ...]:
        width = self.width
        if not max_width:
            return (width,)
        x_width = int(math.ceil(width / max_width))
        if (width % x_width) == 0:
            return (width // x_width,) * x_width

        widths = []
        while True:
            if width > max_width:
                widths.append(max_width)
            else:
                widths.append(width)
                break
            width -= max_width
        return tuple(widths)

    def _split_depth(
        self,
        accesslanes: Lanes | None,
        powerlanes: Lanes | None,
        max_depth: PositiveInt | None,
    ) -> Iterator[tuple[PositiveInt, Addrspace, Addrspace]]:
        width = self.width
        max_depth = max_depth or self.depth
        bytes_per_word = width / 8  # might be fractional
        if accesslanes or powerlanes:
            accessspaces = tuple(self._lane2addrspaces(accesslanes))
            powerspaces = tuple(self._lane2addrspaces(powerlanes))
            for accessspace, powerspace in zip_addrspaces(accessspaces, powerspaces):
                common = accessspace.get_intersect(powerspace)
                offset = int(common.baseaddr / bytes_per_word)
                depth = int(common.size / bytes_per_word)
                accesslane = self._addrspace2lane(accessspace)
                powerlane = self._addrspace2lane(powerspace)
                for segdepth in _split_depth(depth, max_depth, offset=offset):
                    yield segdepth, accesslane, powerlane
        else:
            for segdepth in _split_depth(self.depth, max_depth):
                yield segdepth, None, None

    def _lane2addrspaces(self, lanes: Lanes) -> Iterator[Addrspace]:
        """Convert to Address Spaces."""
        baseaddr = 0
        for lane in lanes or (DefaultLane(size=self.size),):
            if lane.name:
                yield Addrspace(name=lane.name, baseaddr=baseaddr, width=8, size=lane.size, attrs=lane.attrs)
            else:
                yield DefaultAddrspace(width=8, size=lane.size, attrs=lane.attrs)
            baseaddr += lane.size

    @staticmethod
    def _addrspace2lane(addrspace: Addrspace) -> Lane | None:
        if not addrspace.name:
            return None
        return Lane(name=addrspace.name, size=addrspace.size, attrs=addrspace.attrs)


def _split_depth(depth, max_depth, offset=0):
    """
    Split memory `depth` into aligned segments with `max_depth` starting at may be not aligned `offset`.

    >>> tuple(_split_depth(7*1024, 2*1024))
    (2048, 2048, 2048, 1024)
    >>> tuple(_split_depth(9*1024, 4*1024, offset=512))
    (512, 1024, 2048, 4096, 1536)
    """

    def split(d):
        remainder = (d % max_depth) or max_depth
        y_d = int(math.ceil(d / max_depth))
        return [max_depth] * (y_d - 1) + [remainder]

    aligned_limited_segs = [split(int(addrrange.size)) for addrrange in num.split_aligned_segs(offset, depth)]
    return chain(*aligned_limited_segs)
