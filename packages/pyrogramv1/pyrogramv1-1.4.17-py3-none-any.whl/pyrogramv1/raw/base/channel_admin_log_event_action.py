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

ChannelAdminLogEventAction = Union[raw.types.ChannelAdminLogEventActionChangeAbout, raw.types.ChannelAdminLogEventActionChangeAvailableReactions, raw.types.ChannelAdminLogEventActionChangeHistoryTTL, raw.types.ChannelAdminLogEventActionChangeLinkedChat, raw.types.ChannelAdminLogEventActionChangeLocation, raw.types.ChannelAdminLogEventActionChangePhoto, raw.types.ChannelAdminLogEventActionChangeStickerSet, raw.types.ChannelAdminLogEventActionChangeTitle, raw.types.ChannelAdminLogEventActionChangeUsername, raw.types.ChannelAdminLogEventActionChangeUsernames, raw.types.ChannelAdminLogEventActionCreateTopic, raw.types.ChannelAdminLogEventActionDefaultBannedRights, raw.types.ChannelAdminLogEventActionDeleteMessage, raw.types.ChannelAdminLogEventActionDeleteTopic, raw.types.ChannelAdminLogEventActionDiscardGroupCall, raw.types.ChannelAdminLogEventActionEditMessage, raw.types.ChannelAdminLogEventActionEditTopic, raw.types.ChannelAdminLogEventActionExportedInviteDelete, raw.types.ChannelAdminLogEventActionExportedInviteEdit, raw.types.ChannelAdminLogEventActionExportedInviteRevoke, raw.types.ChannelAdminLogEventActionParticipantInvite, raw.types.ChannelAdminLogEventActionParticipantJoin, raw.types.ChannelAdminLogEventActionParticipantJoinByInvite, raw.types.ChannelAdminLogEventActionParticipantJoinByRequest, raw.types.ChannelAdminLogEventActionParticipantLeave, raw.types.ChannelAdminLogEventActionParticipantMute, raw.types.ChannelAdminLogEventActionParticipantToggleAdmin, raw.types.ChannelAdminLogEventActionParticipantToggleBan, raw.types.ChannelAdminLogEventActionParticipantUnmute, raw.types.ChannelAdminLogEventActionParticipantVolume, raw.types.ChannelAdminLogEventActionPinTopic, raw.types.ChannelAdminLogEventActionSendMessage, raw.types.ChannelAdminLogEventActionStartGroupCall, raw.types.ChannelAdminLogEventActionStopPoll, raw.types.ChannelAdminLogEventActionToggleAntiSpam, raw.types.ChannelAdminLogEventActionToggleForum, raw.types.ChannelAdminLogEventActionToggleGroupCallSetting, raw.types.ChannelAdminLogEventActionToggleInvites, raw.types.ChannelAdminLogEventActionToggleNoForwards, raw.types.ChannelAdminLogEventActionTogglePreHistoryHidden, raw.types.ChannelAdminLogEventActionToggleSignatures, raw.types.ChannelAdminLogEventActionToggleSlowMode, raw.types.ChannelAdminLogEventActionUpdatePinned]


# noinspection PyRedeclaration
class ChannelAdminLogEventAction:  # type: ignore
    """This base type has 43 constructors available.

    Constructors:
        .. hlist::
            :columns: 2

            - :obj:`ChannelAdminLogEventActionChangeAbout <pyrogramv1.raw.types.ChannelAdminLogEventActionChangeAbout>`
            - :obj:`ChannelAdminLogEventActionChangeAvailableReactions <pyrogramv1.raw.types.ChannelAdminLogEventActionChangeAvailableReactions>`
            - :obj:`ChannelAdminLogEventActionChangeHistoryTTL <pyrogramv1.raw.types.ChannelAdminLogEventActionChangeHistoryTTL>`
            - :obj:`ChannelAdminLogEventActionChangeLinkedChat <pyrogramv1.raw.types.ChannelAdminLogEventActionChangeLinkedChat>`
            - :obj:`ChannelAdminLogEventActionChangeLocation <pyrogramv1.raw.types.ChannelAdminLogEventActionChangeLocation>`
            - :obj:`ChannelAdminLogEventActionChangePhoto <pyrogramv1.raw.types.ChannelAdminLogEventActionChangePhoto>`
            - :obj:`ChannelAdminLogEventActionChangeStickerSet <pyrogramv1.raw.types.ChannelAdminLogEventActionChangeStickerSet>`
            - :obj:`ChannelAdminLogEventActionChangeTitle <pyrogramv1.raw.types.ChannelAdminLogEventActionChangeTitle>`
            - :obj:`ChannelAdminLogEventActionChangeUsername <pyrogramv1.raw.types.ChannelAdminLogEventActionChangeUsername>`
            - :obj:`ChannelAdminLogEventActionChangeUsernames <pyrogramv1.raw.types.ChannelAdminLogEventActionChangeUsernames>`
            - :obj:`ChannelAdminLogEventActionCreateTopic <pyrogramv1.raw.types.ChannelAdminLogEventActionCreateTopic>`
            - :obj:`ChannelAdminLogEventActionDefaultBannedRights <pyrogramv1.raw.types.ChannelAdminLogEventActionDefaultBannedRights>`
            - :obj:`ChannelAdminLogEventActionDeleteMessage <pyrogramv1.raw.types.ChannelAdminLogEventActionDeleteMessage>`
            - :obj:`ChannelAdminLogEventActionDeleteTopic <pyrogramv1.raw.types.ChannelAdminLogEventActionDeleteTopic>`
            - :obj:`ChannelAdminLogEventActionDiscardGroupCall <pyrogramv1.raw.types.ChannelAdminLogEventActionDiscardGroupCall>`
            - :obj:`ChannelAdminLogEventActionEditMessage <pyrogramv1.raw.types.ChannelAdminLogEventActionEditMessage>`
            - :obj:`ChannelAdminLogEventActionEditTopic <pyrogramv1.raw.types.ChannelAdminLogEventActionEditTopic>`
            - :obj:`ChannelAdminLogEventActionExportedInviteDelete <pyrogramv1.raw.types.ChannelAdminLogEventActionExportedInviteDelete>`
            - :obj:`ChannelAdminLogEventActionExportedInviteEdit <pyrogramv1.raw.types.ChannelAdminLogEventActionExportedInviteEdit>`
            - :obj:`ChannelAdminLogEventActionExportedInviteRevoke <pyrogramv1.raw.types.ChannelAdminLogEventActionExportedInviteRevoke>`
            - :obj:`ChannelAdminLogEventActionParticipantInvite <pyrogramv1.raw.types.ChannelAdminLogEventActionParticipantInvite>`
            - :obj:`ChannelAdminLogEventActionParticipantJoin <pyrogramv1.raw.types.ChannelAdminLogEventActionParticipantJoin>`
            - :obj:`ChannelAdminLogEventActionParticipantJoinByInvite <pyrogramv1.raw.types.ChannelAdminLogEventActionParticipantJoinByInvite>`
            - :obj:`ChannelAdminLogEventActionParticipantJoinByRequest <pyrogramv1.raw.types.ChannelAdminLogEventActionParticipantJoinByRequest>`
            - :obj:`ChannelAdminLogEventActionParticipantLeave <pyrogramv1.raw.types.ChannelAdminLogEventActionParticipantLeave>`
            - :obj:`ChannelAdminLogEventActionParticipantMute <pyrogramv1.raw.types.ChannelAdminLogEventActionParticipantMute>`
            - :obj:`ChannelAdminLogEventActionParticipantToggleAdmin <pyrogramv1.raw.types.ChannelAdminLogEventActionParticipantToggleAdmin>`
            - :obj:`ChannelAdminLogEventActionParticipantToggleBan <pyrogramv1.raw.types.ChannelAdminLogEventActionParticipantToggleBan>`
            - :obj:`ChannelAdminLogEventActionParticipantUnmute <pyrogramv1.raw.types.ChannelAdminLogEventActionParticipantUnmute>`
            - :obj:`ChannelAdminLogEventActionParticipantVolume <pyrogramv1.raw.types.ChannelAdminLogEventActionParticipantVolume>`
            - :obj:`ChannelAdminLogEventActionPinTopic <pyrogramv1.raw.types.ChannelAdminLogEventActionPinTopic>`
            - :obj:`ChannelAdminLogEventActionSendMessage <pyrogramv1.raw.types.ChannelAdminLogEventActionSendMessage>`
            - :obj:`ChannelAdminLogEventActionStartGroupCall <pyrogramv1.raw.types.ChannelAdminLogEventActionStartGroupCall>`
            - :obj:`ChannelAdminLogEventActionStopPoll <pyrogramv1.raw.types.ChannelAdminLogEventActionStopPoll>`
            - :obj:`ChannelAdminLogEventActionToggleAntiSpam <pyrogramv1.raw.types.ChannelAdminLogEventActionToggleAntiSpam>`
            - :obj:`ChannelAdminLogEventActionToggleForum <pyrogramv1.raw.types.ChannelAdminLogEventActionToggleForum>`
            - :obj:`ChannelAdminLogEventActionToggleGroupCallSetting <pyrogramv1.raw.types.ChannelAdminLogEventActionToggleGroupCallSetting>`
            - :obj:`ChannelAdminLogEventActionToggleInvites <pyrogramv1.raw.types.ChannelAdminLogEventActionToggleInvites>`
            - :obj:`ChannelAdminLogEventActionToggleNoForwards <pyrogramv1.raw.types.ChannelAdminLogEventActionToggleNoForwards>`
            - :obj:`ChannelAdminLogEventActionTogglePreHistoryHidden <pyrogramv1.raw.types.ChannelAdminLogEventActionTogglePreHistoryHidden>`
            - :obj:`ChannelAdminLogEventActionToggleSignatures <pyrogramv1.raw.types.ChannelAdminLogEventActionToggleSignatures>`
            - :obj:`ChannelAdminLogEventActionToggleSlowMode <pyrogramv1.raw.types.ChannelAdminLogEventActionToggleSlowMode>`
            - :obj:`ChannelAdminLogEventActionUpdatePinned <pyrogramv1.raw.types.ChannelAdminLogEventActionUpdatePinned>`
    """

    QUALNAME = "pyrogramv1.raw.base.ChannelAdminLogEventAction"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyrogram.org/telegram/base/channel-admin-log-event-action")
