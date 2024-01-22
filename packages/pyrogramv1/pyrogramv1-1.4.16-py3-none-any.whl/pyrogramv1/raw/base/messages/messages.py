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

Messages = Union[raw.types.messages.ChannelMessages, raw.types.messages.Messages, raw.types.messages.MessagesNotModified, raw.types.messages.MessagesSlice]


# noinspection PyRedeclaration
class Messages:  # type: ignore
    """This base type has 4 constructors available.

    Constructors:
        .. hlist::
            :columns: 2

            - :obj:`messages.ChannelMessages <pyrogramv1.raw.types.messages.ChannelMessages>`
            - :obj:`messages.Messages <pyrogramv1.raw.types.messages.Messages>`
            - :obj:`messages.MessagesNotModified <pyrogramv1.raw.types.messages.MessagesNotModified>`
            - :obj:`messages.MessagesSlice <pyrogramv1.raw.types.messages.MessagesSlice>`

    See Also:
        This object can be returned by 13 methods:

        .. hlist::
            :columns: 2

            - :obj:`messages.GetMessages <pyrogramv1.raw.functions.messages.GetMessages>`
            - :obj:`messages.GetHistory <pyrogramv1.raw.functions.messages.GetHistory>`
            - :obj:`messages.Search <pyrogramv1.raw.functions.messages.Search>`
            - :obj:`messages.SearchGlobal <pyrogramv1.raw.functions.messages.SearchGlobal>`
            - :obj:`messages.GetUnreadMentions <pyrogramv1.raw.functions.messages.GetUnreadMentions>`
            - :obj:`messages.GetRecentLocations <pyrogramv1.raw.functions.messages.GetRecentLocations>`
            - :obj:`messages.GetScheduledHistory <pyrogramv1.raw.functions.messages.GetScheduledHistory>`
            - :obj:`messages.GetScheduledMessages <pyrogramv1.raw.functions.messages.GetScheduledMessages>`
            - :obj:`messages.GetReplies <pyrogramv1.raw.functions.messages.GetReplies>`
            - :obj:`messages.GetUnreadReactions <pyrogramv1.raw.functions.messages.GetUnreadReactions>`
            - :obj:`messages.SearchSentMedia <pyrogramv1.raw.functions.messages.SearchSentMedia>`
            - :obj:`channels.GetMessages <pyrogramv1.raw.functions.channels.GetMessages>`
            - :obj:`stats.GetMessagePublicForwards <pyrogramv1.raw.functions.stats.GetMessagePublicForwards>`
    """

    QUALNAME = "pyrogramv1.raw.base.messages.Messages"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyrogram.org/telegram/base/messages")
