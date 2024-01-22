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

PrivacyKey = Union[raw.types.PrivacyKeyAddedByPhone, raw.types.PrivacyKeyChatInvite, raw.types.PrivacyKeyForwards, raw.types.PrivacyKeyPhoneCall, raw.types.PrivacyKeyPhoneNumber, raw.types.PrivacyKeyPhoneP2P, raw.types.PrivacyKeyProfilePhoto, raw.types.PrivacyKeyStatusTimestamp, raw.types.PrivacyKeyVoiceMessages]


# noinspection PyRedeclaration
class PrivacyKey:  # type: ignore
    """This base type has 9 constructors available.

    Constructors:
        .. hlist::
            :columns: 2

            - :obj:`PrivacyKeyAddedByPhone <pyrogramv1.raw.types.PrivacyKeyAddedByPhone>`
            - :obj:`PrivacyKeyChatInvite <pyrogramv1.raw.types.PrivacyKeyChatInvite>`
            - :obj:`PrivacyKeyForwards <pyrogramv1.raw.types.PrivacyKeyForwards>`
            - :obj:`PrivacyKeyPhoneCall <pyrogramv1.raw.types.PrivacyKeyPhoneCall>`
            - :obj:`PrivacyKeyPhoneNumber <pyrogramv1.raw.types.PrivacyKeyPhoneNumber>`
            - :obj:`PrivacyKeyPhoneP2P <pyrogramv1.raw.types.PrivacyKeyPhoneP2P>`
            - :obj:`PrivacyKeyProfilePhoto <pyrogramv1.raw.types.PrivacyKeyProfilePhoto>`
            - :obj:`PrivacyKeyStatusTimestamp <pyrogramv1.raw.types.PrivacyKeyStatusTimestamp>`
            - :obj:`PrivacyKeyVoiceMessages <pyrogramv1.raw.types.PrivacyKeyVoiceMessages>`
    """

    QUALNAME = "pyrogramv1.raw.base.PrivacyKey"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyrogram.org/telegram/base/privacy-key")
