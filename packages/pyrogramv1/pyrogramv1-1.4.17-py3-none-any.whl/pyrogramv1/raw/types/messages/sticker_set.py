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


class StickerSet(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~pyrogramv1.raw.base.messages.StickerSet`.

    Details:
        - Layer: ``158``
        - ID: ``0x6e153f16``

    Parameters:
        set: :obj:`StickerSet <pyrogramv1.raw.base.StickerSet>`
        packs: List of :obj:`StickerPack <pyrogramv1.raw.base.StickerPack>`
        keywords: List of :obj:`StickerKeyword <pyrogramv1.raw.base.StickerKeyword>`
        documents: List of :obj:`Document <pyrogramv1.raw.base.Document>`

    See Also:
        This object can be returned by 8 methods:

        .. hlist::
            :columns: 2

            - :obj:`messages.GetStickerSet <pyrogramv1.raw.functions.messages.GetStickerSet>`
            - :obj:`stickers.CreateStickerSet <pyrogramv1.raw.functions.stickers.CreateStickerSet>`
            - :obj:`stickers.RemoveStickerFromSet <pyrogramv1.raw.functions.stickers.RemoveStickerFromSet>`
            - :obj:`stickers.ChangeStickerPosition <pyrogramv1.raw.functions.stickers.ChangeStickerPosition>`
            - :obj:`stickers.AddStickerToSet <pyrogramv1.raw.functions.stickers.AddStickerToSet>`
            - :obj:`stickers.SetStickerSetThumb <pyrogramv1.raw.functions.stickers.SetStickerSetThumb>`
            - :obj:`stickers.ChangeSticker <pyrogramv1.raw.functions.stickers.ChangeSticker>`
            - :obj:`stickers.RenameStickerSet <pyrogramv1.raw.functions.stickers.RenameStickerSet>`
    """

    __slots__: List[str] = ["set", "packs", "keywords", "documents"]

    ID = 0x6e153f16
    QUALNAME = "types.messages.StickerSet"

    def __init__(self, *, set: "raw.base.StickerSet", packs: List["raw.base.StickerPack"], keywords: List["raw.base.StickerKeyword"], documents: List["raw.base.Document"]) -> None:
        self.set = set  # StickerSet
        self.packs = packs  # Vector<StickerPack>
        self.keywords = keywords  # Vector<StickerKeyword>
        self.documents = documents  # Vector<Document>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StickerSet":
        # No flags
        
        set = TLObject.read(b)
        
        packs = TLObject.read(b)
        
        keywords = TLObject.read(b)
        
        documents = TLObject.read(b)
        
        return StickerSet(set=set, packs=packs, keywords=keywords, documents=documents)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.set.write())
        
        b.write(Vector(self.packs))
        
        b.write(Vector(self.keywords))
        
        b.write(Vector(self.documents))
        
        return b.getvalue()
