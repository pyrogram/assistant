#  MIT License
#
#  Copyright (c) 2019-2020 Dan <https://github.com/delivrance>
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

import re

from pyrogram import filters, emoji, types
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup,
                            InlineKeyboardButton, Object)
from pyrogram.raw import types as raw_types, functions as raw_methods
from pyrogram.raw.all import layer
from pyrogram import Client


class Result:
    DESCRIPTION_MAX_LEN = 60

    @staticmethod
    def get_description(item):
        full = item.__doc__.split("\n")[0]
        short = full[: Result.DESCRIPTION_MAX_LEN].strip()

        if len(short) >= Result.DESCRIPTION_MAX_LEN - 1:
            short += "…"

        return short, full

    @staticmethod
    def snek(s: str):
        s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
        return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()

    class Method:
        DOCS = "https://docs.pyrogram.org/api/methods/{}"
        THUMB = "https://i.imgur.com/S5lY8fy.png"

        def __new__(cls, item):
            short, full = Result.get_description(item)

            return InlineQueryResultArticle(
                title=f"{item.__name__}",
                description="Method - " + short,
                input_message_content=InputTextMessageContent(
                    f"{emoji.CLOSED_BOOK} **Pyrogram Docs**\n\n"
                    f"[{item.__name__}]({cls.DOCS.format(item.__name__)}) - Method\n\n"
                    f"`{full}`\n",
                    disable_web_page_preview=True,
                ),
                thumb_url=cls.THUMB,
            )

    class Decorator:
        DOCS = "https://docs.pyrogram.org/api/decorators#pyrogram.Client.{}"
        THUMB = "https://i.imgur.com/xp3jld1.png"

        def __new__(cls, item):
            short, full = Result.get_description(item)

            return InlineQueryResultArticle(
                title=f"{item.__name__}",
                description="Decorator - " + short,
                input_message_content=InputTextMessageContent(
                    f"{emoji.ARTIST_PALETTE} **Pyrogram Docs**\n\n"
                    f"[{item.__name__}]({cls.DOCS.format(item.__name__)}) - Decorator\n\n"
                    f"`{full}`\n",
                    disable_web_page_preview=True,
                ),
                thumb_url=cls.THUMB,
            )

    class Type:
        DOCS = "https://docs.pyrogram.org/api/types/{}"
        THUMB = "https://i.imgur.com/dw1lLBX.png"

        def __new__(cls, item):
            short, full = Result.get_description(item)

            return InlineQueryResultArticle(
                title=f"{item.__name__}",
                description="Type - " + short,
                input_message_content=InputTextMessageContent(
                    f"{emoji.GREEN_BOOK} **Pyrogram Docs**\n\n"
                    f"[{item.__name__}]({cls.DOCS.format(item.__name__)}) - Type\n\n"
                    f"`{full}`",
                    disable_web_page_preview=True,
                ),
                thumb_url=cls.THUMB,
            )

    class Filter:
        DOCS = "https://docs.pyrogram.org/api/filters#pyrogram.filters.{}"
        THUMB = "https://i.imgur.com/YRe6cKU.png"

        def __new__(cls, item):
            return InlineQueryResultArticle(
                title=f"{item.__class__.__name__}",
                description=f"Filter - {item.__class__.__name__}",
                input_message_content=InputTextMessageContent(
                    f"{emoji.CONTROL_KNOBS} **Pyrogram Docs**\n\n"
                    f"[{item.__class__.__name__}]({cls.DOCS.format(item.__class__.__name__.lower())}) - Filter",
                    disable_web_page_preview=True,
                ),
                thumb_url=cls.THUMB,
            )

    class BoundMethod:
        DOCS = "https://docs.pyrogram.org/api/bound-methods/{}.{}"
        THUMB = "https://i.imgur.com/GxFuuks.png"

        def __new__(cls, item):
            a, b = item.__qualname__.split(".")

            return InlineQueryResultArticle(
                title=f"{item.__qualname__}",
                description=f'Bound Method "{b}" of {a}',
                input_message_content=InputTextMessageContent(
                    f"{emoji.LEDGER} **Pyrogram Docs**\n\n"
                    f"[{item.__qualname__}]({cls.DOCS.format(a, b)}) - Bound Method",
                    disable_web_page_preview=True,
                ),
                thumb_url=cls.THUMB,
            )

    class RawMethod:
        DOCS = "https://docs.pyrogram.org/telegram/functions/{}"
        THUMB = "https://i.imgur.com/NY4uasQ.png"

        def __new__(cls, item):
            constructor_id = hex(item[1].ID)
            path = cls.DOCS.format(Result.snek(item[0]).replace("_", "-").replace(".-", "/"))

            return InlineQueryResultArticle(
                title=f"{item[0]}",
                description=f"Raw Method - {constructor_id}\nSchema: Layer {layer}",
                input_message_content=InputTextMessageContent(
                    f"{emoji.BLUE_BOOK} **Pyrogram Docs**\n\n"
                    f"[{item[0]}]({path}) - Raw Method\n\n"
                    f"`ID`: **{constructor_id}**\n"
                    f"`Schema`: **Layer {layer}**",
                    disable_web_page_preview=True,
                ),
                thumb_url=cls.THUMB,
            )

    class RawType:
        DOCS = "https://docs.pyrogram.org/telegram/types/{}"
        THUMB = "https://i.imgur.com/b33rM21.png"

        def __new__(cls, item):
            constructor_id = hex(item[1].ID)
            path = cls.DOCS.format(Result.snek(item[0]).replace("_", "-").replace(".-", "/"))

            return InlineQueryResultArticle(
                title=f"{item[0]}",
                description=f"Raw Type - {constructor_id}\nSchema: Layer {layer}",
                input_message_content=InputTextMessageContent(
                    f"{emoji.ORANGE_BOOK} **Pyrogram Docs**\n\n"
                    f"[{item[0]}]({path}) - Raw Type\n\n"
                    f"`ID`: **{constructor_id}**\n"
                    f"`Schema`: **Layer {layer}**",
                    disable_web_page_preview=True,
                ),
                thumb_url=cls.THUMB,
            )


METHODS = []

for a in dir(Client):
    m = getattr(Client, a)

    try:
        if not a.startswith("_") and a[0].islower() and m.__doc__ and not a.startswith("on_"):
            METHODS.append((a.lower(), Result.Method(m)))
    except AttributeError:
        pass

DECORATORS = []

for a in dir(Client):
    m = getattr(Client, a)

    try:
        if not a.startswith("_") and a[0].islower() and m.__doc__ and a.startswith("on_"):
            DECORATORS.append((a.lower(), Result.Decorator(m)))
    except AttributeError:
        pass

TYPES = []

for a in dir(types):
    t = getattr(types, a)

    if not a.startswith("_") and a[0].isupper() and t.__doc__:
        TYPES.append((a, Result.Type(t)))

FILTERS = [
    (i.lower(), Result.Filter(getattr(filters, i)))
    for i in filter(
        lambda x: not x.startswith("_")
                  and x[0].islower(),
        dir(filters)
    )
]

BOUND_METHODS = []

for a in dir(types):
    try:
        c = getattr(types, a)
        if issubclass(c, Object):
            for m in dir(c):
                if (
                    not m.startswith("_")
                    and callable(getattr(c, m))
                    and m not in ["default", "read", "write", "with_traceback", "continue_propagation",
                                  "stop_propagation"]
                ):
                    BOUND_METHODS.append((f"{a}.{m}", Result.BoundMethod(getattr(c, m))))
    except TypeError:
        pass

RAW_METHODS = []

for i in filter(lambda x: not x.startswith("_"), dir(raw_methods)):
    if i[0].isupper():
        RAW_METHODS.append((i, Result.RawMethod((i, getattr(raw_methods, i)))))
    else:
        if "Int" not in dir(getattr(raw_methods, i)):
            for j in filter(lambda x: not x.startswith("_") and x[0].isupper(), dir(getattr(raw_methods, i))):
                RAW_METHODS.append((f"{i}.{j}", Result.RawMethod((f"{i}.{j}", getattr(getattr(raw_methods, i), j)))))

for i in RAW_METHODS[:]:
    if "." not in i[0]:
        RAW_METHODS.remove(i)
        RAW_METHODS.append(i)

RAW_TYPES = []

for i in filter(lambda x: not x.startswith("_"), dir(raw_types)):
    if i[0].isupper():
        RAW_TYPES.append((i, Result.RawType((i, getattr(raw_types, i)))))
    else:
        if "Int" not in dir(getattr(raw_types, i)):
            for j in filter(lambda x: not x.startswith("_") and x[0].isupper(), dir(getattr(raw_types, i))):
                RAW_TYPES.append((f"{i}.{j}", Result.RawType((f"{i}.{j}", getattr(getattr(raw_types, i), j)))))

for i in RAW_TYPES[:]:
    if "." not in i[0]:
        RAW_TYPES.remove(i)
        RAW_TYPES.append(i)

FIRE_THUMB = "https://i.imgur.com/qhYYqZa.png"
ROCKET_THUMB = "https://i.imgur.com/PDaYHd8.png"
ABOUT_BOT_THUMB = "https://i.imgur.com/zRglRz3.png"
OPEN_BOOK_THUMB = "https://i.imgur.com/v1XSJ1D.png"
RED_HEART_THUMB = "https://i.imgur.com/66FVFXz.png"
SCROLL_THUMB = "https://i.imgur.com/L1u0VlX.png"

HELP = (
    f"{emoji.ROBOT} **Pyrogram Assistant**\n\n"
    f"You can use this bot in inline mode to search for Pyrogram methods, types and other resources from "
    f"https://docs.pyrogram.org.\n\n"

    f"**__Search__**\n"
    f"`@pyrogrambot <terms>` – Pyrogram API\n"
    f"`@pyrogrambot !r <terms>` – Telegram Raw API\n\n"

    f"**__List__**\n"
    f"`@pyrogrambot !m` – Methods\n"
    f"`@pyrogrambot !t` – Types\n"
    f"`@pyrogrambot !f` – Filters\n"
    f"`@pyrogrambot !b` – Bound Methods\n"
    f"`@pyrogrambot !d` – Decorators\n"
    f"`@pyrogrambot !rm` – Raw Methods\n"
    f"`@pyrogrambot !rt` – Raw Types\n\n"
)

DEFAULT_RESULTS = [
    InlineQueryResultArticle(
        title="About Pyrogram",
        input_message_content=InputTextMessageContent(
            f"{emoji.FIRE} **Pyrogram**\n\n"
            f"Pyrogram is an elegant, easy-to-use Telegram client library and framework written from the ground up in "
            f"Python and C. It enables you to easily create custom apps using both user and bot identities (bot API "
            f"alternative) via the MTProto API.",
            disable_web_page_preview=True,
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"{emoji.BUSTS_IN_SILHOUETTE} Community", url="https://t.me/pyrogram")
                ],
                [
                    InlineKeyboardButton(f"{emoji.CARD_INDEX_DIVIDERS} GitHub", url="https://github.com/pyrogram"),
                    InlineKeyboardButton(f"{emoji.OPEN_BOOK} Docs", url="https://docs.pyrogram.org")
                ]
            ]
        ),
        description="Pyrogram is an elegant, easy-to-use Telegram client library and framework.",
        thumb_url=FIRE_THUMB,
    ),
    InlineQueryResultArticle(
        title="About this Bot",
        input_message_content=InputTextMessageContent(HELP, disable_web_page_preview=True, parse_mode="markdown"),
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                f"{emoji.CARD_INDEX_DIVIDERS} Source Code",
                url="https://github.com/pyrogram/assistant"
            ),
            InlineKeyboardButton(
                f"{emoji.FIRE} Go!",
                switch_inline_query=""
            )
        ]]),
        description="How to use Pyrogram Assistant Bot.",
        thumb_url=ABOUT_BOT_THUMB,
    ),
    InlineQueryResultArticle(
        title="Quick Start",
        input_message_content=InputTextMessageContent(
            f"{emoji.ROCKET} **Pyrogram Docs**\n\n"
            f"[Quick Start](https://docs.pyrogram.org/intro/quickstart) - Introduction\n\n"
            f"`Quick overview to get you started as fast as possible`",
            disable_web_page_preview=True,
        ),
        description="Quick overview to get you started as fast as possible.",
        thumb_url=ROCKET_THUMB,
    ),
    InlineQueryResultArticle(
        title="Support",
        input_message_content=InputTextMessageContent(
            f"{emoji.RED_HEART} **Support Pyrogram**\n\n"
            f"[Support](https://docs.pyrogram.org/support-pyrogram) - Meta\n\n"
            f"`Ways to show your appreciation.`",
            disable_web_page_preview=True,
        ),
        description="Ways to show your appreciation.",
        thumb_url=RED_HEART_THUMB,
    ),
]

rules = """
**Pyrogram Rules**

` 0.` Follow rules; improve chances of getting answers.
` 1.` English only. Other groups by language: #groups.
` 2.` Spam, flood and hate speech is strictly forbidden.
` 3.` Talks unrelated to Pyrogram (ot) are not allowed.
` 4.` Keep unrelated media and emojis to a minimum.
` 5.` Be nice, respect people and use common sense.
` 6.` Ask before sending PMs and respect the answers.
` 7.` "Doesn't work" means nothing. Explain in details.
` 8.` Ask if you get any error, not if the code is correct.
` 9.` Make use of nekobin.com for sharing long code.
`10.` No photos unless they are meaningful and small.

__Rules are subject to change without notice.__
"""

RULES = [
    InlineQueryResultArticle(
        title=f"Rule {i}",
        description=re.sub(r"` ?\d+.` ", "", rule),
        input_message_content=InputTextMessageContent("**Pyrogram Rules**\n\n" + rule),
        thumb_url=SCROLL_THUMB,
    )
    for i, rule in enumerate(rules.split("\n")[3:-3])
]
