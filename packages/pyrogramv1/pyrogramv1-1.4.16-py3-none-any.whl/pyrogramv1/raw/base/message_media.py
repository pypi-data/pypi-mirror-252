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

MessageMedia = Union[raw.types.MessageMediaContact, raw.types.MessageMediaDice, raw.types.MessageMediaDocument, raw.types.MessageMediaEmpty, raw.types.MessageMediaGame, raw.types.MessageMediaGeo, raw.types.MessageMediaGeoLive, raw.types.MessageMediaInvoice, raw.types.MessageMediaPhoto, raw.types.MessageMediaPoll, raw.types.MessageMediaUnsupported, raw.types.MessageMediaVenue, raw.types.MessageMediaWebPage]


# noinspection PyRedeclaration
class MessageMedia:  # type: ignore
    """This base type has 13 constructors available.

    Constructors:
        .. hlist::
            :columns: 2

            - :obj:`MessageMediaContact <pyrogramv1.raw.types.MessageMediaContact>`
            - :obj:`MessageMediaDice <pyrogramv1.raw.types.MessageMediaDice>`
            - :obj:`MessageMediaDocument <pyrogramv1.raw.types.MessageMediaDocument>`
            - :obj:`MessageMediaEmpty <pyrogramv1.raw.types.MessageMediaEmpty>`
            - :obj:`MessageMediaGame <pyrogramv1.raw.types.MessageMediaGame>`
            - :obj:`MessageMediaGeo <pyrogramv1.raw.types.MessageMediaGeo>`
            - :obj:`MessageMediaGeoLive <pyrogramv1.raw.types.MessageMediaGeoLive>`
            - :obj:`MessageMediaInvoice <pyrogramv1.raw.types.MessageMediaInvoice>`
            - :obj:`MessageMediaPhoto <pyrogramv1.raw.types.MessageMediaPhoto>`
            - :obj:`MessageMediaPoll <pyrogramv1.raw.types.MessageMediaPoll>`
            - :obj:`MessageMediaUnsupported <pyrogramv1.raw.types.MessageMediaUnsupported>`
            - :obj:`MessageMediaVenue <pyrogramv1.raw.types.MessageMediaVenue>`
            - :obj:`MessageMediaWebPage <pyrogramv1.raw.types.MessageMediaWebPage>`

    See Also:
        This object can be returned by 3 methods:

        .. hlist::
            :columns: 2

            - :obj:`messages.GetWebPagePreview <pyrogramv1.raw.functions.messages.GetWebPagePreview>`
            - :obj:`messages.UploadMedia <pyrogramv1.raw.functions.messages.UploadMedia>`
            - :obj:`messages.UploadImportedMedia <pyrogramv1.raw.functions.messages.UploadImportedMedia>`
    """

    QUALNAME = "pyrogramv1.raw.base.MessageMedia"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyrogram.org/telegram/base/message-media")
