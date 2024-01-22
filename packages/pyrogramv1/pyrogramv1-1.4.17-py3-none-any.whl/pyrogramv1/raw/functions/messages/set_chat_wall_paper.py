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


class SetChatWallPaper(TLObject):  # type: ignore
    """Telegram API method.

    Details:
        - Layer: ``158``
        - ID: ``0x8ffacae1``

    Parameters:
        peer: :obj:`InputPeer <pyrogramv1.raw.base.InputPeer>`
        wallpaper (optional): :obj:`InputWallPaper <pyrogramv1.raw.base.InputWallPaper>`
        settings (optional): :obj:`WallPaperSettings <pyrogramv1.raw.base.WallPaperSettings>`
        id (optional): ``int`` ``32-bit``

    Returns:
        :obj:`Updates <pyrogramv1.raw.base.Updates>`
    """

    __slots__: List[str] = ["peer", "wallpaper", "settings", "id"]

    ID = 0x8ffacae1
    QUALNAME = "functions.messages.SetChatWallPaper"

    def __init__(self, *, peer: "raw.base.InputPeer", wallpaper: "raw.base.InputWallPaper" = None, settings: "raw.base.WallPaperSettings" = None, id: Optional[int] = None) -> None:
        self.peer = peer  # InputPeer
        self.wallpaper = wallpaper  # flags.0?InputWallPaper
        self.settings = settings  # flags.2?WallPaperSettings
        self.id = id  # flags.1?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SetChatWallPaper":
        
        flags = Int.read(b)
        
        peer = TLObject.read(b)
        
        wallpaper = TLObject.read(b) if flags & (1 << 0) else None
        
        settings = TLObject.read(b) if flags & (1 << 2) else None
        
        id = Int.read(b) if flags & (1 << 1) else None
        return SetChatWallPaper(peer=peer, wallpaper=wallpaper, settings=settings, id=id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.wallpaper is not None else 0
        flags |= (1 << 2) if self.settings is not None else 0
        flags |= (1 << 1) if self.id is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        if self.wallpaper is not None:
            b.write(self.wallpaper.write())
        
        if self.settings is not None:
            b.write(self.settings.write())
        
        if self.id is not None:
            b.write(Int(self.id))
        
        return b.getvalue()
