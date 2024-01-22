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


class ExportedChatlistInvite(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~pyrogramv1.raw.base.chatlists.ExportedChatlistInvite`.

    Details:
        - Layer: ``158``
        - ID: ``0x10e6e3a6``

    Parameters:
        filter: :obj:`DialogFilter <pyrogramv1.raw.base.DialogFilter>`
        invite: :obj:`ExportedChatlistInvite <pyrogramv1.raw.base.ExportedChatlistInvite>`

    See Also:
        This object can be returned by 1 method:

        .. hlist::
            :columns: 2

            - :obj:`chatlists.ExportChatlistInvite <pyrogramv1.raw.functions.chatlists.ExportChatlistInvite>`
    """

    __slots__: List[str] = ["filter", "invite"]

    ID = 0x10e6e3a6
    QUALNAME = "types.chatlists.ExportedChatlistInvite"

    def __init__(self, *, filter: "raw.base.DialogFilter", invite: "raw.base.ExportedChatlistInvite") -> None:
        self.filter = filter  # DialogFilter
        self.invite = invite  # ExportedChatlistInvite

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ExportedChatlistInvite":
        # No flags
        
        filter = TLObject.read(b)
        
        invite = TLObject.read(b)
        
        return ExportedChatlistInvite(filter=filter, invite=invite)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.filter.write())
        
        b.write(self.invite.write())
        
        return b.getvalue()
