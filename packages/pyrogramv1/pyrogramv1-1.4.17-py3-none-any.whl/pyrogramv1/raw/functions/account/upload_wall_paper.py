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


class UploadWallPaper(TLObject):  # type: ignore
    """Telegram API method.

    Details:
        - Layer: ``158``
        - ID: ``0xe39a8f03``

    Parameters:
        file: :obj:`InputFile <pyrogramv1.raw.base.InputFile>`
        mime_type: ``str``
        settings: :obj:`WallPaperSettings <pyrogramv1.raw.base.WallPaperSettings>`
        for_chat (optional): ``bool``

    Returns:
        :obj:`WallPaper <pyrogramv1.raw.base.WallPaper>`
    """

    __slots__: List[str] = ["file", "mime_type", "settings", "for_chat"]

    ID = 0xe39a8f03
    QUALNAME = "functions.account.UploadWallPaper"

    def __init__(self, *, file: "raw.base.InputFile", mime_type: str, settings: "raw.base.WallPaperSettings", for_chat: Optional[bool] = None) -> None:
        self.file = file  # InputFile
        self.mime_type = mime_type  # string
        self.settings = settings  # WallPaperSettings
        self.for_chat = for_chat  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UploadWallPaper":
        
        flags = Int.read(b)
        
        for_chat = True if flags & (1 << 0) else False
        file = TLObject.read(b)
        
        mime_type = String.read(b)
        
        settings = TLObject.read(b)
        
        return UploadWallPaper(file=file, mime_type=mime_type, settings=settings, for_chat=for_chat)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.for_chat else 0
        b.write(Int(flags))
        
        b.write(self.file.write())
        
        b.write(String(self.mime_type))
        
        b.write(self.settings.write())
        
        return b.getvalue()
