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
Types.
"""

import ucdp as u
from ucdp_addr.util import calc_depth_size
from ucdp_glbl.lane import Lanes
from ucdp_glbl.mem import MemIoType, SliceWidths

__all__ = ["MemIoType", "LanesMemIoType", "MemPwrType", "MemTechType"]


class LanesMemIoType(u.AStructType):
    """Memory Lanes IO Type."""

    datawidth: int | u.Expr
    writable: bool
    slicewidths: SliceWidths | None = None
    lanes: Lanes

    def _build(self) -> None:
        width = self.datawidth
        for lane in self.lanes:
            depth = calc_depth_size(width, size=lane.size)[0]
            type_ = MemIoType(
                datawidth=width,
                addrwidth=u.log2(depth - 1),
                writable=self.writable,
                slicewidths=self.slicewidths,
                addressing="data",
            )
            self._add(lane.name or "main", type_)


class MemPwrType(u.AStructType):
    """Memory Lane Power Type."""

    def _build(self):
        pass


class LanesMemPwrType(u.DynamicStructType):
    """Memory Lanes Power Type."""


class MemTechType(u.AStructType):
    """Memory Technology Type."""

    def _build(self):
        pass
