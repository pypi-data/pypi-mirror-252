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

JSONValue = Union[raw.types.JsonArray, raw.types.JsonBool, raw.types.JsonNull, raw.types.JsonNumber, raw.types.JsonObject, raw.types.JsonString]


# noinspection PyRedeclaration
class JSONValue:  # type: ignore
    """This base type has 6 constructors available.

    Constructors:
        .. hlist::
            :columns: 2

            - :obj:`JsonArray <pyrogramv1.raw.types.JsonArray>`
            - :obj:`JsonBool <pyrogramv1.raw.types.JsonBool>`
            - :obj:`JsonNull <pyrogramv1.raw.types.JsonNull>`
            - :obj:`JsonNumber <pyrogramv1.raw.types.JsonNumber>`
            - :obj:`JsonObject <pyrogramv1.raw.types.JsonObject>`
            - :obj:`JsonString <pyrogramv1.raw.types.JsonString>`
    """

    QUALNAME = "pyrogramv1.raw.base.JSONValue"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyrogram.org/telegram/base/json-value")
