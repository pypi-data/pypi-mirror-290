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
Base Memory.
"""

from abc import abstractmethod
from functools import cached_property

import ucdp as u
from makolator.helper import indent
from pydantic import PositiveInt
from ucdp_addr.addrspace import RO, Access, Addrspace
from ucdp_addr.util import calc_depth_size
from ucdp_glbl.lane import Lane, Lanes, fill_lanes
from ucdp_glbl.mem import calc_slicewidths

from .memtechconstraints import MemTechConstraints
from .segmentation import Segmentation
from .types import LanesMemIoType, LanesMemPwrType, MemPwrType, MemTechType, SliceWidths
from .wordmasks import Wordmasks, cast_wordmasks, width_to_wordmasks

try:
    import ucdpmemtechconfig
except ImportError:
    ucdpmemtechconfig = None

indent4 = indent(4)


class AMemMod(u.ATailoredMod):
    """Memory Module."""

    width: PositiveInt
    """Width in Bits."""
    depth: PositiveInt = u.Field(repr=False)
    """Number of words."""
    size: u.Bytes
    """Size in Bytes."""
    slicewidths: SliceWidths | None = None
    """Data Slice Widths."""
    wordmasks: Wordmasks
    """Word Masks for 32-bit mapping."""
    accesslanes: Lanes
    """Access Lanes."""
    powerlanes: Lanes
    """Access Lanes."""

    access: u.ClassVar[Access] = RO

    def __init__(
        self,
        *args,
        width: PositiveInt,
        depth: PositiveInt | None = None,
        size: u.Bytes | None = None,
        wordmasks: Wordmasks | None = None,
        accesslanes: Lanes | None = None,
        powerlanes: Lanes | None = None,
        slicewidths: SliceWidths | None = None,
        slicewidth: int | u.Expr | None = None,
        **kwargs,
    ):
        depth, size = calc_depth_size(width, depth, size)
        size = u.Bytesize(size)
        wordmasks = cast_wordmasks(wordmasks, width=width) if wordmasks else width_to_wordmasks(width)
        accesslanes = fill_lanes(accesslanes, size, default=True)
        powerlanes = fill_lanes(powerlanes, size, default=True)
        if slicewidth and slicewidths:
            raise ValueError("'slicewidth' and 'slicewidths' are mutally exclusive.")
        if slicewidth:
            slicewidths = calc_slicewidths(width, slicewidth)
        super().__init__(
            *args,
            width=width,
            depth=depth,
            size=size,
            accesslanes=accesslanes,
            powerlanes=powerlanes,
            wordmasks=wordmasks,
            slicewidths=slicewidths,
            **kwargs,
        )

    def _build(self) -> None:
        self.add_port(u.ClkRstAnType(), "main_i")
        self.add_port(self.iotype, "io_i")
        self.add_port(self.pwrtype, "pwr_i")
        self.add_port(self.techtype, "tech_i")

    @cached_property
    def iotype(self) -> LanesMemIoType:
        """IO Type."""
        return LanesMemIoType(
            datawidth=self.width,
            writable=bool(self.access.write),
            slicewidths=self.slicewidths,
            lanes=self.accesslanes,
        )

    @cached_property
    def pwrtype(self) -> LanesMemPwrType:
        """Power Control Type."""
        type_ = LanesMemPwrType()
        for lane in self.powerlanes:
            type_.add(lane.name or "main", self.get_pwrlanetype(lane))
        return type_

    def get_pwrlanetype(self, lane: Lane) -> MemPwrType:
        """Determine Power Lane Control Type."""
        return MemPwrType()

    @cached_property
    def techtype(self) -> MemTechType:
        """Technology Parameter Power."""
        return MemTechType()

    @cached_property
    def addrspace(self) -> Addrspace:
        """Address Space."""
        return Addrspace(name=self.hiername, width=self.width, depth=self.depth, bus=self.access)

    @cached_property
    @abstractmethod
    def memtechconstraints(self) -> MemTechConstraints | None:
        """Memory Technology Constraints."""

    @cached_property
    def segmentation(self) -> Segmentation:
        """Physical Memory Segmentation."""
        constraints = self.memtechconstraints
        return Segmentation.create(
            width=self.width,
            depth=self.depth,
            slicewidths=self.slicewidths,
            accesslanes=self.accesslanes,
            powerlanes=self.powerlanes,
            constraints=constraints,
        )

    def get_overview(self) -> str:
        """Overview."""
        wordmasks = ", ".join(str(mask) for mask in self.wordmasks)
        accesslanes = ", ".join(f"{lane.name}='{lane.size}'" for lane in self.accesslanes if lane.name) or "-"
        powerlanes = ", ".join(f"{lane.name}='{lane.size}'" for lane in self.powerlanes if lane.name) or "-"
        memtechconstraints = self.memtechconstraints or "-"
        lines = [
            f"Org:         {self.addrspace.org}",
            f"Wordmasks:   {wordmasks}",
            f"Accesslanes: {accesslanes}",
            f"Powerlanes:  {powerlanes}",
            f"Constraints: {memtechconstraints}",
            "Segmentation:",
            indent4(self.segmentation.get_overview()),
        ]
        return "\n".join(lines)
