from YMusic import call, app
from YMusic.core import userbot
from YMusic.utils.queue import QUEUE, pop_an_item, get_queue, clear_queue, is_queue_empty, get_current_song
from YMusic.utils.loop import get_loop
from YMusic.misc import SUDOERS
from YMusic.plugins.pytgcalls.pytgcalls import stop
from YMusic.plugins.sounds.current import start_play_time, stop_play_time
from YMusic.utils.utils import clear_downloads_cache, send_song_info
from YMusic.utils.formaters import get_readable_time, format_time
from YMusic.filters import command
from pytgcalls.types import MediaStream
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
import logging
from config import OWNER_ID

logger = logging.getLogger(__name__)

@app.on_message(command(["التالي", "تخطي", "سكب"]) & filters.group)
async def _aSkip(_, message):
    chat_id = message.chat.id
    administrators = []
    async for admin in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        administrators.append(admin)

    if (message.from_user.id in SUDOERS) or (message.from_user.id in [admin.user.id for admin in administrators]):
        if is_queue_empty(chat_id):
            await message.reply_text("Tidak ada lagu yang sedang diputar untuk di-skip.")
            return            
   
    m = await message.reply_text("⦗ جارٍ التخطي ⦘")
    await stop_play_time(chat_id)
    try:
        popped_item = pop_an_item(chat_id)
        if not popped_item:
            await m.edit("⦗ لايوجد شي بقائمة الانتضار , تم الخروج وتنظيف الذاكرة ⦘")
            await stop(chat_id)
            await clear_downloads_cache()
        else:
            next_song = get_current_song(chat_id)
            if next_song:
                if next_song['is_video']:
                    await userbot.playVideo(chat_id, next_song['audio_file'])
                else:
                    await userbot.playAudio(chat_id, next_song['audio_file'])
                await start_play_time(chat_id)
                await m.delete()
                await send_song_info(chat_id, next_song)
            else:
                await m.edit("⦗ لايوجد شي بقائمة الانتضار , تم الخروج وتنظيف الذاكرة ⦘")
                await stop(chat_id)
                await clear_downloads_cache()
    except Exception as e:
        logger.error(f"خطأ في _aSkipGroup للدردشة {chat_id}: {e}")
        await m.edit(f"حدث خطأ: {str(e)}")

@app.on_message(command(["التالي", "تخطي", "سكب"]) & (filters.channel | filters.private))
async def _aSkipChannel(_, message):
    chat_id = message.chat.id

    if is_queue_empty(chat_id):
        await message.reply_text("⦗ لايوجد شيء لتخطيةة ⦘")
        return

    m = await message.reply_text("⦗ جارٍ التخطي ⦘")
    await stop_play_time(chat_id)
    try:
        popped_item = pop_an_item(chat_id)
        if not popped_item:
            await m.edit("⦗ لايوجد شي بقائمة الانتضار , تم الخروج وتنظيف الذاكرة ⦘")
            await stop(chat_id)
            await clear_downloads_cache()
        else:
            next_song = get_current_song(chat_id)
            if next_song:
                if next_song['is_video']:
                    await userbot.playVideo(chat_id, next_song['audio_file'])
                else:
                    await userbot.playAudio(chat_id, next_song['audio_file'])
                await start_play_time(chat_id)
                await m.delete()
                await send_song_info(chat_id, next_song)
            else:
                await m.edit("⦗ لايوجد شي بقائمة الانتضار , تم الخروج وتنظيف الذاكرة ⦘")
                await stop(chat_id)
                await clear_downloads_cache()
    except Exception as e:
        logger.error(f"خطأ في _aSkipChannel للدردشة {chat_id}: {e}")
        await m.edit(f"حدث خطأ: {str(e)}")
        
