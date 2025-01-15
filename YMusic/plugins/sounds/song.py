import os
import glob
import random
import wget
import requests
import re
import yt_dlp
import logging
import asyncio
from YMusic.filters import command
from YMusic import app
from pyrogram import Client, filters
from youtube_search import YoutubeSearch

def get_cookies_file():
    folder_path = f"{os.getcwd()}/cookies"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt_file = random.choice(txt_files)
    return cookie_txt_file

def sanitize_filename(title):
    return re.sub(r'[<>:"/\\|?*]', '', title).replace(' ', '_')

def download_audio(link, ydl_opts):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=False)
        audio_file = ydl.prepare_filename(info_dict)
        ydl.process_info(info_dict)
    return audio_file

@app.on_message(command(["song", "بحث", "تحميل", "تنزيل", "يوت", "yt"]) & (filters.private | filters.group | filters.channel))
async def song(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chutiya = message.from_user.mention

    query = " ".join(message.command[1:])
    
    m = await message.reply("⦗ جارٍ البحث ... ⦘")
    
    ydl_opts = {
        "format": "bestaudio[ext=m4a]",
        "cookiefile": get_cookies_file()
    }

    if "youtube.com" in query or "youtu.be" in query:
        link = query
    else:
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            link = f"https://youtube.com{results[0]['url_suffix']}"
        except Exception as e:
            await m.edit("⦗ لم يتم العثور على الصوت ⦘")
            logging.error(f"Failed to fetch YouTube video: {str(e)}")
            return

    await m.edit("⦗ جارٍ التحميل ... ⦘")

    try:
        loop = asyncio.get_event_loop()
        audio_file = await loop.run_in_executor(None, download_audio, link, ydl_opts)
        
        rep = f"- بواسطة : {chutiya}" if chutiya else "voice"
        
        await message.reply_audio(
            audio_file,
            caption=rep,
            performer=" voice .",
            thumb=None,
            title=None,
        )
        await m.delete()
    
    except Exception as e:
        await m.edit(f"[Victorious] **\n\\خطأ :** {e}")
        logging.error(f"Error while downloading audio: {str(e)}")

    finally:
        try:
            os.remove(audio_file)
        except Exception as e:
            logging.error(f"Failed to delete temporary files: {str(e)}")

@app.on_message(command(["نزلي فيديو","نزلي الفيديو"]) & (filters.private | filters.group | filters.channel))
async def vsong(client, message):
    ydl_opts = {
        "format": "best",
        "cookiefile": get_cookies_file(),
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quiet": True,
    }

    query = " ".join(message.command[1:])

    m = await message.reply("⦗ جارٍ البحث ... ⦘")

    if "youtube.com" in query or "youtu.be" in query:
        link = query
    else:
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            link = f"https://youtube.com{results[0]['url_suffix']}"
        except Exception as e:
            await m.edit("🚫 **خطأ:** لم يتم العثور على الفيديو")
            return

    await m.edit("⦗ جارٍ التحميل ... ⦘")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
        
        await message.reply_video(
            file_name,
            duration=int(ytdl_data["duration"]),
            thumb=None,
            caption=ytdl_data["title"],
        )

        await m.delete()  

    except Exception as e:
        await m.edit(f"🚫 **خطأ:** {e}")

    finally:
        try:
            os.remove(file_name)
        except Exception as e:
            logging.error(f"Failed to delete temporary files: {str(e)}")
