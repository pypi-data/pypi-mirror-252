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


class EmojiGroups(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~pyrogramv1.raw.base.messages.EmojiGroups`.

    Details:
        - Layer: ``158``
        - ID: ``0x881fb94b``

    Parameters:
        hash: ``int`` ``32-bit``
        groups: List of :obj:`EmojiGroup <pyrogramv1.raw.base.EmojiGroup>`

    See Also:
        This object can be returned by 3 methods:

        .. hlist::
            :columns: 2

            - :obj:`messages.GetEmojiGroups <pyrogramv1.raw.functions.messages.GetEmojiGroups>`
            - :obj:`messages.GetEmojiStatusGroups <pyrogramv1.raw.functions.messages.GetEmojiStatusGroups>`
            - :obj:`messages.GetEmojiProfilePhotoGroups <pyrogramv1.raw.functions.messages.GetEmojiProfilePhotoGroups>`
    """

    __slots__: List[str] = ["hash", "groups"]

    ID = 0x881fb94b
    QUALNAME = "types.messages.EmojiGroups"

    def __init__(self, *, hash: int, groups: List["raw.base.EmojiGroup"]) -> None:
        self.hash = hash  # int
        self.groups = groups  # Vector<EmojiGroup>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EmojiGroups":
        # No flags
        
        hash = Int.read(b)
        
        groups = TLObject.read(b)
        
        return EmojiGroups(hash=hash, groups=groups)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.hash))
        
        b.write(Vector(self.groups))
        
        return b.getvalue()
