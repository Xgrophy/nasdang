#
# Copyright (C) 2021-2022 by kenkansaja@Github, < https://github.com/kenkansaja >.
#
# This file is part of < https://github.com/kenkansaja/Musikku > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/kenkansaja/Musikku/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters
from pyrogram.types import Message
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from strings import get_command
from Musikku import app
from Musikku.core.call import Musikku
from Musikku.utils.decorators.play import PlayWrapper
from Musikku.utils.logger import play_logs
from Musikku.utils.stream.stream import stream

# Command
STREAM_COMMAND = get_command("STREAM_COMMAND")


@app.on_message(
    filters.command(STREAM_COMMAND) & filters.group & ~BANNED_USERS
)
@PlayWrapper
async def stream_command(
    client,
    message: Message,
    _,
    chat_id,
    video,
    channel,
    playmode,
    url,
):
    if url:
        mystic = await message.reply_text(
            _["play_2"].format(channel) if channel else _["play_1"]
        )
        try:
            await Musikku.stream_call(url)
        except NoActiveGroupCall:
            await mystic.edit_text(
                "There's an issue with the bot. Please report it to my owner and ask them to check logger group."
            )
            return await app.send_message(
                config.LOG_GROUP_ID,
                "Please turn on Voice Chat.. Bot is not able to stream urls..",
            )
        except Exception as e:
            return await mystic.edit_text(
                _["general_3"].format(type(e).__name__)
            )
        await mystic.edit_text(_["str_2"])
        try:
            await stream(
                _,
                mystic,
                message.from_user.id,
                url,
                chat_id,
                message.from_user.first_name,
                message.chat.id,
                video=True,
                streamtype="index",
            )
        except Exception as e:
            ex_type = type(e).__name__
            err = (
                e
                if ex_type == "AssistantErr"
                else _["general_3"].format(ex_type)
            )
            return await mystic.edit_text(err)
        return await play_logs(
            message, streamtype="M3u8 or Index Link"
        )
    else:
        await mystic.edit_text(_["str_1"])
