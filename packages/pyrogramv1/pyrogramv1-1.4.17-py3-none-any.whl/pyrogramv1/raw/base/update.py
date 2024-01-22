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

Update = Union[raw.types.UpdateAttachMenuBots, raw.types.UpdateAutoSaveSettings, raw.types.UpdateBotCallbackQuery, raw.types.UpdateBotChatInviteRequester, raw.types.UpdateBotCommands, raw.types.UpdateBotInlineQuery, raw.types.UpdateBotInlineSend, raw.types.UpdateBotMenuButton, raw.types.UpdateBotPrecheckoutQuery, raw.types.UpdateBotShippingQuery, raw.types.UpdateBotStopped, raw.types.UpdateBotWebhookJSON, raw.types.UpdateBotWebhookJSONQuery, raw.types.UpdateChannel, raw.types.UpdateChannelAvailableMessages, raw.types.UpdateChannelMessageForwards, raw.types.UpdateChannelMessageViews, raw.types.UpdateChannelParticipant, raw.types.UpdateChannelPinnedTopic, raw.types.UpdateChannelPinnedTopics, raw.types.UpdateChannelReadMessagesContents, raw.types.UpdateChannelTooLong, raw.types.UpdateChannelUserTyping, raw.types.UpdateChannelWebPage, raw.types.UpdateChat, raw.types.UpdateChatDefaultBannedRights, raw.types.UpdateChatParticipant, raw.types.UpdateChatParticipantAdd, raw.types.UpdateChatParticipantAdmin, raw.types.UpdateChatParticipantDelete, raw.types.UpdateChatParticipants, raw.types.UpdateChatUserTyping, raw.types.UpdateConfig, raw.types.UpdateContactsReset, raw.types.UpdateDcOptions, raw.types.UpdateDeleteChannelMessages, raw.types.UpdateDeleteMessages, raw.types.UpdateDeleteScheduledMessages, raw.types.UpdateDialogFilter, raw.types.UpdateDialogFilterOrder, raw.types.UpdateDialogFilters, raw.types.UpdateDialogPinned, raw.types.UpdateDialogUnreadMark, raw.types.UpdateDraftMessage, raw.types.UpdateEditChannelMessage, raw.types.UpdateEditMessage, raw.types.UpdateEncryptedChatTyping, raw.types.UpdateEncryptedMessagesRead, raw.types.UpdateEncryption, raw.types.UpdateFavedStickers, raw.types.UpdateFolderPeers, raw.types.UpdateGeoLiveViewed, raw.types.UpdateGroupCall, raw.types.UpdateGroupCallConnection, raw.types.UpdateGroupCallParticipants, raw.types.UpdateGroupInvitePrivacyForbidden, raw.types.UpdateInlineBotCallbackQuery, raw.types.UpdateLangPack, raw.types.UpdateLangPackTooLong, raw.types.UpdateLoginToken, raw.types.UpdateMessageExtendedMedia, raw.types.UpdateMessageID, raw.types.UpdateMessagePoll, raw.types.UpdateMessagePollVote, raw.types.UpdateMessageReactions, raw.types.UpdateMoveStickerSetToTop, raw.types.UpdateNewChannelMessage, raw.types.UpdateNewEncryptedMessage, raw.types.UpdateNewMessage, raw.types.UpdateNewScheduledMessage, raw.types.UpdateNewStickerSet, raw.types.UpdateNotifySettings, raw.types.UpdatePeerBlocked, raw.types.UpdatePeerHistoryTTL, raw.types.UpdatePeerLocated, raw.types.UpdatePeerSettings, raw.types.UpdatePendingJoinRequests, raw.types.UpdatePhoneCall, raw.types.UpdatePhoneCallSignalingData, raw.types.UpdatePinnedChannelMessages, raw.types.UpdatePinnedDialogs, raw.types.UpdatePinnedMessages, raw.types.UpdatePrivacy, raw.types.UpdatePtsChanged, raw.types.UpdateReadChannelDiscussionInbox, raw.types.UpdateReadChannelDiscussionOutbox, raw.types.UpdateReadChannelInbox, raw.types.UpdateReadChannelOutbox, raw.types.UpdateReadFeaturedEmojiStickers, raw.types.UpdateReadFeaturedStickers, raw.types.UpdateReadHistoryInbox, raw.types.UpdateReadHistoryOutbox, raw.types.UpdateReadMessagesContents, raw.types.UpdateRecentEmojiStatuses, raw.types.UpdateRecentReactions, raw.types.UpdateRecentStickers, raw.types.UpdateSavedGifs, raw.types.UpdateSavedRingtones, raw.types.UpdateServiceNotification, raw.types.UpdateStickerSets, raw.types.UpdateStickerSetsOrder, raw.types.UpdateTheme, raw.types.UpdateTranscribedAudio, raw.types.UpdateUser, raw.types.UpdateUserEmojiStatus, raw.types.UpdateUserName, raw.types.UpdateUserPhone, raw.types.UpdateUserStatus, raw.types.UpdateUserTyping, raw.types.UpdateWebPage, raw.types.UpdateWebViewResultSent]


# noinspection PyRedeclaration
class Update:  # type: ignore
    """This base type has 111 constructors available.

    Constructors:
        .. hlist::
            :columns: 2

            - :obj:`UpdateAttachMenuBots <pyrogramv1.raw.types.UpdateAttachMenuBots>`
            - :obj:`UpdateAutoSaveSettings <pyrogramv1.raw.types.UpdateAutoSaveSettings>`
            - :obj:`UpdateBotCallbackQuery <pyrogramv1.raw.types.UpdateBotCallbackQuery>`
            - :obj:`UpdateBotChatInviteRequester <pyrogramv1.raw.types.UpdateBotChatInviteRequester>`
            - :obj:`UpdateBotCommands <pyrogramv1.raw.types.UpdateBotCommands>`
            - :obj:`UpdateBotInlineQuery <pyrogramv1.raw.types.UpdateBotInlineQuery>`
            - :obj:`UpdateBotInlineSend <pyrogramv1.raw.types.UpdateBotInlineSend>`
            - :obj:`UpdateBotMenuButton <pyrogramv1.raw.types.UpdateBotMenuButton>`
            - :obj:`UpdateBotPrecheckoutQuery <pyrogramv1.raw.types.UpdateBotPrecheckoutQuery>`
            - :obj:`UpdateBotShippingQuery <pyrogramv1.raw.types.UpdateBotShippingQuery>`
            - :obj:`UpdateBotStopped <pyrogramv1.raw.types.UpdateBotStopped>`
            - :obj:`UpdateBotWebhookJSON <pyrogramv1.raw.types.UpdateBotWebhookJSON>`
            - :obj:`UpdateBotWebhookJSONQuery <pyrogramv1.raw.types.UpdateBotWebhookJSONQuery>`
            - :obj:`UpdateChannel <pyrogramv1.raw.types.UpdateChannel>`
            - :obj:`UpdateChannelAvailableMessages <pyrogramv1.raw.types.UpdateChannelAvailableMessages>`
            - :obj:`UpdateChannelMessageForwards <pyrogramv1.raw.types.UpdateChannelMessageForwards>`
            - :obj:`UpdateChannelMessageViews <pyrogramv1.raw.types.UpdateChannelMessageViews>`
            - :obj:`UpdateChannelParticipant <pyrogramv1.raw.types.UpdateChannelParticipant>`
            - :obj:`UpdateChannelPinnedTopic <pyrogramv1.raw.types.UpdateChannelPinnedTopic>`
            - :obj:`UpdateChannelPinnedTopics <pyrogramv1.raw.types.UpdateChannelPinnedTopics>`
            - :obj:`UpdateChannelReadMessagesContents <pyrogramv1.raw.types.UpdateChannelReadMessagesContents>`
            - :obj:`UpdateChannelTooLong <pyrogramv1.raw.types.UpdateChannelTooLong>`
            - :obj:`UpdateChannelUserTyping <pyrogramv1.raw.types.UpdateChannelUserTyping>`
            - :obj:`UpdateChannelWebPage <pyrogramv1.raw.types.UpdateChannelWebPage>`
            - :obj:`UpdateChat <pyrogramv1.raw.types.UpdateChat>`
            - :obj:`UpdateChatDefaultBannedRights <pyrogramv1.raw.types.UpdateChatDefaultBannedRights>`
            - :obj:`UpdateChatParticipant <pyrogramv1.raw.types.UpdateChatParticipant>`
            - :obj:`UpdateChatParticipantAdd <pyrogramv1.raw.types.UpdateChatParticipantAdd>`
            - :obj:`UpdateChatParticipantAdmin <pyrogramv1.raw.types.UpdateChatParticipantAdmin>`
            - :obj:`UpdateChatParticipantDelete <pyrogramv1.raw.types.UpdateChatParticipantDelete>`
            - :obj:`UpdateChatParticipants <pyrogramv1.raw.types.UpdateChatParticipants>`
            - :obj:`UpdateChatUserTyping <pyrogramv1.raw.types.UpdateChatUserTyping>`
            - :obj:`UpdateConfig <pyrogramv1.raw.types.UpdateConfig>`
            - :obj:`UpdateContactsReset <pyrogramv1.raw.types.UpdateContactsReset>`
            - :obj:`UpdateDcOptions <pyrogramv1.raw.types.UpdateDcOptions>`
            - :obj:`UpdateDeleteChannelMessages <pyrogramv1.raw.types.UpdateDeleteChannelMessages>`
            - :obj:`UpdateDeleteMessages <pyrogramv1.raw.types.UpdateDeleteMessages>`
            - :obj:`UpdateDeleteScheduledMessages <pyrogramv1.raw.types.UpdateDeleteScheduledMessages>`
            - :obj:`UpdateDialogFilter <pyrogramv1.raw.types.UpdateDialogFilter>`
            - :obj:`UpdateDialogFilterOrder <pyrogramv1.raw.types.UpdateDialogFilterOrder>`
            - :obj:`UpdateDialogFilters <pyrogramv1.raw.types.UpdateDialogFilters>`
            - :obj:`UpdateDialogPinned <pyrogramv1.raw.types.UpdateDialogPinned>`
            - :obj:`UpdateDialogUnreadMark <pyrogramv1.raw.types.UpdateDialogUnreadMark>`
            - :obj:`UpdateDraftMessage <pyrogramv1.raw.types.UpdateDraftMessage>`
            - :obj:`UpdateEditChannelMessage <pyrogramv1.raw.types.UpdateEditChannelMessage>`
            - :obj:`UpdateEditMessage <pyrogramv1.raw.types.UpdateEditMessage>`
            - :obj:`UpdateEncryptedChatTyping <pyrogramv1.raw.types.UpdateEncryptedChatTyping>`
            - :obj:`UpdateEncryptedMessagesRead <pyrogramv1.raw.types.UpdateEncryptedMessagesRead>`
            - :obj:`UpdateEncryption <pyrogramv1.raw.types.UpdateEncryption>`
            - :obj:`UpdateFavedStickers <pyrogramv1.raw.types.UpdateFavedStickers>`
            - :obj:`UpdateFolderPeers <pyrogramv1.raw.types.UpdateFolderPeers>`
            - :obj:`UpdateGeoLiveViewed <pyrogramv1.raw.types.UpdateGeoLiveViewed>`
            - :obj:`UpdateGroupCall <pyrogramv1.raw.types.UpdateGroupCall>`
            - :obj:`UpdateGroupCallConnection <pyrogramv1.raw.types.UpdateGroupCallConnection>`
            - :obj:`UpdateGroupCallParticipants <pyrogramv1.raw.types.UpdateGroupCallParticipants>`
            - :obj:`UpdateGroupInvitePrivacyForbidden <pyrogramv1.raw.types.UpdateGroupInvitePrivacyForbidden>`
            - :obj:`UpdateInlineBotCallbackQuery <pyrogramv1.raw.types.UpdateInlineBotCallbackQuery>`
            - :obj:`UpdateLangPack <pyrogramv1.raw.types.UpdateLangPack>`
            - :obj:`UpdateLangPackTooLong <pyrogramv1.raw.types.UpdateLangPackTooLong>`
            - :obj:`UpdateLoginToken <pyrogramv1.raw.types.UpdateLoginToken>`
            - :obj:`UpdateMessageExtendedMedia <pyrogramv1.raw.types.UpdateMessageExtendedMedia>`
            - :obj:`UpdateMessageID <pyrogramv1.raw.types.UpdateMessageID>`
            - :obj:`UpdateMessagePoll <pyrogramv1.raw.types.UpdateMessagePoll>`
            - :obj:`UpdateMessagePollVote <pyrogramv1.raw.types.UpdateMessagePollVote>`
            - :obj:`UpdateMessageReactions <pyrogramv1.raw.types.UpdateMessageReactions>`
            - :obj:`UpdateMoveStickerSetToTop <pyrogramv1.raw.types.UpdateMoveStickerSetToTop>`
            - :obj:`UpdateNewChannelMessage <pyrogramv1.raw.types.UpdateNewChannelMessage>`
            - :obj:`UpdateNewEncryptedMessage <pyrogramv1.raw.types.UpdateNewEncryptedMessage>`
            - :obj:`UpdateNewMessage <pyrogramv1.raw.types.UpdateNewMessage>`
            - :obj:`UpdateNewScheduledMessage <pyrogramv1.raw.types.UpdateNewScheduledMessage>`
            - :obj:`UpdateNewStickerSet <pyrogramv1.raw.types.UpdateNewStickerSet>`
            - :obj:`UpdateNotifySettings <pyrogramv1.raw.types.UpdateNotifySettings>`
            - :obj:`UpdatePeerBlocked <pyrogramv1.raw.types.UpdatePeerBlocked>`
            - :obj:`UpdatePeerHistoryTTL <pyrogramv1.raw.types.UpdatePeerHistoryTTL>`
            - :obj:`UpdatePeerLocated <pyrogramv1.raw.types.UpdatePeerLocated>`
            - :obj:`UpdatePeerSettings <pyrogramv1.raw.types.UpdatePeerSettings>`
            - :obj:`UpdatePendingJoinRequests <pyrogramv1.raw.types.UpdatePendingJoinRequests>`
            - :obj:`UpdatePhoneCall <pyrogramv1.raw.types.UpdatePhoneCall>`
            - :obj:`UpdatePhoneCallSignalingData <pyrogramv1.raw.types.UpdatePhoneCallSignalingData>`
            - :obj:`UpdatePinnedChannelMessages <pyrogramv1.raw.types.UpdatePinnedChannelMessages>`
            - :obj:`UpdatePinnedDialogs <pyrogramv1.raw.types.UpdatePinnedDialogs>`
            - :obj:`UpdatePinnedMessages <pyrogramv1.raw.types.UpdatePinnedMessages>`
            - :obj:`UpdatePrivacy <pyrogramv1.raw.types.UpdatePrivacy>`
            - :obj:`UpdatePtsChanged <pyrogramv1.raw.types.UpdatePtsChanged>`
            - :obj:`UpdateReadChannelDiscussionInbox <pyrogramv1.raw.types.UpdateReadChannelDiscussionInbox>`
            - :obj:`UpdateReadChannelDiscussionOutbox <pyrogramv1.raw.types.UpdateReadChannelDiscussionOutbox>`
            - :obj:`UpdateReadChannelInbox <pyrogramv1.raw.types.UpdateReadChannelInbox>`
            - :obj:`UpdateReadChannelOutbox <pyrogramv1.raw.types.UpdateReadChannelOutbox>`
            - :obj:`UpdateReadFeaturedEmojiStickers <pyrogramv1.raw.types.UpdateReadFeaturedEmojiStickers>`
            - :obj:`UpdateReadFeaturedStickers <pyrogramv1.raw.types.UpdateReadFeaturedStickers>`
            - :obj:`UpdateReadHistoryInbox <pyrogramv1.raw.types.UpdateReadHistoryInbox>`
            - :obj:`UpdateReadHistoryOutbox <pyrogramv1.raw.types.UpdateReadHistoryOutbox>`
            - :obj:`UpdateReadMessagesContents <pyrogramv1.raw.types.UpdateReadMessagesContents>`
            - :obj:`UpdateRecentEmojiStatuses <pyrogramv1.raw.types.UpdateRecentEmojiStatuses>`
            - :obj:`UpdateRecentReactions <pyrogramv1.raw.types.UpdateRecentReactions>`
            - :obj:`UpdateRecentStickers <pyrogramv1.raw.types.UpdateRecentStickers>`
            - :obj:`UpdateSavedGifs <pyrogramv1.raw.types.UpdateSavedGifs>`
            - :obj:`UpdateSavedRingtones <pyrogramv1.raw.types.UpdateSavedRingtones>`
            - :obj:`UpdateServiceNotification <pyrogramv1.raw.types.UpdateServiceNotification>`
            - :obj:`UpdateStickerSets <pyrogramv1.raw.types.UpdateStickerSets>`
            - :obj:`UpdateStickerSetsOrder <pyrogramv1.raw.types.UpdateStickerSetsOrder>`
            - :obj:`UpdateTheme <pyrogramv1.raw.types.UpdateTheme>`
            - :obj:`UpdateTranscribedAudio <pyrogramv1.raw.types.UpdateTranscribedAudio>`
            - :obj:`UpdateUser <pyrogramv1.raw.types.UpdateUser>`
            - :obj:`UpdateUserEmojiStatus <pyrogramv1.raw.types.UpdateUserEmojiStatus>`
            - :obj:`UpdateUserName <pyrogramv1.raw.types.UpdateUserName>`
            - :obj:`UpdateUserPhone <pyrogramv1.raw.types.UpdateUserPhone>`
            - :obj:`UpdateUserStatus <pyrogramv1.raw.types.UpdateUserStatus>`
            - :obj:`UpdateUserTyping <pyrogramv1.raw.types.UpdateUserTyping>`
            - :obj:`UpdateWebPage <pyrogramv1.raw.types.UpdateWebPage>`
            - :obj:`UpdateWebViewResultSent <pyrogramv1.raw.types.UpdateWebViewResultSent>`
    """

    QUALNAME = "pyrogramv1.raw.base.Update"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyrogram.org/telegram/base/update")
