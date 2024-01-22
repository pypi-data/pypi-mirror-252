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

RichText = Union[raw.types.TextAnchor, raw.types.TextBold, raw.types.TextConcat, raw.types.TextEmail, raw.types.TextEmpty, raw.types.TextFixed, raw.types.TextImage, raw.types.TextItalic, raw.types.TextMarked, raw.types.TextPhone, raw.types.TextPlain, raw.types.TextStrike, raw.types.TextSubscript, raw.types.TextSuperscript, raw.types.TextUnderline, raw.types.TextUrl]


# noinspection PyRedeclaration
class RichText:  # type: ignore
    """This base type has 16 constructors available.

    Constructors:
        .. hlist::
            :columns: 2

            - :obj:`TextAnchor <pyrogramv1.raw.types.TextAnchor>`
            - :obj:`TextBold <pyrogramv1.raw.types.TextBold>`
            - :obj:`TextConcat <pyrogramv1.raw.types.TextConcat>`
            - :obj:`TextEmail <pyrogramv1.raw.types.TextEmail>`
            - :obj:`TextEmpty <pyrogramv1.raw.types.TextEmpty>`
            - :obj:`TextFixed <pyrogramv1.raw.types.TextFixed>`
            - :obj:`TextImage <pyrogramv1.raw.types.TextImage>`
            - :obj:`TextItalic <pyrogramv1.raw.types.TextItalic>`
            - :obj:`TextMarked <pyrogramv1.raw.types.TextMarked>`
            - :obj:`TextPhone <pyrogramv1.raw.types.TextPhone>`
            - :obj:`TextPlain <pyrogramv1.raw.types.TextPlain>`
            - :obj:`TextStrike <pyrogramv1.raw.types.TextStrike>`
            - :obj:`TextSubscript <pyrogramv1.raw.types.TextSubscript>`
            - :obj:`TextSuperscript <pyrogramv1.raw.types.TextSuperscript>`
            - :obj:`TextUnderline <pyrogramv1.raw.types.TextUnderline>`
            - :obj:`TextUrl <pyrogramv1.raw.types.TextUrl>`
    """

    QUALNAME = "pyrogramv1.raw.base.RichText"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyrogram.org/telegram/base/rich-text")
