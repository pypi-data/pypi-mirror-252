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


class UpdateShort(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~pyrogramv1.raw.base.Updates`.

    Details:
        - Layer: ``158``
        - ID: ``0x78d4dec1``

    Parameters:
        update: :obj:`Update <pyrogramv1.raw.base.Update>`
        date: ``int`` ``32-bit``

    See Also:
        This object can be returned by 87 methods:

        .. hlist::
            :columns: 2

            - :obj:`account.GetNotifyExceptions <pyrogramv1.raw.functions.account.GetNotifyExceptions>`
            - :obj:`contacts.DeleteContacts <pyrogramv1.raw.functions.contacts.DeleteContacts>`
            - :obj:`contacts.AddContact <pyrogramv1.raw.functions.contacts.AddContact>`
            - :obj:`contacts.AcceptContact <pyrogramv1.raw.functions.contacts.AcceptContact>`
            - :obj:`contacts.GetLocated <pyrogramv1.raw.functions.contacts.GetLocated>`
            - :obj:`contacts.BlockFromReplies <pyrogramv1.raw.functions.contacts.BlockFromReplies>`
            - :obj:`messages.SendMessage <pyrogramv1.raw.functions.messages.SendMessage>`
            - :obj:`messages.SendMedia <pyrogramv1.raw.functions.messages.SendMedia>`
            - :obj:`messages.ForwardMessages <pyrogramv1.raw.functions.messages.ForwardMessages>`
            - :obj:`messages.EditChatTitle <pyrogramv1.raw.functions.messages.EditChatTitle>`
            - :obj:`messages.EditChatPhoto <pyrogramv1.raw.functions.messages.EditChatPhoto>`
            - :obj:`messages.AddChatUser <pyrogramv1.raw.functions.messages.AddChatUser>`
            - :obj:`messages.DeleteChatUser <pyrogramv1.raw.functions.messages.DeleteChatUser>`
            - :obj:`messages.CreateChat <pyrogramv1.raw.functions.messages.CreateChat>`
            - :obj:`messages.ImportChatInvite <pyrogramv1.raw.functions.messages.ImportChatInvite>`
            - :obj:`messages.StartBot <pyrogramv1.raw.functions.messages.StartBot>`
            - :obj:`messages.MigrateChat <pyrogramv1.raw.functions.messages.MigrateChat>`
            - :obj:`messages.SendInlineBotResult <pyrogramv1.raw.functions.messages.SendInlineBotResult>`
            - :obj:`messages.EditMessage <pyrogramv1.raw.functions.messages.EditMessage>`
            - :obj:`messages.GetAllDrafts <pyrogramv1.raw.functions.messages.GetAllDrafts>`
            - :obj:`messages.SetGameScore <pyrogramv1.raw.functions.messages.SetGameScore>`
            - :obj:`messages.SendScreenshotNotification <pyrogramv1.raw.functions.messages.SendScreenshotNotification>`
            - :obj:`messages.SendMultiMedia <pyrogramv1.raw.functions.messages.SendMultiMedia>`
            - :obj:`messages.UpdatePinnedMessage <pyrogramv1.raw.functions.messages.UpdatePinnedMessage>`
            - :obj:`messages.SendVote <pyrogramv1.raw.functions.messages.SendVote>`
            - :obj:`messages.GetPollResults <pyrogramv1.raw.functions.messages.GetPollResults>`
            - :obj:`messages.EditChatDefaultBannedRights <pyrogramv1.raw.functions.messages.EditChatDefaultBannedRights>`
            - :obj:`messages.SendScheduledMessages <pyrogramv1.raw.functions.messages.SendScheduledMessages>`
            - :obj:`messages.DeleteScheduledMessages <pyrogramv1.raw.functions.messages.DeleteScheduledMessages>`
            - :obj:`messages.SetHistoryTTL <pyrogramv1.raw.functions.messages.SetHistoryTTL>`
            - :obj:`messages.SetChatTheme <pyrogramv1.raw.functions.messages.SetChatTheme>`
            - :obj:`messages.HideChatJoinRequest <pyrogramv1.raw.functions.messages.HideChatJoinRequest>`
            - :obj:`messages.HideAllChatJoinRequests <pyrogramv1.raw.functions.messages.HideAllChatJoinRequests>`
            - :obj:`messages.ToggleNoForwards <pyrogramv1.raw.functions.messages.ToggleNoForwards>`
            - :obj:`messages.SendReaction <pyrogramv1.raw.functions.messages.SendReaction>`
            - :obj:`messages.GetMessagesReactions <pyrogramv1.raw.functions.messages.GetMessagesReactions>`
            - :obj:`messages.SetChatAvailableReactions <pyrogramv1.raw.functions.messages.SetChatAvailableReactions>`
            - :obj:`messages.SendWebViewData <pyrogramv1.raw.functions.messages.SendWebViewData>`
            - :obj:`messages.GetExtendedMedia <pyrogramv1.raw.functions.messages.GetExtendedMedia>`
            - :obj:`messages.SendBotRequestedPeer <pyrogramv1.raw.functions.messages.SendBotRequestedPeer>`
            - :obj:`messages.SetChatWallPaper <pyrogramv1.raw.functions.messages.SetChatWallPaper>`
            - :obj:`help.GetAppChangelog <pyrogramv1.raw.functions.help.GetAppChangelog>`
            - :obj:`channels.CreateChannel <pyrogramv1.raw.functions.channels.CreateChannel>`
            - :obj:`channels.EditAdmin <pyrogramv1.raw.functions.channels.EditAdmin>`
            - :obj:`channels.EditTitle <pyrogramv1.raw.functions.channels.EditTitle>`
            - :obj:`channels.EditPhoto <pyrogramv1.raw.functions.channels.EditPhoto>`
            - :obj:`channels.JoinChannel <pyrogramv1.raw.functions.channels.JoinChannel>`
            - :obj:`channels.LeaveChannel <pyrogramv1.raw.functions.channels.LeaveChannel>`
            - :obj:`channels.InviteToChannel <pyrogramv1.raw.functions.channels.InviteToChannel>`
            - :obj:`channels.DeleteChannel <pyrogramv1.raw.functions.channels.DeleteChannel>`
            - :obj:`channels.ToggleSignatures <pyrogramv1.raw.functions.channels.ToggleSignatures>`
            - :obj:`channels.EditBanned <pyrogramv1.raw.functions.channels.EditBanned>`
            - :obj:`channels.DeleteHistory <pyrogramv1.raw.functions.channels.DeleteHistory>`
            - :obj:`channels.TogglePreHistoryHidden <pyrogramv1.raw.functions.channels.TogglePreHistoryHidden>`
            - :obj:`channels.EditCreator <pyrogramv1.raw.functions.channels.EditCreator>`
            - :obj:`channels.ToggleSlowMode <pyrogramv1.raw.functions.channels.ToggleSlowMode>`
            - :obj:`channels.ConvertToGigagroup <pyrogramv1.raw.functions.channels.ConvertToGigagroup>`
            - :obj:`channels.ToggleJoinToSend <pyrogramv1.raw.functions.channels.ToggleJoinToSend>`
            - :obj:`channels.ToggleJoinRequest <pyrogramv1.raw.functions.channels.ToggleJoinRequest>`
            - :obj:`channels.ToggleForum <pyrogramv1.raw.functions.channels.ToggleForum>`
            - :obj:`channels.CreateForumTopic <pyrogramv1.raw.functions.channels.CreateForumTopic>`
            - :obj:`channels.EditForumTopic <pyrogramv1.raw.functions.channels.EditForumTopic>`
            - :obj:`channels.UpdatePinnedForumTopic <pyrogramv1.raw.functions.channels.UpdatePinnedForumTopic>`
            - :obj:`channels.ReorderPinnedForumTopics <pyrogramv1.raw.functions.channels.ReorderPinnedForumTopics>`
            - :obj:`channels.ToggleAntiSpam <pyrogramv1.raw.functions.channels.ToggleAntiSpam>`
            - :obj:`channels.ToggleParticipantsHidden <pyrogramv1.raw.functions.channels.ToggleParticipantsHidden>`
            - :obj:`payments.AssignAppStoreTransaction <pyrogramv1.raw.functions.payments.AssignAppStoreTransaction>`
            - :obj:`payments.AssignPlayMarketTransaction <pyrogramv1.raw.functions.payments.AssignPlayMarketTransaction>`
            - :obj:`phone.DiscardCall <pyrogramv1.raw.functions.phone.DiscardCall>`
            - :obj:`phone.SetCallRating <pyrogramv1.raw.functions.phone.SetCallRating>`
            - :obj:`phone.CreateGroupCall <pyrogramv1.raw.functions.phone.CreateGroupCall>`
            - :obj:`phone.JoinGroupCall <pyrogramv1.raw.functions.phone.JoinGroupCall>`
            - :obj:`phone.LeaveGroupCall <pyrogramv1.raw.functions.phone.LeaveGroupCall>`
            - :obj:`phone.InviteToGroupCall <pyrogramv1.raw.functions.phone.InviteToGroupCall>`
            - :obj:`phone.DiscardGroupCall <pyrogramv1.raw.functions.phone.DiscardGroupCall>`
            - :obj:`phone.ToggleGroupCallSettings <pyrogramv1.raw.functions.phone.ToggleGroupCallSettings>`
            - :obj:`phone.ToggleGroupCallRecord <pyrogramv1.raw.functions.phone.ToggleGroupCallRecord>`
            - :obj:`phone.EditGroupCallParticipant <pyrogramv1.raw.functions.phone.EditGroupCallParticipant>`
            - :obj:`phone.EditGroupCallTitle <pyrogramv1.raw.functions.phone.EditGroupCallTitle>`
            - :obj:`phone.ToggleGroupCallStartSubscription <pyrogramv1.raw.functions.phone.ToggleGroupCallStartSubscription>`
            - :obj:`phone.StartScheduledGroupCall <pyrogramv1.raw.functions.phone.StartScheduledGroupCall>`
            - :obj:`phone.JoinGroupCallPresentation <pyrogramv1.raw.functions.phone.JoinGroupCallPresentation>`
            - :obj:`phone.LeaveGroupCallPresentation <pyrogramv1.raw.functions.phone.LeaveGroupCallPresentation>`
            - :obj:`folders.EditPeerFolders <pyrogramv1.raw.functions.folders.EditPeerFolders>`
            - :obj:`chatlists.JoinChatlistInvite <pyrogramv1.raw.functions.chatlists.JoinChatlistInvite>`
            - :obj:`chatlists.JoinChatlistUpdates <pyrogramv1.raw.functions.chatlists.JoinChatlistUpdates>`
            - :obj:`chatlists.LeaveChatlist <pyrogramv1.raw.functions.chatlists.LeaveChatlist>`
    """

    __slots__: List[str] = ["update", "date"]

    ID = 0x78d4dec1
    QUALNAME = "types.UpdateShort"

    def __init__(self, *, update: "raw.base.Update", date: int) -> None:
        self.update = update  # Update
        self.date = date  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateShort":
        # No flags
        
        update = TLObject.read(b)
        
        date = Int.read(b)
        
        return UpdateShort(update=update, date=date)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.update.write())
        
        b.write(Int(self.date))
        
        return b.getvalue()
