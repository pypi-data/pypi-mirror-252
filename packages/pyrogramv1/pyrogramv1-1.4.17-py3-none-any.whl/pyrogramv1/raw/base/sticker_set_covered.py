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

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from pyrogramv1 import raw
from pyrogramv1.raw.core import TLObject

StickerSetCovered = Union[raw.types.StickerSetCovered, raw.types.StickerSetFullCovered, raw.types.StickerSetMultiCovered, raw.types.StickerSetNoCovered]


# noinspection PyRedeclaration
class StickerSetCovered:  # type: ignore
    """This base type has 4 constructors available.

    Constructors:
        .. hlist::
            :columns: 2

            - :obj:`StickerSetCovered <pyrogramv1.raw.types.StickerSetCovered>`
            - :obj:`StickerSetFullCovered <pyrogramv1.raw.types.StickerSetFullCovered>`
            - :obj:`StickerSetMultiCovered <pyrogramv1.raw.types.StickerSetMultiCovered>`
            - :obj:`StickerSetNoCovered <pyrogramv1.raw.types.StickerSetNoCovered>`

    See Also:
        This object can be returned by 1 method:

        .. hlist::
            :columns: 2

            - :obj:`messages.GetAttachedStickers <pyrogramv1.raw.functions.messages.GetAttachedStickers>`
    """

    QUALNAME = "pyrogramv1.raw.base.StickerSetCovered"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyrogram.org/telegram/base/sticker-set-covered")
