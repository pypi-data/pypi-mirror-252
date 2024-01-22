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


class ForumTopics(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~pyrogramv1.raw.base.messages.ForumTopics`.

    Details:
        - Layer: ``158``
        - ID: ``0x367617d3``

    Parameters:
        count: ``int`` ``32-bit``
        topics: List of :obj:`ForumTopic <pyrogramv1.raw.base.ForumTopic>`
        messages: List of :obj:`Message <pyrogramv1.raw.base.Message>`
        chats: List of :obj:`Chat <pyrogramv1.raw.base.Chat>`
        users: List of :obj:`User <pyrogramv1.raw.base.User>`
        pts: ``int`` ``32-bit``
        order_by_create_date (optional): ``bool``

    See Also:
        This object can be returned by 2 methods:

        .. hlist::
            :columns: 2

            - :obj:`channels.GetForumTopics <pyrogramv1.raw.functions.channels.GetForumTopics>`
            - :obj:`channels.GetForumTopicsByID <pyrogramv1.raw.functions.channels.GetForumTopicsByID>`
    """

    __slots__: List[str] = ["count", "topics", "messages", "chats", "users", "pts", "order_by_create_date"]

    ID = 0x367617d3
    QUALNAME = "types.messages.ForumTopics"

    def __init__(self, *, count: int, topics: List["raw.base.ForumTopic"], messages: List["raw.base.Message"], chats: List["raw.base.Chat"], users: List["raw.base.User"], pts: int, order_by_create_date: Optional[bool] = None) -> None:
        self.count = count  # int
        self.topics = topics  # Vector<ForumTopic>
        self.messages = messages  # Vector<Message>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>
        self.pts = pts  # int
        self.order_by_create_date = order_by_create_date  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ForumTopics":
        
        flags = Int.read(b)
        
        order_by_create_date = True if flags & (1 << 0) else False
        count = Int.read(b)
        
        topics = TLObject.read(b)
        
        messages = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        pts = Int.read(b)
        
        return ForumTopics(count=count, topics=topics, messages=messages, chats=chats, users=users, pts=pts, order_by_create_date=order_by_create_date)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.order_by_create_date else 0
        b.write(Int(flags))
        
        b.write(Int(self.count))
        
        b.write(Vector(self.topics))
        
        b.write(Vector(self.messages))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        b.write(Int(self.pts))
        
        return b.getvalue()
