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

InputPrivacyRule = Union[raw.types.InputPrivacyValueAllowAll, raw.types.InputPrivacyValueAllowChatParticipants, raw.types.InputPrivacyValueAllowContacts, raw.types.InputPrivacyValueAllowUsers, raw.types.InputPrivacyValueDisallowAll, raw.types.InputPrivacyValueDisallowChatParticipants, raw.types.InputPrivacyValueDisallowContacts, raw.types.InputPrivacyValueDisallowUsers]


# noinspection PyRedeclaration
class InputPrivacyRule:  # type: ignore
    """This base type has 8 constructors available.

    Constructors:
        .. hlist::
            :columns: 2

            - :obj:`InputPrivacyValueAllowAll <pyrogramv1.raw.types.InputPrivacyValueAllowAll>`
            - :obj:`InputPrivacyValueAllowChatParticipants <pyrogramv1.raw.types.InputPrivacyValueAllowChatParticipants>`
            - :obj:`InputPrivacyValueAllowContacts <pyrogramv1.raw.types.InputPrivacyValueAllowContacts>`
            - :obj:`InputPrivacyValueAllowUsers <pyrogramv1.raw.types.InputPrivacyValueAllowUsers>`
            - :obj:`InputPrivacyValueDisallowAll <pyrogramv1.raw.types.InputPrivacyValueDisallowAll>`
            - :obj:`InputPrivacyValueDisallowChatParticipants <pyrogramv1.raw.types.InputPrivacyValueDisallowChatParticipants>`
            - :obj:`InputPrivacyValueDisallowContacts <pyrogramv1.raw.types.InputPrivacyValueDisallowContacts>`
            - :obj:`InputPrivacyValueDisallowUsers <pyrogramv1.raw.types.InputPrivacyValueDisallowUsers>`
    """

    QUALNAME = "pyrogramv1.raw.base.InputPrivacyRule"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyrogram.org/telegram/base/input-privacy-rule")
