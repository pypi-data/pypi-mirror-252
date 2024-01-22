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

EmojiGroups = Union[raw.types.messages.EmojiGroups, raw.types.messages.EmojiGroupsNotModified]


# noinspection PyRedeclaration
class EmojiGroups:  # type: ignore
    """This base type has 2 constructors available.

    Constructors:
        .. hlist::
            :columns: 2

            - :obj:`messages.EmojiGroups <pyrogramv1.raw.types.messages.EmojiGroups>`
            - :obj:`messages.EmojiGroupsNotModified <pyrogramv1.raw.types.messages.EmojiGroupsNotModified>`

    See Also:
        This object can be returned by 3 methods:

        .. hlist::
            :columns: 2

            - :obj:`messages.GetEmojiGroups <pyrogramv1.raw.functions.messages.GetEmojiGroups>`
            - :obj:`messages.GetEmojiStatusGroups <pyrogramv1.raw.functions.messages.GetEmojiStatusGroups>`
            - :obj:`messages.GetEmojiProfilePhotoGroups <pyrogramv1.raw.functions.messages.GetEmojiProfilePhotoGroups>`
    """

    QUALNAME = "pyrogramv1.raw.base.messages.EmojiGroups"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyrogram.org/telegram/base/emoji-groups")
