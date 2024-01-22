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

InputStickerSet = Union[raw.types.InputStickerSetAnimatedEmoji, raw.types.InputStickerSetAnimatedEmojiAnimations, raw.types.InputStickerSetDice, raw.types.InputStickerSetEmojiDefaultStatuses, raw.types.InputStickerSetEmojiDefaultTopicIcons, raw.types.InputStickerSetEmojiGenericAnimations, raw.types.InputStickerSetEmpty, raw.types.InputStickerSetID, raw.types.InputStickerSetPremiumGifts, raw.types.InputStickerSetShortName]


# noinspection PyRedeclaration
class InputStickerSet:  # type: ignore
    """This base type has 10 constructors available.

    Constructors:
        .. hlist::
            :columns: 2

            - :obj:`InputStickerSetAnimatedEmoji <pyrogramv1.raw.types.InputStickerSetAnimatedEmoji>`
            - :obj:`InputStickerSetAnimatedEmojiAnimations <pyrogramv1.raw.types.InputStickerSetAnimatedEmojiAnimations>`
            - :obj:`InputStickerSetDice <pyrogramv1.raw.types.InputStickerSetDice>`
            - :obj:`InputStickerSetEmojiDefaultStatuses <pyrogramv1.raw.types.InputStickerSetEmojiDefaultStatuses>`
            - :obj:`InputStickerSetEmojiDefaultTopicIcons <pyrogramv1.raw.types.InputStickerSetEmojiDefaultTopicIcons>`
            - :obj:`InputStickerSetEmojiGenericAnimations <pyrogramv1.raw.types.InputStickerSetEmojiGenericAnimations>`
            - :obj:`InputStickerSetEmpty <pyrogramv1.raw.types.InputStickerSetEmpty>`
            - :obj:`InputStickerSetID <pyrogramv1.raw.types.InputStickerSetID>`
            - :obj:`InputStickerSetPremiumGifts <pyrogramv1.raw.types.InputStickerSetPremiumGifts>`
            - :obj:`InputStickerSetShortName <pyrogramv1.raw.types.InputStickerSetShortName>`
    """

    QUALNAME = "pyrogramv1.raw.base.InputStickerSet"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyrogram.org/telegram/base/input-sticker-set")
