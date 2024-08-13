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

import ucdp as u
import ucdp_mem as um
from test2ref import assert_refdata


class HdlFileList(u.ModFileList):
    """HDL File Lists."""

    name: str = "hdl"
    filepaths: u.ToPaths = ("$PRJROOT/{mod.modname}.sv",)
    template_filepaths: u.ToPaths = ("sv.mako",)


class SegMuxMod(um.SegMuxMod):
    """Segmentation Multiplexer."""

    filelists: u.ClassVar[u.ModFileLists] = (HdlFileList(gen="full", template_filepaths=("segmux.sv.mako",)),)


class RomMod(um.RomMod):
    """ROM Module."""

    filelists: u.ClassVar[u.ModFileLists] = (HdlFileList(gen="full"),)

    def _build(self):
        super()._build()
        SegMuxMod.create(self, "u_mux", self.segmentation, self.accesslanes, "io_i", "create(mem_s)", writable=False)


class RamMod(um.RamMod):
    """RAM Module."""

    filelists: u.ClassVar[u.ModFileLists] = (HdlFileList(gen="full"),)

    def _build(self):
        super()._build()
        SegMuxMod.create(self, "u_mux", self.segmentation, self.accesslanes, "io_i", "create(mem_s)", addrgate=True)


class OtpMod(um.OtpMod):
    """OTP Module."""

    filelists: u.ClassVar[u.ModFileLists] = (HdlFileList(gen="full"),)


class AllMod(u.AMod):
    """All Modules."""

    filelists: u.ClassVar[u.ModFileLists] = (HdlFileList(gen="full"),)

    def _build(self):
        accesslanes = (
            um.Lane(name="one", size="8k"),
            um.Lane(name="two"),
        )
        powerlanes = (
            um.Lane(name="one", size="4k"),
            um.Lane(name="two"),
        )

        OtpMod(self, "u_otp0", depth=100, width=8)
        OtpMod(self, "u_otp1", size=8 * 1024, width=64)

        RomMod(self, "u_rom0", depth=100, width=8)
        RomMod(self, "u_rom1", size=8 * 1024, width=64)
        RomMod(self, "u_rom2", size=4 * 8 * 1024, width=64, accesslanes=accesslanes)
        RomMod(self, "u_rom3", size=8 * 1024, width=16, powerlanes=powerlanes)
        RomMod(self, "u_rom4", size="40KB", width=16, powerlanes=powerlanes, accesslanes=accesslanes)
        RomMod(self, "u_rom5", depth=10240, width=18)
        # RomMod(self, "u_rom6", depth=1981, width=77)

        RamMod(self, "u_ram0", depth=100, width=8)
        RamMod(self, "u_ram1", size=8 * 1024, width=64)
        RamMod(self, "u_ram2", size=4 * 8 * 1024, width=64, accesslanes=accesslanes)
        RamMod(self, "u_ram3", size=8 * 1024, width=16, powerlanes=powerlanes)
        RamMod(self, "u_ram4", size="40KB", width=16, powerlanes=powerlanes, accesslanes=accesslanes)
        RamMod(self, "u_ram5", depth=10240, width=18)
        # RamMod(self, "u_ram6", depth=1981, width=77)
        RamMod(self, "u_ram7", size=1024, width=64, slicewidth=8)
        RamMod(self, "u_ram8", size=1024, width=68, slicewidth=4)


def test_all(prjroot):
    """All Modules."""
    mod = AllMod()
    u.generate(mod, "*")
    assert_refdata(test_all, prjroot)


def test_all_configured(prjroot, techconfig):
    """All Modules with Configured."""
    mod = AllMod()
    u.generate(mod, "*")
    assert_refdata(test_all_configured, prjroot)
