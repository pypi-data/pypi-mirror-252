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

PageBlock = Union[raw.types.PageBlockAnchor, raw.types.PageBlockAudio, raw.types.PageBlockAuthorDate, raw.types.PageBlockBlockquote, raw.types.PageBlockChannel, raw.types.PageBlockCollage, raw.types.PageBlockCover, raw.types.PageBlockDetails, raw.types.PageBlockDivider, raw.types.PageBlockEmbed, raw.types.PageBlockEmbedPost, raw.types.PageBlockFooter, raw.types.PageBlockHeader, raw.types.PageBlockKicker, raw.types.PageBlockList, raw.types.PageBlockMap, raw.types.PageBlockOrderedList, raw.types.PageBlockParagraph, raw.types.PageBlockPhoto, raw.types.PageBlockPreformatted, raw.types.PageBlockPullquote, raw.types.PageBlockRelatedArticles, raw.types.PageBlockSlideshow, raw.types.PageBlockSubheader, raw.types.PageBlockSubtitle, raw.types.PageBlockTable, raw.types.PageBlockTitle, raw.types.PageBlockUnsupported, raw.types.PageBlockVideo]


# noinspection PyRedeclaration
class PageBlock:  # type: ignore
    """This base type has 29 constructors available.

    Constructors:
        .. hlist::
            :columns: 2

            - :obj:`PageBlockAnchor <pyrogramv1.raw.types.PageBlockAnchor>`
            - :obj:`PageBlockAudio <pyrogramv1.raw.types.PageBlockAudio>`
            - :obj:`PageBlockAuthorDate <pyrogramv1.raw.types.PageBlockAuthorDate>`
            - :obj:`PageBlockBlockquote <pyrogramv1.raw.types.PageBlockBlockquote>`
            - :obj:`PageBlockChannel <pyrogramv1.raw.types.PageBlockChannel>`
            - :obj:`PageBlockCollage <pyrogramv1.raw.types.PageBlockCollage>`
            - :obj:`PageBlockCover <pyrogramv1.raw.types.PageBlockCover>`
            - :obj:`PageBlockDetails <pyrogramv1.raw.types.PageBlockDetails>`
            - :obj:`PageBlockDivider <pyrogramv1.raw.types.PageBlockDivider>`
            - :obj:`PageBlockEmbed <pyrogramv1.raw.types.PageBlockEmbed>`
            - :obj:`PageBlockEmbedPost <pyrogramv1.raw.types.PageBlockEmbedPost>`
            - :obj:`PageBlockFooter <pyrogramv1.raw.types.PageBlockFooter>`
            - :obj:`PageBlockHeader <pyrogramv1.raw.types.PageBlockHeader>`
            - :obj:`PageBlockKicker <pyrogramv1.raw.types.PageBlockKicker>`
            - :obj:`PageBlockList <pyrogramv1.raw.types.PageBlockList>`
            - :obj:`PageBlockMap <pyrogramv1.raw.types.PageBlockMap>`
            - :obj:`PageBlockOrderedList <pyrogramv1.raw.types.PageBlockOrderedList>`
            - :obj:`PageBlockParagraph <pyrogramv1.raw.types.PageBlockParagraph>`
            - :obj:`PageBlockPhoto <pyrogramv1.raw.types.PageBlockPhoto>`
            - :obj:`PageBlockPreformatted <pyrogramv1.raw.types.PageBlockPreformatted>`
            - :obj:`PageBlockPullquote <pyrogramv1.raw.types.PageBlockPullquote>`
            - :obj:`PageBlockRelatedArticles <pyrogramv1.raw.types.PageBlockRelatedArticles>`
            - :obj:`PageBlockSlideshow <pyrogramv1.raw.types.PageBlockSlideshow>`
            - :obj:`PageBlockSubheader <pyrogramv1.raw.types.PageBlockSubheader>`
            - :obj:`PageBlockSubtitle <pyrogramv1.raw.types.PageBlockSubtitle>`
            - :obj:`PageBlockTable <pyrogramv1.raw.types.PageBlockTable>`
            - :obj:`PageBlockTitle <pyrogramv1.raw.types.PageBlockTitle>`
            - :obj:`PageBlockUnsupported <pyrogramv1.raw.types.PageBlockUnsupported>`
            - :obj:`PageBlockVideo <pyrogramv1.raw.types.PageBlockVideo>`
    """

    QUALNAME = "pyrogramv1.raw.base.PageBlock"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyrogram.org/telegram/base/page-block")
