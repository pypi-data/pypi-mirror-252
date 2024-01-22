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

MessagesFilter = Union[raw.types.InputMessagesFilterChatPhotos, raw.types.InputMessagesFilterContacts, raw.types.InputMessagesFilterDocument, raw.types.InputMessagesFilterEmpty, raw.types.InputMessagesFilterGeo, raw.types.InputMessagesFilterGif, raw.types.InputMessagesFilterMusic, raw.types.InputMessagesFilterMyMentions, raw.types.InputMessagesFilterPhoneCalls, raw.types.InputMessagesFilterPhotoVideo, raw.types.InputMessagesFilterPhotos, raw.types.InputMessagesFilterPinned, raw.types.InputMessagesFilterRoundVideo, raw.types.InputMessagesFilterRoundVoice, raw.types.InputMessagesFilterUrl, raw.types.InputMessagesFilterVideo, raw.types.InputMessagesFilterVoice]


# noinspection PyRedeclaration
class MessagesFilter:  # type: ignore
    """This base type has 17 constructors available.

    Constructors:
        .. hlist::
            :columns: 2

            - :obj:`InputMessagesFilterChatPhotos <pyrogramv1.raw.types.InputMessagesFilterChatPhotos>`
            - :obj:`InputMessagesFilterContacts <pyrogramv1.raw.types.InputMessagesFilterContacts>`
            - :obj:`InputMessagesFilterDocument <pyrogramv1.raw.types.InputMessagesFilterDocument>`
            - :obj:`InputMessagesFilterEmpty <pyrogramv1.raw.types.InputMessagesFilterEmpty>`
            - :obj:`InputMessagesFilterGeo <pyrogramv1.raw.types.InputMessagesFilterGeo>`
            - :obj:`InputMessagesFilterGif <pyrogramv1.raw.types.InputMessagesFilterGif>`
            - :obj:`InputMessagesFilterMusic <pyrogramv1.raw.types.InputMessagesFilterMusic>`
            - :obj:`InputMessagesFilterMyMentions <pyrogramv1.raw.types.InputMessagesFilterMyMentions>`
            - :obj:`InputMessagesFilterPhoneCalls <pyrogramv1.raw.types.InputMessagesFilterPhoneCalls>`
            - :obj:`InputMessagesFilterPhotoVideo <pyrogramv1.raw.types.InputMessagesFilterPhotoVideo>`
            - :obj:`InputMessagesFilterPhotos <pyrogramv1.raw.types.InputMessagesFilterPhotos>`
            - :obj:`InputMessagesFilterPinned <pyrogramv1.raw.types.InputMessagesFilterPinned>`
            - :obj:`InputMessagesFilterRoundVideo <pyrogramv1.raw.types.InputMessagesFilterRoundVideo>`
            - :obj:`InputMessagesFilterRoundVoice <pyrogramv1.raw.types.InputMessagesFilterRoundVoice>`
            - :obj:`InputMessagesFilterUrl <pyrogramv1.raw.types.InputMessagesFilterUrl>`
            - :obj:`InputMessagesFilterVideo <pyrogramv1.raw.types.InputMessagesFilterVideo>`
            - :obj:`InputMessagesFilterVoice <pyrogramv1.raw.types.InputMessagesFilterVoice>`
    """

    QUALNAME = "pyrogramv1.raw.base.MessagesFilter"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyrogram.org/telegram/base/messages-filter")
