from YMusic import app
from YMusic.misc import SUDOERS
from YMusic.utils.queue import get_queue
from YMusic.filters import command
from YMusic.utils.formaters import get_readable_time, format_time
from pyrogram import filters
import time
import config

PLAY_START_TIME = {}

@app.on_message(command(["رابط"]))
async def _current(_, message):
    chat_id = message.chat.id

    try:
        queue = get_queue(chat_id)
        if not queue:
            await message.reply_text("- لايوجد صوت في الانتضار .")
            return

        current_song = queue[0]
        title = current_song['title']
        duration = current_song['duration']
        link = current_song['link']
        reqname = current_song['requester_name']
        reqid = current_song['requester_id']
        total_duration = format_time(duration)

        if chat_id in PLAY_START_TIME:
            elapsed_time = int(time.time() - PLAY_START_TIME[chat_id])
            current_time = format_time(elapsed_time)

            await message.reply_text(
                f" معلومات الصوت :\n\n"
                f"الرابط : [{title}]({link})\n"
                f"المدة : {current_time} / {total_duration}\n"
                f"طلب : [{reqname}](tg://user?id={reqid})",
                disable_web_page_preview=True
            )
        else:

            await message.reply_text(
                f"معلومات الصوت :\n\n"
                f"الرابط: [{title}]({link})\n"
                f"المدة: {total_duration}\n"
                f"طلب : [{reqname}](tg://user?id={reqid})",
                disable_web_page_preview=True
            )

    except Exception as e:
        await message.reply_text(f"خطا: {str(e)}")

async def start_play_time(chat_id):
    PLAY_START_TIME[chat_id] = time.time()

async def stop_play_time(chat_id):
    if chat_id in PLAY_START_TIME:
        del PLAY_START_TIME[chat_id]
        
