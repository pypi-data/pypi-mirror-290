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
"""One-Time-Programmable Memory."""

from functools import cached_property

import ucdp as u
from ucdp_addr.addrspace import RWL, Access

from .mem import AMemMod
from .memtechconstraints import MemTechConstraints


class OtpMod(AMemMod):
    """One-Time-Programmable Memory."""

    access: u.ClassVar[Access] = RWL

    @cached_property
    def memtechconstraints(self) -> MemTechConstraints | None:
        """Memory Technology Constraints."""
        try:
            import ucdpmemtechconfig

            return ucdpmemtechconfig.get_otptechconstraints(self.hiername)
        except (ImportError, AttributeError):
            return None
