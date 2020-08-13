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

import time
from datetime import datetime

from pyrogram import Client, Message
from pyrogram import __version__
from pyrogram.api.all import layer


class Assistant(Client):
    CREATOR_ID = 23122162  # Dan (haskell)
    CHATS = [-1001387666944,  # Inn (pyrogramchat)
             -1001221450384,  # Lounge (pyrogramlounge)
             -1001355792138]  # Pyrogram Italia

    def __init__(self):
        name = self.__class__.__name__.lower()

        super().__init__(
            name,
            config_file=f"{name}.ini",
            workers=16,
            plugins=dict(
                root=f"{name}.plugins",
                exclude=["welcome"]
            )
        )

        self.admins = {
            chat: {Assistant.CREATOR_ID}
            for chat in Assistant.CHATS
        }

        self.uptime_reference = time.monotonic_ns()
        self.start_datetime = datetime.utcnow()

    async def start(self):
        await super().start()

        me = await self.get_me()
        print(f"Assistant for Pyrogram v{__version__} (Layer {layer}) started on @{me.username}. Hi.")

        # Fetch current admins from chats
        for chat, admins in self.admins.items():
            async for admin in self.iter_chat_members(chat, filter="administrators"):
                admins.add(admin.user.id)

    async def stop(self, *args):
        await super().stop()
        print("Pyrogram Assistant stopped. Bye.")

    def is_admin(self, message: Message) -> bool:
        user_id = message.from_user.id
        chat_id = message.chat.id

        return user_id in self.admins[chat_id]
