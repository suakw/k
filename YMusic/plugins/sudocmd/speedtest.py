from YMusic.misc import SUDOERS
from YMusic.filters import command
from YMusic import app
from pyrogram import filters
import speedtest
import asyncio
import config

def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("جار التحميل ")
        test.download()
        m = m.edit("جار الرفع ")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("النتيجة هي:")
    except Exception as e:
        return m.edit(e)
    return result


@app.on_message(command(["السرعة"]) & SUDOERS)
async def speedtest_function(client, message):
    m = await message.reply_text("- بدءً الان .")
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    output = f"""**نتيجة اختبار السرعة بواسطة Ookla**

__**العميل:**__
**__مزود الخدمة:__** {result['client']['isp']}
**__البلد:__** {result['client']['country']}
**__تقييم مزود الخدمة:__** {result['client']['isprating']}

__**الخادم:**__
**__الاسم:__** {result['server']['name']}
**__البلد:__** {result['server']['country']}, {result['server']['cc']}
**__الراعي:__** {result['server']['sponsor']}
**__الكمون:__** {result['server']['latency']}
**__البنك:__** {result['ping']}

__**السرعة:**__
**__سرعة التنزيل:__** {result['download'] / 1024 / 1024:.2f} ميجابت/ثانية
**__سرعة التحميل:__** {result['upload'] / 1024 / 1024:.2f} ميجابت/ثانية
"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=result["share"], caption=output
    )
    await m.delete()
