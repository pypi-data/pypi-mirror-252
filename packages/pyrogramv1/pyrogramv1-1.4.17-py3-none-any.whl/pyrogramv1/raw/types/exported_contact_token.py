#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogramv1.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogramv1.raw.core import TLObject
from pyrogramv1 import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class ExportedContactToken(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~pyrogramv1.raw.base.ExportedContactToken`.

    Details:
        - Layer: ``158``
        - ID: ``0x41bf109b``

    Parameters:
        url: ``str``
        expires: ``int`` ``32-bit``

    See Also:
        This object can be returned by 1 method:

        .. hlist::
            :columns: 2

            - :obj:`contacts.ExportContactToken <pyrogramv1.raw.functions.contacts.ExportContactToken>`
    """

    __slots__: List[str] = ["url", "expires"]

    ID = 0x41bf109b
    QUALNAME = "types.ExportedContactToken"

    def __init__(self, *, url: str, expires: int) -> None:
        self.url = url  # string
        self.expires = expires  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ExportedContactToken":
        # No flags
        
        url = String.read(b)
        
        expires = Int.read(b)
        
        return ExportedContactToken(url=url, expires=expires)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        b.write(Int(self.expires))
        
        return b.getvalue()
