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


class StickerSetNotModified(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~pyrogramv1.raw.base.messages.StickerSet`.

    Details:
        - Layer: ``140``
        - ID: ``0xd3f924eb``

    **No parameters required.**

    See Also:
        This object can be returned by 6 methods:

        .. hlist::
            :columns: 2

            - :obj:`messages.GetStickerSet <pyrogramv1.raw.functions.messages.GetStickerSet>`
            - :obj:`stickers.CreateStickerSet <pyrogramv1.raw.functions.stickers.CreateStickerSet>`
            - :obj:`stickers.RemoveStickerFromSet <pyrogramv1.raw.functions.stickers.RemoveStickerFromSet>`
            - :obj:`stickers.ChangeStickerPosition <pyrogramv1.raw.functions.stickers.ChangeStickerPosition>`
            - :obj:`stickers.AddStickerToSet <pyrogramv1.raw.functions.stickers.AddStickerToSet>`
            - :obj:`stickers.SetStickerSetThumb <pyrogramv1.raw.functions.stickers.SetStickerSetThumb>`
    """

    __slots__: List[str] = []

    ID = 0xd3f924eb
    QUALNAME = "types.messages.StickerSetNotModified"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StickerSetNotModified":
        # No flags
        
        return StickerSetNotModified()

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
