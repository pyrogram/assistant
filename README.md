# Pyrogram Assistant

> The assistant bot that helps people with [Pyrogram](//github.com/pyrogram/pyrogram) directly on Telegram.

This repository contains the source code of [@PyrogramBot](//t.me/pyrogrambot) and the instructions for running a
copy yourself. Beside its main purpose, the bot is featuring [**Pyrogram Asyncio**](//github.com/pyrogram/pyrogram/issues/181),
[**Smart Plugins**](//docs.pyrogram.org/topics/smart-plugins) and **Inline Mode**; feel free to explore the source code to
learn more about these topics.

## Requirements

- Python 3.6 or higher.
- A [Telegram API key](//docs.pyrogram.org/intro/setup#api-keys).
- A [Telegram bot token](//t.me/botfather).

## Run

1. `git clone https://github.com/pyrogram/assistant`, to download the source code.
2. `cd assistant`, to enter the directory.
3. `python3 -m venv venv && . venv/bin/activate` to create and activate a virtual environment.
3. `pip install -U -r requirements.txt`, to install the requirements.
4. Create a new `assistant.ini` file, copy-paste the following and replace the values with your own:
   ```ini
   [pyrogram]
   api_id = 12345
   api_hash = 0123456789abcdef0123456789abcdef
   bot_token = 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
   ```
5. Run with `python -m assistant`.
6. Stop with <kbd>CTRL+C</kbd> and `deactivate` the virtual environment.

## License

MIT © 2019-present [Dan](//github.com/delivrance)
