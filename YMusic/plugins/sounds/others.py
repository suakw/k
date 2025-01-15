from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from config import OWNER_ID
from YMusic import app
from YMusic.utils.queue import clear_queue
from YMusic.utils.loop import get_loop, set_loop
from YMusic.utils.utils import clear_downloads_cache
from YMusic.core import userbot
from YMusic.misc import SUDOERS
from YMusic.filters import command
import config

def add_sudo(user_id: int):
    global SUDOERS
    SUDOERS.add(user_id)

def remove_sudo(user_id: int):
    global SUDOERS
    if user_id in SUDOERS:
        SUDOERS.remove(user_id)

@app.on_message(command(["ايقاف", "اوكف", "stop", "ستوب"]) & filters.channel)
async def _stop(_, message):
    Text = await userbot.stop(message.chat.id)
    try:
        clear_queue(message.chat.id)
        await clear_downloads_cache()
    except: 
        pass
    await message.reply_text(Text)

@app.on_message(command(["مؤقت"]) & filters.channel)
async def _pause(_, message):
    Text = await userbot.pause(message.chat.id)
    await message.reply_text(Text)

@app.on_message(command(["استمرار"]) & filters.channel)
async def _resume(_, message):
    Text = await userbot.resume(message.chat.id)
    await message.reply_text(Text)

@app.on_message(command(["تكرار"]) & filters.channel)
async def _loop(_, message):
    loop = await get_loop(message.chat.id)
    if loop == 0:
        try:
            await set_loop(message.chat.id, 5)
            await message.reply_text("- تم تفعيل التكرار، سيتم تشغيل الصوت الحالي 5 مرات .")
        except Exception as e:
            return await message.reply_text(f"خطأ: <code>{str(e)}</code>")
    else:
        await message.reply_text("- عزيزي التكرار مفعل بالفعل .")

@app.on_message(command(["ايقاف التكرار"]) & filters.channel)
async def _endLoop(_, message):
    loop = await get_loop(message.chat.id)
    if loop == 0:
        await message.reply_text("- التكرار غير مفعل .")
    else:
        try:
            await set_loop(message.chat.id, 0)
            await message.reply_text("- تم إيقاف التكرار بنجاح .")
        except Exception as e:
            return await message.reply_text(f"خطأ: <code>{str(e)}</code>")

@app.on_message(command(["ايقاف", "اوكف", "stop", "ستوب"]) & filters.group)
async def _stop(_, message):
    # Get administrators
    administrators = []
    async for m in app.get_chat_members(
        message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
    ):
        administrators.append(m)
    if (message.from_user.id) in SUDOERS or (message.from_user.id) in [
        admin.user.id for admin in administrators
    ]:
        Text = await userbot.stop(message.chat.id)
        try:
            clear_queue(message.chat.id)
            await clear_downloads_cache()
        except:
            pass
        await message.reply_text(Text)
    else:
        return await message.reply_text(
            "⦗ الأمر للمشرفين فقط ⦘"
        )        
@app.on_message(command(["مؤقت"]) & filters.group)
async def _pause_group(_, message):
        # Get administrators
    administrators = []
    async for m in app.get_chat_members(
        message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
    ):
        administrators.append(m)
    if (message.from_user.id) in SUDOERS or (message.from_user.id) in [
        admin.user.id for admin in administrators
    ]:
        Text = await userbot.pause(message.chat.id)
        await message.reply_text(Text)
    else:
        return await message.reply_text(
            "⦗ الأمر للمشرفين فقط ⦘"
        )

@app.on_message(command(["استمرار"]) & filters.group)
async def _resume_group(_, message):
    administrators = []
    async for m in app.get_chat_members(
        message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
    ):
        administrators.append(m)
    if (message.from_user.id) in SUDOERS or (message.from_user.id) in [
        admin.user.id for admin in administrators
    ]:
        Text = await userbot.resume(message.chat.id)
        await message.reply_text(Text)
    else:
        return await message.reply_text(
            "⦗ الأمر للمشرفين فقط ⦘"
        )

@app.on_message(command(["تكرار"]) & filters.group)
async def _loop_group(_, message):
    administrators = []
    async for m in app.get_chat_members(
        message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
    ):
        administrators.append(m)
    if (message.from_user.id) in SUDOERS or (message.from_user.id) in [
        admin.user.id for admin in administrators
    ]:
       loop = await get_loop(message.chat.id)
    if loop == 0:
        try:
            await set_loop(message.chat.id, 5)
            await message.reply_text("- تم تفعيل التكرار، سيتم تشغيل الصوت الحالي 5 مرات .")
        except Exception as e:
            return await message.reply_text(f"خطأ: <code>{str(e)}</code>")
    else:
        await message.reply_text("- عزيزي التكرار مفعل بالفعل .")

@app.on_message(command(["ايقاف التكرار"]) & filters.group)
async def _endLoop_group(_, message):
    administrators = []
    async for m in app.get_chat_members(
        message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
    ):
        administrators.append(m)
    if (message.from_user.id) in SUDOERS or (message.from_user.id) in [
        admin.user.id for admin in administrators
    ]:
        loop = await get_loop(message.chat.id)
    if loop == 0:
        await message.reply_text("- التكرار غير مفعل .")
    else:
        try:
            await set_loop(message.chat.id, 0)
            await message.reply_text("- تم إيقاف التكرار .")
        except Exception as e:
            return await message.reply_text(f"خطأ: <code>{str(e)}</code>")

@app.on_message(command(["رفع مطور", "مط", "اضف"]) & filters.user(config.OWNER_ID))
async def _add_sudo(client, message):
    if len(message.command) != 2:
        await message.reply_text("- استخدام الامر : رفع مطور + الايدي الخاص بة")
        return
    
    try:
        user_id = int(message.command[1])
        if user_id in SUDOERS:
            await message.reply_text(f"- لايوجد هكذا ايدي .")
        else:
            add_sudo(user_id)
            await message.reply_text(f"- المستخدم {user_id} \n- تم ترقيتة مطور بنجاح .")
    except ValueError:
        await message.reply_text("- يجب ان يكون ايدي وليس معرف .")

@app.on_message(command(["ازالة مطور", "تنزيل مطور"]) & filters.user(config.OWNER_ID))
async def _remove_sudo(client, message):
    if len(message.command) != 2:
        await message.reply_text("- استخدام الامر : تنزيل مطور + الأيدي الخاص بة")
        return
    
    try:
        user_id = int(message.command[1])
        if user_id not in SUDOERS:
            await message.reply_text(f"- لايوجد هكذا ايدي في المطورين .")
        else:
            remove_sudo(user_id)
            await message.reply_text(f"- تم تنزيل {user_id} \n- من قائمة المطورين بنجاح .")
    except ValueError:
        await message.reply_text("- يجب ان يكون ايدي وليس معرف .")

@app.on_message(command(["المطورين", "عرض المطورين"]) & filters.user(config.OWNER_ID))
async def _sudo_list(client, message):
    sudo_list = ", ".join(str(sudo_id) for sudo_id in SUDOERS)
    await message.reply_text(f"- 🪬 قائمة مطورين الحساب :\n\n{sudo_list}")
    
@app.on_message(command(["الادنى"]) & filters.user(config.OWNER_ID))
async def set_max_duration(client, message):
    if len(message.command) != 2:
        await message.reply_text("- استخدام الامر : ادنى + عدد الدقائق")
        return
    
    try:
        new_duration = int(message.command[1])
        if new_duration <= 0:
            await message.reply_text("- عزيزي يجب ان تكون المدة اكثر من صفر دقيقة .")
            return
        
        global MAX_DURATION_MINUTES
        config.MAX_DURATION_MINUTES = new_duration
        await message.reply_text(f"- تم بنجاح تعيين الحد الادنى للتشغيل أصبح الآن {new_duration} دقيقة .")
    except ValueError:
        await message.reply_text("- حدث خطا غير معروف .")        
    
@app.on_message(command(["ايقاف", "اوكف", "stop", "ستوب"]) & filters.private)
async def _stop_private(_, message):
    user_id = message.from_user.id
    Text = await userbot.stop(user_id)
    if is_user_queue_empty(user_id):
        clear_queue(user_id) 
        
        try:
            clear_user_queue(user_id)  
            await clear_user_downloads_cache(user_id)  
        except:
            pass
    await message.reply_text(Text)

user_queues = {}

def is_user_queue_empty(user_id):
    return not user_queues.get(user_id, [])

@app.on_message(command(["مؤقت"]) & filters.private)
async def _pause_private(_, message):
    user_id = message.from_user.id
    Text = await userbot.pause(user_id)
    await message.reply_text(Text)

@app.on_message(command(["استمرار"]) & filters.private)
async def _resume_private(_, message):
    user_id = message.from_user.id
    Text = await userbot.resume(user_id)
    await message.reply_text(Text)

@app.on_message(command(["تكرار"]) & filters.private)
async def _loop_private(_, message):
    user_id = message.from_user.id
    loop = await get_user_loop(user_id)
    if loop == 0:
        try:
            await set_user_loop(user_id, 5)  
            await message.reply_text("- تم تفعيل التكرار، سيتم تشغيل الصوت الحالي 5 مرات.")
        except Exception as e:
            return await message.reply_text(f"خطأ: <code>{str(e)}</code>")
    else:
        await message.reply_text("- عزيزي التكرار مفعل بالفعل.")

@app.on_message(command(["ايقاف التكرار"]) & filters.private)
async def _endLoop_private(_, message):
    user_id = message.from_user.id
    loop = await get_user_loop(user_id)
    if loop == 0:
        await message.reply_text("- التكرار غير مفعل.")
    else:
        try:
            await set_user_loop(user_id, 0)
            await message.reply_text("- تم إيقاف التكرار.")
        except Exception as e:
            return await message.reply_text(f"خطأ: <code>{str(e)}</code>")
