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


class MessageActionSetSameChatWallPaper(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~pyrogramv1.raw.base.MessageAction`.

    Details:
        - Layer: ``158``
        - ID: ``0xc0787d6d``

    Parameters:
        wallpaper: :obj:`WallPaper <pyrogramv1.raw.base.WallPaper>`
    """

    __slots__: List[str] = ["wallpaper"]

    ID = 0xc0787d6d
    QUALNAME = "types.MessageActionSetSameChatWallPaper"

    def __init__(self, *, wallpaper: "raw.base.WallPaper") -> None:
        self.wallpaper = wallpaper  # WallPaper

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionSetSameChatWallPaper":
        # No flags
        
        wallpaper = TLObject.read(b)
        
        return MessageActionSetSameChatWallPaper(wallpaper=wallpaper)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.wallpaper.write())
        
        return b.getvalue()
