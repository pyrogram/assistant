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

import asyncio
import time
from functools import partial, wraps

import aiohttp
from num2words import num2words
from pyrogram import filters, emoji
from pyrogram.types import CallbackQuery, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup, Message

from ..assistant import Assistant
from ..utils import docs

command = partial(filters.command, prefixes=list("#!"))


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


def admins_only(func):
    @wraps(func)
    async def decorator(bot: Assistant, message: Message):
        if bot.is_admin(message):
            await func(bot, message)

        await message.delete()

    decorator.admin = True

    return decorator


################################

PING_TTL = 5


@Assistant.on_message(command("ping"))
async def ping(_, message: Message):
    """Ping the assistant"""
    start = time.time()
    reply = await message.reply_text("...")
    delta_ping = time.time() - start
    await reply.edit_text(f"**Pong!** `{delta_ping * 1000:.3f} ms`")


################################


SCHEMA = "https"
BASE = "nekobin.com"
ENDPOINT = f"{SCHEMA}://{BASE}/api/documents"
ANSWER = "**Long message from** {}\n{}"
TIMEOUT = 3
MESSAGE_ID_DIFF = 100


@Assistant.on_message(command("neko"))
@admins_only
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

    await reply_and_delete(reply, ANSWER.format(reply.from_user.mention, f"{BASE}/{key}.py"))


################################


LOG = """
Enable Logging: add the following on the top of your script and run it again:

```import logging
logging.basicConfig(level=logging.INFO)```

For a more verbose logging, use `level=logging.DEBUG` instead.
"""


@Assistant.on_message(command("log"))
async def log(_, message: Message):
    """Enable debug logging"""
    await reply_and_delete(message, LOG)


################################


EX = """
Please, provide us a **minimal** and **reproducible** example in order to easily understand and reproduce the problem.

[How do I create a minimal, reproducible example?](https://stackoverflow.com/help/minimal-reproducible-example)
"""


@Assistant.on_message(command("ex"))
async def ex(_, message: Message):
    """Ask for minimal example"""
    await reply_and_delete(message, EX)


################################


OT = [
    "This argument is off-topic and not related to Pyrogram. Please, move the discussion to @PyrogramLounge",
    "Looks like this topic is related to Pyrogram. You can discuss at @PyrogramChat"
]


@Assistant.on_message(command("ot"))
async def ot(_, message: Message):
    """offtopic conversation"""
    answer = OT[0] if message.chat.id == -1001387666944 else OT[1]  # @PyrogramChat id
    await reply_and_delete(message, answer)


################################


ASK = """
Sorry, your question is not well formulated. Please, be clear and try to follow the guidelines in the link below.

[How do I ask a good question?](https://stackoverflow.com/help/how-to-ask)
"""


@Assistant.on_message(command("ask"))
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


@Assistant.on_message(command("res"))
async def res(_, message: Message):
    """Good Python resources"""
    await reply_and_delete(message, RES)


################################


LEARN = "Your issue is not related to Pyrogram. Please, learn more Python and try again.\n" + RES


@Assistant.on_message(command("learn"))
async def learn(_, message: Message):
    """Tell to learn Python"""
    await reply_and_delete(message, LEARN)


################################


# One place for all rules, the docs.
RULES = docs.rules


@Assistant.on_message(command("rules"))
async def rules(_, message: Message):
    """Show Pyrogram rules"""
    # Still ugly. Patching Colin's code.
    # noinspection PyBroadException
    try:
        index = int(message.command[1])
        split = RULES.strip().split("\n")
        text = f"{split[0]}\n\n{split[index + 2]}"
    except Exception:
        text = RULES

    await reply_and_delete(message, text)


@Assistant.on_message(
    filters.via_bot
    & filters.regex(r"^Pyrogram Rules\n")
    & ~filters.regex(r"^Pyrogram Rules[\s\S]+notice\.$")
)  # I know this is ugly, but this way we don't filter the full ruleset lol
async def repost_rules(_, message: Message):
    code = message.entities[-1]
    index = int(message.text[code.offset:code.offset + code.length][:-1])
    split = RULES.split("\n")
    text = f"{split[1]}\n\n{split[3:-3][index]}"
    # First split index is a newline, thus using 1,
    # also -1 because we have a literal in the message, not a list index :D
    await reply_and_delete(message, text)


################################


GROUPS = f"""
**Pyrogram group chats**

__Main groups__
[{emoji.GLOBE_WITH_MERIDIANS} International (English)](t.me/PyrogramChat)
[{emoji.SPEECH_BALLOON} Offtopic group](t.me/PyrogramLounge)

__Other groups__
[{emoji.FLAG_ITALY} Italian](t.me/joinchat/AWDQ8lDPvwpWu3UH4Bx9Uw)
[{emoji.FLAG_IRAN} Farsi](t.me/PyrogramIR)
[{emoji.FLAG_BRAZIL} Portuguese](t.me/PyrogramBR)
[{emoji.FLAG_INDONESIA} Indonesian](t.me/PyrogramID)
[{emoji.FLAG_RUSSIA} Russian](t.me/RuPyrogram)
[{emoji.FLAG_ISRAEL} Hebrew](t.me/PyrogramHe)

__If you want to host and maintain a group dedicated to your language, let us know!__
"""


@Assistant.on_message(command("groups"))
async def groups(_, message: Message):
    """Show all groups"""
    await reply_and_delete(message, GROUPS)


################################


FAQ = (
    "Your question has already been answered in the FAQ section of the documentation. "
    "Please, head on to [Pyrogram FAQs](https://docs.pyrogram.org/faq) now"
)


@Assistant.on_message(command("faq"))
async def faq(_, message: Message):
    """Answer is in the FAQ"""
    await reply_and_delete(message, FAQ)


################################


RTD = "Please, read the docs: https://docs.pyrogram.org"


@Assistant.on_message(command("rtd"))
async def rtd(_, message: Message):
    """Tell to RTD (gentle)"""
    await reply_and_delete(message, RTD)


################################


RTFD = "You seem to be lost...\n\nGo read the **fscking docs**: https://docs.pyrogram.org"


@Assistant.on_message(command("rtfd"))
@admins_only
async def rtfd(_, message: Message):
    """Tell to RTFD (rude)"""
    await asyncio.gather(
        message.delete(),
        message.reply_photo(
            "https://i.imgur.com/a08Ju2e.png",
            quote=False,
            caption=RTFD,
            reply_to_message_id=getattr(
                message.reply_to_message,
                "message_id", None
            )
        )
    )


################################


FMT = (
    "Please format your code with triple backticks to make it more readable.\n"
    "<code>```your code here```</code>"
)


@Assistant.on_message(command("fmt"))
@admins_only
async def fmt(_, message: Message):
    """Tell to format code"""
    await asyncio.gather(
        message.delete(),
        message.reply(
            FMT,
            quote=False,
            parse_mode="html",
            disable_web_page_preview=True,
            reply_to_message_id=getattr(
                message.reply_to_message,
                "message_id", None
            ),
        )
    )


################################


DEV = (
    "The fix for this issue has already been pushed to the `master` branch on "
    "[GitHub](https://github.com/pyrogram/pyrogram). You can now upgrade Pyrogram with:\n\n"
    "`pip3 install -U https://github.com/pyrogram/pyrogram/archive/master.zip`"
)


@Assistant.on_message(command("dev"))
async def dev(_, message: Message):
    """Fixed in dev branch"""
    await reply_and_delete(message, DEV)


################################

MESSAGE_DATE_DIFF = 43200  # 12h


@Assistant.on_message(command("delete"))
@admins_only
async def delete(bot: Assistant, message: Message):
    """Delete messages"""
    reply = message.reply_to_message

    if not reply:
        return

    # Don't delete admins messages
    if bot.is_admin(reply):
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

@Assistant.on_message(command("ban"))
@admins_only
async def ban(bot: Assistant, message: Message):
    """Ban a user in chat"""
    reply = message.reply_to_message

    if not reply:
        return

    # Don't ban admins
    if bot.is_admin(reply):
        m = await message.reply("Sorry, I don't ban administrators")
        await asyncio.sleep(5)
        await m.delete()
        return

    await bot.restrict_chat_member(message.chat.id, reply.from_user.id, ChatPermissions())

    await message.reply(
        f"__Banned {reply.from_user.mention} indefinitely__",
        quote=False,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Give grace", f"unban.{reply.from_user.id}")
        ]])
    )


################################

@Assistant.on_message(command("kick"))
@admins_only
async def kick(bot: Assistant, message: Message):
    """Kick (they can rejoin)"""
    reply = message.reply_to_message

    if not reply:
        return

    # Don't kick admins
    if bot.is_admin(reply):
        m = await message.reply("Sorry, I don't kick administrators")
        await asyncio.sleep(5)
        await m.delete()
        return

    # Default ban until_time 60 seconds later as failsafe in case unban doesn't work
    # (can happen in case the server processes unban before ban and thus ignoring unban)
    await bot.kick_chat_member(message.chat.id, reply.from_user.id, int(time.time()) + 60)

    await message.reply(
        f"__Kicked {reply.from_user.mention}. They can rejoin__",
        quote=False
    )

    await asyncio.sleep(5)  # Sleep to allow the server some time to process the kick
    await bot.unban_chat_member(message.chat.id, reply.from_user.id)


################################

@Assistant.on_message(command("nab"))
@admins_only
async def nab(bot: Assistant, message: Message):
    reply = message.reply_to_message

    if not reply:
        return

    target = reply.from_user

    if target.id in [bot.CREATOR_ID, bot.ASSISTANT_ID]:
        target = message.from_user

    await message.reply(
        f"__Banned {target.mention} indefinitely__",
        quote=False
    )


################################

LOCKED = f"{emoji.LOCKED} Chat has been locked. Send #unlock to unlock."
UNLOCKED = f"{emoji.UNLOCKED} Chat has been unlocked."

PERMISSIONS = {
    -1001387666944: ChatPermissions(  # Inn
        can_send_messages=True,
        can_send_media_messages=True,
        can_use_inline_bots=True
    ),
    -1001221450384: ChatPermissions(  # Lounge
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_stickers=True,
        can_send_animations=True,
        can_send_games=True,
        can_use_inline_bots=True,
        can_send_polls=True
    ),
    -1001355792138: ChatPermissions(  # Italian Group
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_stickers=True,
        can_send_animations=True,
        can_send_games=True,
        can_use_inline_bots=True
    )
}


@Assistant.on_message(command("lock"))
@admins_only
async def lock(bot: Assistant, message: Message):
    """Lock the Chat"""
    await bot.set_chat_permissions(message.chat.id, ChatPermissions(can_send_messages=False))
    await reply_and_delete(message, LOCKED)


@Assistant.on_message(command("unlock"))
@admins_only
async def unlock(bot: Assistant, message: Message):
    """Unlock the Chat"""
    await bot.set_chat_permissions(message.chat.id, PERMISSIONS[message.chat.id])
    await reply_and_delete(message, UNLOCKED)


################################

EVIL = (
    "Pyrogram is free, open-source and community driven software; "
    "this means you are completely free to use it for any purpose whatsoever. "
    "However, help and support is a privilege and nobody is obligated to assist you, "
    "especially if you want to misbehave or harm Telegram with evil actions."
)


@Assistant.on_message(command("evil"))
async def evil(_, message: Message):
    """No help for evil actions"""
    await reply_and_delete(message, EVIL)


################################

# Pattern: https://regex101.com/r/6xdeRf/3
@Assistant.on_callback_query(filters.regex(r"^(?P<action>remove|unban)\.(?P<uid>\d+)"))
async def cb_query(bot: Assistant, query: CallbackQuery):
    match = query.matches[0]
    action = match.group("action")
    user_id = int(match.group("uid"))
    text = query.message.text

    if action == "unban":
        if query.from_user.id != Assistant.CREATOR_ID:
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

    if action == "remove":
        # Dummy Message object to check if the user is admin.
        # Re: https://t.me/pyrogramlounge/324583
        dummy = Message(
            message_id=0,
            from_user=query.from_user,
            chat=query.message.chat
        )
        if query.from_user.id == user_id or bot.is_admin(dummy):
            await query.answer()
            await query.message.delete()
        else:
            await query.answer("Only Admins can remove the help messages.")


################################

@Assistant.on_message(command("up"))
async def up(bot: Assistant, message: Message):
    """Show Assistant's uptime"""
    uptime = time.monotonic_ns() - bot.uptime_reference

    us, ns = divmod(uptime, 1000)
    ms, us = divmod(us, 1000)
    s, ms = divmod(ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    try:
        arg = message.command[1]
    except IndexError:
        await reply_and_delete(message, f"**Uptime**: `{d}d {h}h {m}m {s}s`")
    else:
        if arg == "-v":
            await reply_and_delete(
                message,
                f"**Uptime**: `{d}d {h}h {m}m {s}s {ms}ms {us}μs {ns}ns`\n"
                f"**Since**: `{bot.start_datetime} UTC`"
            )
        elif arg == "-p":
            await reply_and_delete(
                message,
                f"**Uptime**: "
                f"`{num2words(d)} days, {num2words(h)} hours, {num2words(m)} minutes, "
                f"{num2words(s)} seconds, {num2words(ms)} milliseconds, "
                f"{num2words(us)} microseconds, {num2words(ns)} nanoseconds`\n"
                f""
                f"**Since**: `year {num2words(bot.start_datetime.year)}, "
                f"month {bot.start_datetime.strftime('%B').lower()}, day {num2words(bot.start_datetime.day)}, "
                f"hour {num2words(bot.start_datetime.hour)}, minute {num2words(bot.start_datetime.minute)}, "
                f"second {num2words(bot.start_datetime.second)}, "
                f"microsecond {num2words(bot.start_datetime.microsecond)}, Coordinated Universal Time`"
            )
        else:
            await message.delete()


################################

# noinspection PyShadowingBuiltins
@Assistant.on_message(command("help"))
async def help(bot: Assistant, message: Message):
    """Show this message"""
    await asyncio.gather(
        message.delete(),
        message.reply(
            HELP,
            quote=False,
            reply_to_message_id=getattr(
                message.reply_to_message,
                "message_id", None
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Remove Help", f"remove.{message.from_user.id}")
            ]]),
        )
    )


################################

nl = "\n"

HELP = f"""
**List of available commands**

{nl.join(
    f"• #{fn[0]}{'`*`' if hasattr(fn[1], 'admin') else ''} - {fn[1].__doc__}"
    for fn in locals().items()
    if hasattr(fn[1], "handler")
    and fn[0] not in ["cb_query", "repost_rules", "nab"])}

`*` Administrators only
"""
