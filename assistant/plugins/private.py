#  MIT License
#
#  Copyright (c) 2019-present Dan <https://github.com/delivrance>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

from pyrogram import filters, emoji
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from ..assistant import Assistant
from ..utils import docs


@Assistant.on_message(filters.private)
async def go(_, message: Message):
    await message.reply(
        docs.HELP,
        disable_web_page_preview=True,
        parse_mode="markdown",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                f"{emoji.CARD_INDEX_DIVIDERS} Source Code",
                url="https://github.com/pyrogram/assistant"
            ),
            InlineKeyboardButton(
                f"{emoji.FIRE} Go!",
                switch_inline_query=""
            )
        ]])
    )
