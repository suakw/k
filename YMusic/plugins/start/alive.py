from pyrogram import filters
from YMusic import app
from YMusic.misc import _boot_
from YMusic.filters import command
from YMusic.utils.formaters import get_readable_time
import config
import time


@app.on_message(command(["وقت التشغيل"]))
async def _ping(_, message):
    uptime = get_readable_time(int(time.time() - _boot_))
    await message.reply_text(f"- مدة التشغيل حتى الان : {uptime}")
