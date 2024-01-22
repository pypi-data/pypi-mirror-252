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

MessageAction = Union[raw.types.MessageActionBotAllowed, raw.types.MessageActionChannelCreate, raw.types.MessageActionChannelMigrateFrom, raw.types.MessageActionChatAddUser, raw.types.MessageActionChatCreate, raw.types.MessageActionChatDeletePhoto, raw.types.MessageActionChatDeleteUser, raw.types.MessageActionChatEditPhoto, raw.types.MessageActionChatEditTitle, raw.types.MessageActionChatJoinedByLink, raw.types.MessageActionChatJoinedByRequest, raw.types.MessageActionChatMigrateTo, raw.types.MessageActionContactSignUp, raw.types.MessageActionCustomAction, raw.types.MessageActionEmpty, raw.types.MessageActionGameScore, raw.types.MessageActionGeoProximityReached, raw.types.MessageActionGiftPremium, raw.types.MessageActionGroupCall, raw.types.MessageActionGroupCallScheduled, raw.types.MessageActionHistoryClear, raw.types.MessageActionInviteToGroupCall, raw.types.MessageActionPaymentSent, raw.types.MessageActionPaymentSentMe, raw.types.MessageActionPhoneCall, raw.types.MessageActionPinMessage, raw.types.MessageActionRequestedPeer, raw.types.MessageActionScreenshotTaken, raw.types.MessageActionSecureValuesSent, raw.types.MessageActionSecureValuesSentMe, raw.types.MessageActionSetChatTheme, raw.types.MessageActionSetChatWallPaper, raw.types.MessageActionSetMessagesTTL, raw.types.MessageActionSetSameChatWallPaper, raw.types.MessageActionSuggestProfilePhoto, raw.types.MessageActionTopicCreate, raw.types.MessageActionTopicEdit, raw.types.MessageActionWebViewDataSent, raw.types.MessageActionWebViewDataSentMe]


# noinspection PyRedeclaration
class MessageAction:  # type: ignore
    """This base type has 39 constructors available.

    Constructors:
        .. hlist::
            :columns: 2

            - :obj:`MessageActionBotAllowed <pyrogramv1.raw.types.MessageActionBotAllowed>`
            - :obj:`MessageActionChannelCreate <pyrogramv1.raw.types.MessageActionChannelCreate>`
            - :obj:`MessageActionChannelMigrateFrom <pyrogramv1.raw.types.MessageActionChannelMigrateFrom>`
            - :obj:`MessageActionChatAddUser <pyrogramv1.raw.types.MessageActionChatAddUser>`
            - :obj:`MessageActionChatCreate <pyrogramv1.raw.types.MessageActionChatCreate>`
            - :obj:`MessageActionChatDeletePhoto <pyrogramv1.raw.types.MessageActionChatDeletePhoto>`
            - :obj:`MessageActionChatDeleteUser <pyrogramv1.raw.types.MessageActionChatDeleteUser>`
            - :obj:`MessageActionChatEditPhoto <pyrogramv1.raw.types.MessageActionChatEditPhoto>`
            - :obj:`MessageActionChatEditTitle <pyrogramv1.raw.types.MessageActionChatEditTitle>`
            - :obj:`MessageActionChatJoinedByLink <pyrogramv1.raw.types.MessageActionChatJoinedByLink>`
            - :obj:`MessageActionChatJoinedByRequest <pyrogramv1.raw.types.MessageActionChatJoinedByRequest>`
            - :obj:`MessageActionChatMigrateTo <pyrogramv1.raw.types.MessageActionChatMigrateTo>`
            - :obj:`MessageActionContactSignUp <pyrogramv1.raw.types.MessageActionContactSignUp>`
            - :obj:`MessageActionCustomAction <pyrogramv1.raw.types.MessageActionCustomAction>`
            - :obj:`MessageActionEmpty <pyrogramv1.raw.types.MessageActionEmpty>`
            - :obj:`MessageActionGameScore <pyrogramv1.raw.types.MessageActionGameScore>`
            - :obj:`MessageActionGeoProximityReached <pyrogramv1.raw.types.MessageActionGeoProximityReached>`
            - :obj:`MessageActionGiftPremium <pyrogramv1.raw.types.MessageActionGiftPremium>`
            - :obj:`MessageActionGroupCall <pyrogramv1.raw.types.MessageActionGroupCall>`
            - :obj:`MessageActionGroupCallScheduled <pyrogramv1.raw.types.MessageActionGroupCallScheduled>`
            - :obj:`MessageActionHistoryClear <pyrogramv1.raw.types.MessageActionHistoryClear>`
            - :obj:`MessageActionInviteToGroupCall <pyrogramv1.raw.types.MessageActionInviteToGroupCall>`
            - :obj:`MessageActionPaymentSent <pyrogramv1.raw.types.MessageActionPaymentSent>`
            - :obj:`MessageActionPaymentSentMe <pyrogramv1.raw.types.MessageActionPaymentSentMe>`
            - :obj:`MessageActionPhoneCall <pyrogramv1.raw.types.MessageActionPhoneCall>`
            - :obj:`MessageActionPinMessage <pyrogramv1.raw.types.MessageActionPinMessage>`
            - :obj:`MessageActionRequestedPeer <pyrogramv1.raw.types.MessageActionRequestedPeer>`
            - :obj:`MessageActionScreenshotTaken <pyrogramv1.raw.types.MessageActionScreenshotTaken>`
            - :obj:`MessageActionSecureValuesSent <pyrogramv1.raw.types.MessageActionSecureValuesSent>`
            - :obj:`MessageActionSecureValuesSentMe <pyrogramv1.raw.types.MessageActionSecureValuesSentMe>`
            - :obj:`MessageActionSetChatTheme <pyrogramv1.raw.types.MessageActionSetChatTheme>`
            - :obj:`MessageActionSetChatWallPaper <pyrogramv1.raw.types.MessageActionSetChatWallPaper>`
            - :obj:`MessageActionSetMessagesTTL <pyrogramv1.raw.types.MessageActionSetMessagesTTL>`
            - :obj:`MessageActionSetSameChatWallPaper <pyrogramv1.raw.types.MessageActionSetSameChatWallPaper>`
            - :obj:`MessageActionSuggestProfilePhoto <pyrogramv1.raw.types.MessageActionSuggestProfilePhoto>`
            - :obj:`MessageActionTopicCreate <pyrogramv1.raw.types.MessageActionTopicCreate>`
            - :obj:`MessageActionTopicEdit <pyrogramv1.raw.types.MessageActionTopicEdit>`
            - :obj:`MessageActionWebViewDataSent <pyrogramv1.raw.types.MessageActionWebViewDataSent>`
            - :obj:`MessageActionWebViewDataSentMe <pyrogramv1.raw.types.MessageActionWebViewDataSentMe>`
    """

    QUALNAME = "pyrogramv1.raw.base.MessageAction"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyrogram.org/telegram/base/message-action")
