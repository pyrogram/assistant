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

import asyncio
import time
from functools import partial

import aiohttp
from pyrogram import Filters, Client, Message, Emoji, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, \
    ChatPermissions
from functools import wraps

command = partial(Filters.command, prefixes="#")
dan_id = 23122162


async def reply_and_delete(message: Message, text: str):
    await asyncio.gather(
        message.delete(),
        message.reply(
            text,
            quote=False,
            reply_to_message_id=getattr(
                message.reply_to_message,
                "message_id", None
            ),
            disable_web_page_preview=True
        )
    )


async def is_admin(bot: Client, message: Message):
    return (await bot.get_chat_member(message.chat.id, message.from_user.id)).status in ("creator", "administrator")


def administrators_only(func):
    @wraps(func)
    async def decorator(bot: Client, message: Message):
        if await is_admin(bot, message):
            await func(bot, message)

        await message.delete()

    decorator.admin = True

    return decorator


################################

PING_TTL = 5


@Client.on_message(command("ping"))
async def ping(_, message: Message):
    """Ping the assistant"""
    start = time.time()
    reply = await message.reply("...")
    delta_ping = time.time() - start

    for i in range(PING_TTL, 0, -1):
        start = time.time()
        await reply.edit(f"**Pong!** `{delta_ping * 1000:.3f} ms` ({i})")
        delta_edit = time.time() - start

        await asyncio.sleep(1 - delta_edit)

    await asyncio.gather(reply.delete(), message.delete())


################################


SCHEMA = "https"
BASE = "nekobin.com"
ENDPOINT = f"{SCHEMA}://{BASE}/api/documents"
ANSWER = "**Long message from** {:mention}\n{}"
TIMEOUT = 3
MESSAGE_ID_DIFF = 100


@Client.on_message(command("neko"))
@administrators_only
async def neko(_, message: Message):
    """Paste very long code"""
    reply = message.reply_to_message

    if not reply:
        return

    # Ignore messages that are too old
    if message.message_id - reply.message_id > MESSAGE_ID_DIFF:
        return

    async with aiohttp.ClientSession() as session:
        async with session.post(
            ENDPOINT,
            json={"content": reply.text},
            timeout=TIMEOUT
        ) as response:
            key = (await response.json())["result"]["key"]

    await reply_and_delete(reply, ANSWER.format(reply.from_user, f"{BASE}/{key}.py"))


################################


LOG = """
Enable Logging: add the following on the top of your script and run it again:

```import logging
logging.basicConfig(level=logging.INFO)```

For a more verbose logging, use `level=logging.DEBUG` instead.
"""


@Client.on_message(command("log"))
async def log(_, message: Message):
    """Enable debug logging"""
    await reply_and_delete(message, LOG)


################################


EX = """
Please, provide us a **minimal** and **reproducible** example in order to easily understand and reproduce the problem.

[How do I create a minimal, reproducible example?](https://stackoverflow.com/help/minimal-reproducible-example)
"""


@Client.on_message(command("ex"))
async def ex(_, message: Message):
    """Ask for minimal example"""
    await reply_and_delete(message, EX)


################################


OT = [
    "This argument is off-topic and not related to Pyrogram. Please, move the discussion to @PyrogramLounge",
    "Looks like this topic is related to Pyrogram. You can discuss at @PyrogramChat"
]


@Client.on_message(command("ot"))
async def ot(_, message: Message):
    """offtopic conversation"""
    answer = OT[0] if message.chat.id == -1001387666944 else OT[1]  # @PyrogramChat id
    await reply_and_delete(message, answer)


################################


ASK = """
Sorry, your question is not well formulated. Please, be clear and try to follow the guidelines in the link below.

[How do I ask a good question?](https://stackoverflow.com/help/how-to-ask)
"""


@Client.on_message(command("ask"))
async def ask(_, message: Message):
    """How to ask questions"""
    await reply_and_delete(message, ASK)


################################


RES = """
**Good Python resources for learning**

• [Official Tutorial](https://docs.python.org/3/tutorial/index.html) - Book
• [Dive Into Python 3](https://www.diveinto.org/python3/table-of-contents.html) - Book
• [Hitchhiker's Guide!](https://docs.python-guide.org) - Book
• [Learn Python](https://www.learnpython.org/) - Interactive
• [Project Python](http://projectpython.net) - Interactive
• [Python Video Tutorials](https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU) - Video
• [MIT OpenCourseWare](http://ocw.mit.edu/6-0001F16) - Course
• @PythonRes - Channel
"""


@Client.on_message(command("res"))
async def res(_, message: Message):
    """Good Python resources"""
    await reply_and_delete(message, RES)


################################


LEARN = "Your issue is not related to Pyrogram. Please, learn more Python and try again.\n" + RES


@Client.on_message(command("learn"))
async def learn(_, message: Message):
    """Tell to learn Python"""
    await reply_and_delete(message, LEARN)


################################


RULES = """
**Pyrogram Rules**

` 1.` English only. Other groups by language: #groups.
` 2.` Spam, flood and hate speech is forbidden.
` 3.` Talks unrelated to Pyrogram are not allowed.
` 4.` The offtopic group is at @PyrogramLounge.
` 5.` Keep unrelated media/emojis to a minimum.
` 6.` Use your common sense (yes, you have it too).
` 7.` Be nice and respect other people.
` 8.` Ask before sending PMs and respect answers.
` 9.` "Doesn't work" means nothing. Explain issues in details.
`10.` Don't ask if your code is correct. Ask if you encounter errors.
`11.` Make use of nekobin.com for sharing long code.
"""


@Client.on_message(command("rules"))
async def rules(_, message: Message):
    """Show Pyrogram rules"""
    # noinspection PyBroadException
    try:
        index = int(message.command[1])
        split = RULES.strip().split("\n")
        text = f"{split[0]}\n\n{split[index + 1]}"
    except Exception:
        text = RULES

    await reply_and_delete(message, text)


################################


GROUPS = f"""
**Pyrogram group chats**

__Main groups__
[{Emoji.GLOBE_WITH_MERIDIANS} International (English)](t.me/PyrogramChat)
[{Emoji.SPEECH_BALLOON} Offtopic group](t.me/PyrogramLounge)

__Other groups__
[{Emoji.ITALY} Italian](t.me/joinchat/AWDQ8lDPvwpWu3UH4Bx9Uw)
[{Emoji.IRAN} Farsi](t.me/PyrogramIR)
[{Emoji.BRAZIL} Portuguese](t.me/PyrogramBR)
[{Emoji.INDONESIA} Indonesian](t.me/PyrogramID)
[{Emoji.RUSSIA} Russian](t.me/RuPyrogram)

__If you want to host and maintain a group dedicated to your language, let us know!__
"""


@Client.on_message(command("groups"))
async def groups(_, message: Message):
    """Show all groups"""
    await reply_and_delete(message, GROUPS)


################################


FAQ = (
    "Your question has already been answered in the FAQ section of the documentation. "
    "Please, head on to [Pyrogram FAQs](https://docs.pyrogram.org/faq) now"
)


@Client.on_message(command("faq"))
async def faq(_, message: Message):
    """Answer is in the FAQ"""
    await reply_and_delete(message, FAQ)


################################


RTD = "Please, read the docs: https://docs.pyrogram.org"


@Client.on_message(command("rtd"))
async def rtd(_, message: Message):
    """Tell to Read the Docs"""
    await reply_and_delete(message, RTD)


################################


DEV = (
    "The fix for this issue has already been pushed to the `develop` branch on "
    "[GitHub](https://github.com/pyrogram/pyrogram). You can now upgrade Pyrogram with:\n\n"
    "`pip3 install -U https://github.com/pyrogram/pyrogram/archive/develop.zip`"
)


@Client.on_message(command("dev"))
async def dev(_, message: Message):
    """Fixed in dev branch"""
    await reply_and_delete(message, DEV)


################################

MESSAGE_DATE_DIFF = 43200  # 12h


@Client.on_message(command("delete"))
@administrators_only
async def delete(bot: Client, message: Message):
    """Delete messages"""
    reply = message.reply_to_message

    if not reply:
        return

    # Don't delete admins messages
    if await is_admin(bot, reply):
        m = await message.reply("Sorry, I don't delete administrators' messages.")
        await asyncio.sleep(5)
        await m.delete()
        return

    # Don't delete messages that are too old
    if message.date - reply.date > MESSAGE_DATE_DIFF:
        m = await message.reply("Sorry, I don't delete messages that are too old.")
        await asyncio.sleep(5)
        await m.delete()
        return

    cmd = message.command

    # No args, delete the mentioned message alone
    if len(cmd) == 1:
        await reply.delete()
        return

    # Delete the last N messages of the mentioned user, up to 200

    arg = int(cmd[1])

    # Min 1 max 200
    arg = max(arg, 1)
    arg = min(arg, 200)

    last_200 = range(reply.message_id, reply.message_id - 200, -1)

    message_ids = [
        m.message_id for m in filter(
            lambda m: m.from_user and m.from_user.id == reply.from_user.id,
            await bot.get_messages(message.chat.id, last_200, replies=0)
        )
    ]

    await bot.delete_messages(message.chat.id, message_ids[:arg])


################################

@Client.on_callback_query()
async def unban(bot: Client, query: CallbackQuery):
    action, user_id = query.data.split(".")
    user_id = int(user_id)
    text = query.message.text

    if action == "unban":
        if query.from_user.id != dan_id:
            await query.answer("Only Dan can pardon banned users", show_alert=True)
            return

        await bot.restrict_chat_member(
            query.message.chat.id,
            user_id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_stickers=True,
                can_send_animations=True,
                can_send_games=True,
                can_use_inline_bots=True,
                can_add_web_page_previews=True,
                can_send_polls=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True
            )
        )

        await query.edit_message_text(f"~~{text.markdown}~~\n\nPardoned")


@Client.on_message(command("ban"))
@administrators_only
async def ban(bot: Client, message: Message):
    """Ban a user in chat"""
    reply = message.reply_to_message

    if not reply:
        return

    # Don't ban admins
    if await is_admin(bot, reply):
        m = await message.reply("Sorry, I don't ban administrators")
        await asyncio.sleep(5)
        await m.delete()
        return

    await bot.restrict_chat_member(message.chat.id, reply.from_user.id, ChatPermissions())

    await message.reply(
        f"__Banned {reply.from_user:mention} indefinitely__",
        quote=False,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Give grace", f"unban.{reply.from_user.id}")
        ]])
    )


################################

nl = "\n"

HELP = f"""
**List of available commands**

{nl.join(
    f"• #{fn[0]}{'`*`' if hasattr(fn[1], 'admin') else ''} - {fn[1].__doc__}"
    for fn in locals().items()
    if hasattr(fn[1], "handler")
    and fn[0] not in ["unban"])}

`*` Administrators only
"""


# noinspection PyShadowingBuiltins
@Client.on_message(command("help"))
async def help(_, message: Message):
    """Show this message"""
    await reply_and_delete(message, HELP)
