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

SendMessageAction = Union[raw.types.SendMessageCancelAction, raw.types.SendMessageChooseContactAction, raw.types.SendMessageChooseStickerAction, raw.types.SendMessageEmojiInteraction, raw.types.SendMessageEmojiInteractionSeen, raw.types.SendMessageGamePlayAction, raw.types.SendMessageGeoLocationAction, raw.types.SendMessageHistoryImportAction, raw.types.SendMessageRecordAudioAction, raw.types.SendMessageRecordRoundAction, raw.types.SendMessageRecordVideoAction, raw.types.SendMessageTypingAction, raw.types.SendMessageUploadAudioAction, raw.types.SendMessageUploadDocumentAction, raw.types.SendMessageUploadPhotoAction, raw.types.SendMessageUploadRoundAction, raw.types.SendMessageUploadVideoAction, raw.types.SpeakingInGroupCallAction]


# noinspection PyRedeclaration
class SendMessageAction:  # type: ignore
    """This base type has 18 constructors available.

    Constructors:
        .. hlist::
            :columns: 2

            - :obj:`SendMessageCancelAction <pyrogramv1.raw.types.SendMessageCancelAction>`
            - :obj:`SendMessageChooseContactAction <pyrogramv1.raw.types.SendMessageChooseContactAction>`
            - :obj:`SendMessageChooseStickerAction <pyrogramv1.raw.types.SendMessageChooseStickerAction>`
            - :obj:`SendMessageEmojiInteraction <pyrogramv1.raw.types.SendMessageEmojiInteraction>`
            - :obj:`SendMessageEmojiInteractionSeen <pyrogramv1.raw.types.SendMessageEmojiInteractionSeen>`
            - :obj:`SendMessageGamePlayAction <pyrogramv1.raw.types.SendMessageGamePlayAction>`
            - :obj:`SendMessageGeoLocationAction <pyrogramv1.raw.types.SendMessageGeoLocationAction>`
            - :obj:`SendMessageHistoryImportAction <pyrogramv1.raw.types.SendMessageHistoryImportAction>`
            - :obj:`SendMessageRecordAudioAction <pyrogramv1.raw.types.SendMessageRecordAudioAction>`
            - :obj:`SendMessageRecordRoundAction <pyrogramv1.raw.types.SendMessageRecordRoundAction>`
            - :obj:`SendMessageRecordVideoAction <pyrogramv1.raw.types.SendMessageRecordVideoAction>`
            - :obj:`SendMessageTypingAction <pyrogramv1.raw.types.SendMessageTypingAction>`
            - :obj:`SendMessageUploadAudioAction <pyrogramv1.raw.types.SendMessageUploadAudioAction>`
            - :obj:`SendMessageUploadDocumentAction <pyrogramv1.raw.types.SendMessageUploadDocumentAction>`
            - :obj:`SendMessageUploadPhotoAction <pyrogramv1.raw.types.SendMessageUploadPhotoAction>`
            - :obj:`SendMessageUploadRoundAction <pyrogramv1.raw.types.SendMessageUploadRoundAction>`
            - :obj:`SendMessageUploadVideoAction <pyrogramv1.raw.types.SendMessageUploadVideoAction>`
            - :obj:`SpeakingInGroupCallAction <pyrogramv1.raw.types.SpeakingInGroupCallAction>`
    """

    QUALNAME = "pyrogramv1.raw.base.SendMessageAction"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyrogram.org/telegram/base/send-message-action")
