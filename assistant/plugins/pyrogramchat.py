# MIT License
#
# Copyright (c) 2019 Dan Tès <https://github.com/delivrance>
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

from time import time

from pyrogram import (CallbackQuery, Emoji, Filters, InlineKeyboardButton,
                      InlineKeyboardMarkup, Message)

from ..assistant import Assistant
from ..utils import docs, callback


ALLOWED_CHATS = [-1001221450384, -1001387666944]
chat_filter = Filters.create("Chat", lambda _, m: bool(m.chat and m.chat.id in ALLOWED_CHATS))

MENTION = "[{}](tg://user?id={})"
MESSAGE = "{} Welcome to [Pyrogram](https://docs.pyrogram.org/)'s group chat {}!"




# Filter in only new_chat_members updates generated in TARGET chat
@Assistant.on_message(chat_filter & Filters.new_chat_members)
def welcome(bot: Assistant, message: Message):
    for new_user in message.new_chat_members:
        bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=new_user.id,
            until_date=int(time()) + 604800,
            can_send_messages=False)
        mention = MENTION.format(new_user.first_name, new_user.id)
        greeting = MESSAGE.format(Emoji.SPARKLES, mention)
        kb = pyro_keyboard(user_id=new_user.id, confirmed=False, chat_id=message.chat.id)  
        reply_markups = InlineKeyboardMarkup(kb)
        message.reply(
            text=greeting + "\nTo be able to participate, please press the button below " + Emoji.DOWN_ARROW,
            disable_web_page_preview=True,
            reply_markup=reply_markups
        )


@Assistant.on_callback_query()
def callback_query_pyro(bot: Assistant, cb: CallbackQuery):
    
    data = cb.data.encode('UTF-8') 
    
    user_id = cb.from_user.id 
    
    chat_id = cb.message.chat.id 
    cht = [cb.message.chat.username]
    dataid = cb.id
    res = [item for item in TARGET if item in cht] 
    username = cb.message.chat.username
    data = data.split(b'%') 
    chat = ''.join(str(e) for e in res)
    chat_id = str(chat_id)
    action = ''
    confirmed = False
    
    for elem in data:
        name, *args = elem.split(b'=') 
        if name == b'act':
            action = args[0]
        elif name == b'chat_id':
            chatid = int(args[0])
        elif name == b'user_id':
            userid = int(args[0])
        elif name == b'cnf':
            confirmed = bool(int(args[0]))
            
    if action == b"unres":
        if username == chat:
            if user_id == int(userid):
                if not confirmed:
                    bot.restrict_chat_member(
                      chat_id=chat,
                      user_id=int(userid),
                      until_date=0,
                      can_send_messages=True,
                      can_send_media_messages=True,
                      can_send_other_messages=True,
                      can_add_web_page_previews=True,
                      can_send_polls=True)
                    
                    cb.answer("Your restriction were lifted, welcome!")
              
                    bot.edit_message_text(
                      chat_id=chat,
                      message_id=cb.message.message_id,
                      text=cb.message.text.markdown.split('\n')[0],
                      disable_web_page_preview=True,
                      reply_markup=None)
            else:
                cb.answer("That wasn't your button!", show_alert=True)


@Assistant.on_message(chat_filter & Filters.command("un", "!"))
def unrestrict_members(bot: Assistant, message: Message):
    print(message)
    caller = bot.get_chat_member(message.chat.id, message.from_user.id)
    if caller.status is 'creator' or caller.status is 'administrator' and caller.permissions.can_restrict_members:
        bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            until_date=0,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_send_polls=True)
        message.reply("Restrictions lifted " + Emoji.OK_HAND)
