# MIT License
#
# Copyright (c) 2020 Dan Tès <https://github.com/delivrance>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pyrogram import (
    Emoji, InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton,
    InlineKeyboardMarkup, __version__
)

from ..assistant import Assistant
from ..utils import docs

NEXT_OFFSET = 25
CACHE_TIME = 5

FIRE_THUMB = "https://i.imgur.com/qhYYqZa.png"
ROCKET_THUMB = "https://i.imgur.com/PDaYHd8.png"
OPEN_BOOK_THUMB = "https://i.imgur.com/v1XSJ1D.png"

VERSION = __version__.split("-")[0]


@Assistant.on_inline_query()
async def inline(_, query: InlineQuery):
    string = query.query.lower()

    if string == "":
        await query.answer(
            results=docs.DEFAULT_RESULTS,
            cache_time=CACHE_TIME,
            switch_pm_text=f"{Emoji.MAGNIFYING_GLASS_TILTED_RIGHT} Type to search Pyrogram Docs",
            switch_pm_parameter="start",
        )

        return

    results = []
    offset = int(query.offset or 0)
    switch_pm_text = f"{Emoji.OPEN_BOOK} Pyrogram Docs"

    if string == "!m":
        switch_pm_text = f"{Emoji.CLOSED_BOOK} Pyrogram Methods ({len(docs.METHODS)})"

        if offset == 0:
            results.append(
                InlineQueryResultArticle(
                    title="Methods",
                    description="Pyrogram Methods online documentation page",
                    input_message_content=InputTextMessageContent(
                        f"{Emoji.FIRE} **Pyrogram Methods**\n\n"
                        f"`This page contains all available high-level Methods existing in Pyrogram v{VERSION}.`"
                    ),
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            f"{Emoji.OPEN_BOOK} Online docs",
                            url="https://docs.pyrogram.org/api/methods"
                        )
                    ]]),
                    thumb_url=FIRE_THUMB,
                )
            )

        for i in docs.METHODS[offset: offset + NEXT_OFFSET]:
            results.append(i[1])
    elif string == "!t":
        switch_pm_text = f"{Emoji.GREEN_BOOK} Pyrogram Types ({len(docs.TYPES)})"

        if offset == 0:
            results.append(
                InlineQueryResultArticle(
                    title="Types",
                    description="Pyrogram Types online documentation page",
                    input_message_content=InputTextMessageContent(
                        f"{Emoji.FIRE} **Pyrogram Types**\n\n"
                        f"`This page contains all available high-level Types existing in Pyrogram v{VERSION}.`"
                    ),
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            f"{Emoji.OPEN_BOOK} Online docs",
                            url="https://docs.pyrogram.org/api/types"
                        )
                    ]]),
                    thumb_url=FIRE_THUMB,
                )
            )

        for i in docs.TYPES[offset: offset + NEXT_OFFSET]:
            results.append(i[1])
    elif string == "!b":
        switch_pm_text = f"{Emoji.CLOSED_BOOK} Pyrogram Bound Methods ({len(docs.BOUND_METHODS)})"

        if offset == 0:
            results.append(
                InlineQueryResultArticle(
                    title="Types",
                    description="Pyrogram Bound Methods online documentation page",
                    input_message_content=InputTextMessageContent(
                        f"{Emoji.FIRE} **Pyrogram Bound Methods**\n\n"
                        f"`This page contains all available bound methods existing in Pyrogram v{VERSION}.`"
                    ),
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            f"{Emoji.OPEN_BOOK} Online docs",
                            url="https://docs.pyrogram.org/api/bound-methods"
                        )]]
                    ),
                    thumb_url=FIRE_THUMB,
                )
            )

        for i in docs.BOUND_METHODS[offset: offset + NEXT_OFFSET]:
            results.append(i[1])
    elif string == "!d":
        switch_pm_text = f"{Emoji.CLOSED_BOOK} Pyrogram Decorators ({len(docs.DECORATORS)})"

        if offset == 0:
            results.append(
                InlineQueryResultArticle(
                    title="Decorators",
                    description="Pyrogram Decorators online documentation page",
                    input_message_content=InputTextMessageContent(
                        f"{Emoji.FIRE} **Pyrogram Decorators**\n\n"
                        f"`This page contains all available decorators existing in Pyrogram v{VERSION}.`"
                    ),
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            f"{Emoji.OPEN_BOOK} Online docs",
                            url="https://docs.pyrogram.org/api/decorators"
                        )]]
                    ),
                    thumb_url=FIRE_THUMB,
                )
            )

        for i in docs.DECORATORS[offset: offset + NEXT_OFFSET]:
            results.append(i[1])
    elif string == "!f":
        switch_pm_text = f"{Emoji.CONTROL_KNOBS} Pyrogram Filters ({len(docs.FILTERS)})"

        if offset == 0:
            results.append(
                InlineQueryResultArticle(
                    title="Filters",
                    description="Pyrogram Filters online documentation page",
                    input_message_content=InputTextMessageContent(
                        f"{Emoji.FIRE} **Pyrogram Filters**\n\n"
                        f"`This page contains all library-defined Filters available in Pyrogram v{VERSION}.`"
                    ),
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            f"{Emoji.OPEN_BOOK} Online docs",
                            url="https://docs.pyrogram.org/api/filters"
                        )
                    ]]),
                    thumb_url=FIRE_THUMB,
                )
            )

        for i in docs.FILTERS[offset: offset + NEXT_OFFSET]:
            results.append(i[1])
    elif string == "!rm":
        switch_pm_text = f"{Emoji.BLUE_BOOK} Raw Methods ({len(docs.RAW_METHODS)})"

        if offset == 0:
            results.append(
                InlineQueryResultArticle(
                    title="Raw Methods",
                    description="Pyrogram Raw Methods online documentation page",
                    input_message_content=InputTextMessageContent(
                        f"{Emoji.FIRE} **Pyrogram Raw Methods**\n\n"
                        f"`This page contains all available Raw Methods existing in the Telegram Schema, Layer `"
                        f"`{docs.layer}.`"
                    ),
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            f"{Emoji.OPEN_BOOK} Online docs",
                            url="https://docs.pyrogram.org/telegram/functions"
                        ),
                        InlineKeyboardButton(
                            f"{Emoji.SCROLL} TL Schema",
                            url="https://github.com/pyrogram/pyrogram/blob/develop/compiler/api/source/main_api.tl"
                        ),
                    ]]),
                    thumb_url=FIRE_THUMB,
                )
            )

        for i in docs.RAW_METHODS[offset: offset + NEXT_OFFSET]:
            results.append(i[1])
    elif string == "!rt":
        switch_pm_text = f"{Emoji.ORANGE_BOOK} Raw Types ({len(docs.RAW_TYPES)})"

        if offset == 0:
            results.append(
                InlineQueryResultArticle(
                    title="Raw Types",
                    description="Pyrogram Raw Types online documentation page",
                    input_message_content=InputTextMessageContent(
                        f"{Emoji.FIRE} **Pyrogram Raw Types**\n\n"
                        f"`This page contains all available Raw Types existing in the Telegram Schema, Layer "
                        f"{docs.layer}.`"
                    ),
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            f"{Emoji.OPEN_BOOK} Online docs",
                            url="https://docs.pyrogram.org/telegram/types"
                        ),
                        InlineKeyboardButton(
                            f"{Emoji.SCROLL} TL Schema",
                            url="https://github.com/pyrogram/pyrogram/blob/develop/compiler/api/source/main_api.tl",
                        ),
                    ]]),
                    thumb_url=FIRE_THUMB,
                )
            )

        for i in docs.RAW_TYPES[offset: offset + NEXT_OFFSET]:
            results.append(i[1])

    if results:
        await query.answer(
            results=results,
            cache_time=CACHE_TIME,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            next_offset=str(offset + NEXT_OFFSET),
        )
    else:
        if offset:
            await query.answer(
                results=[],
                cache_time=CACHE_TIME,
                switch_pm_text=switch_pm_text,
                switch_pm_parameter="start",
                next_offset="",
            )

        if string.startswith("!r"):
            string = " ".join(string.split(" ")[1:])

            if string == "":
                await query.answer(
                    results=[],
                    cache_time=CACHE_TIME,
                    switch_pm_text=f"{Emoji.MAGNIFYING_GLASS_TILTED_RIGHT} Type to search Raw Docs",
                    switch_pm_parameter="start",
                )

            for i in docs.RAW_METHODS:
                if string in i[0].lower():
                    results.append(i[1])

            for i in docs.RAW_TYPES:
                if string in i[0].lower():
                    results.append(i[1])

        else:
            for i in docs.METHODS:
                if string in i[0].lower():
                    results.append(i[1])

            for i in docs.TYPES:
                if string in i[0].lower():
                    results.append(i[1])

            for i in docs.BOUND_METHODS:
                if string in i[0].lower():
                    results.append(i[1])

            for i in docs.DECORATORS:
                if string in i[0].lower():
                    results.append(i[1])

            for i in docs.FILTERS:
                if string in i[0].lower():
                    results.append(i[1])

        if results:
            count = len(results)
            switch_pm_text = f"{Emoji.OPEN_BOOK} {count} Result{'s' if count > 1 else ''} for \"{string}\""

            await query.answer(
                results=results[:50],
                cache_time=CACHE_TIME,
                switch_pm_text=switch_pm_text,
                switch_pm_parameter="start"
            )
        else:
            await query.answer(
                results=[],
                cache_time=CACHE_TIME,
                switch_pm_text=f'{Emoji.CROSS_MARK} No results for "{string}"',
                switch_pm_parameter="okay",
            )
