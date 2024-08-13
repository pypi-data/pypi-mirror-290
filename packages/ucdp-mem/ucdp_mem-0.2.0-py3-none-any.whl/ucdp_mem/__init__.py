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
Unified Chip Design Platform - Memories.
"""

from ucdp_glbl.attrs import Attr, Attrs, CastableAttrs, cast_attrs
from ucdp_glbl.lane import Lane

from .mem import AMemMod
from .memtechconstraints import MemTechConstraints
from .otp import OtpMod
from .ram import RamMod
from .rom import RomMod
from .segmentation import Segment, Segmentation
from .segmux import SegMuxMod

__all__ = [
    "AMemMod",
    "Attr",
    "Attrs",
    "cast_attrs",
    "CastableAttrs",
    "Lane",
    "MemTechConstraints",
    "OtpMod",
    "RamMod",
    "RomMod",
    "Segment",
    "Segmentation",
    "SegMuxMod",
]
