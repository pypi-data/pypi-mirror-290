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
Segmentation Multiplexer.
"""

from functools import cached_property

import ucdp as u
from ucdp_glbl.lane import Lanes
from ucdp_glbl.mem import MemIoType

from .segmentation import Segment, Segmentation
from .types import LanesMemIoType


class SegmentsIoType(u.AStructType):
    """Memory Lanes IO Type."""

    segments: tuple[Segment, ...]
    writable: bool = True

    def _build(self) -> None:
        for segment in self.segments:
            name = f"y{segment.y}_x{segment.x}"
            type_ = MemIoType(
                datawidth=segment.phywidth,
                addrwidth=u.log2(segment.phydepth - 1),
                writable=self.writable,
                slicewidths=segment.slicewidths,
                addressing="data",
            )
            self._add(name, type_)

    @staticmethod
    def from_segmentation(segmentation: Segmentation, writable: bool = True) -> "SegmentsIoType":
        """Create IO-Type from Segmentation."""
        return SegmentsIoType(segments=segmentation.segments, writable=writable)


class SegMuxMod(u.ATailoredMod):
    """Segmentation Multiplexer."""

    segmentation: Segmentation
    accesslanes: Lanes
    writable: bool = True
    addrgate: bool = False

    def _build(self) -> None:
        self.add_port(self.intype, "in_i")
        self.add_port(self.outtype, "out_o")

    @cached_property
    def intype(self) -> LanesMemIoType:
        """In-IO Type."""
        segmentation = self.segmentation
        return LanesMemIoType(
            datawidth=segmentation.width,
            writable=self.writable,
            slicewidths=segmentation.slicewidths,
            lanes=self.accesslanes,
        )

    @cached_property
    def outtype(self) -> SegmentsIoType:
        """Out-IO Type."""
        return SegmentsIoType.from_segmentation(self.segmentation, writable=self.writable)

    def get_overview(self) -> str:
        """Overview."""
        return self.segmentation.get_overview()

    @classmethod
    def create(
        cls,
        parent: u.BaseMod,
        name: str,
        segmentation: Segmentation,
        accesslanes: Lanes,
        inroute: str,
        outroute: str,
        **kwargs,
    ):
        """Create Segmentation Multiplexer if needed."""
        if segmentation.is_trivial:
            parent.route(outroute, inroute)
        else:
            mod = cls(parent, name, segmentation=segmentation, accesslanes=accesslanes, **kwargs)
            mod.con("in_i", inroute)
            mod.con("out_o", outroute)
