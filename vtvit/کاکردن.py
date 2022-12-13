import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch

from config import HNDLR, bot, call_py, CHANNEL, PHOTO_CH
from Musicjepthon.helpers.queues import QUEUE, add_to_queue, get_queue

from io import BytesIO
from traceback import format_exc

import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message
from Python_ARQ import ARQ

from Musicjepthon.helpers.merrors import capture_err

ARQ_API_KEY = "HMPXNS-BDPCCB-UJKRPU-OQADHG-ARQ"
aiohttpsession = aiohttp.ClientSession()
arq = ARQ("https://thearq.tech", ARQ_API_KEY, aiohttpsession)


async def quotify(messages: list):
    response = await arq.quotly(messages)
    if not response.ok:
        return [False, response.result]
    sticker = response.result
    sticker = BytesIO(sticker)
    sticker.name = "sticker.webp"
    return [True, sticker]


def getArg(message: Message) -> str:
    arg = message.text.strip().split(None, 1)[1].strip()
    return arg


def isArgInt(message: Message) -> bool:
    count = getArg(message)
    try:
        count = int(count)
        return [True, count]
    except ValueError:
        return [False, 0]

# music player
def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        # CHANGE THIS BASED ON WHAT YOU WANT
        "bestaudio",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


# video player
def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        # CHANGE THIS BASED ON WHAT YOU WANT
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(filters.command(["play"], prefixes=f"{HNDLR}"))
async def play(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    m.chat.title
    if replied:
        if replied.audio or replied.voice:
            await m.delete()
            huehue = await replied.reply("**🔄 پێکرا کەمێك چاوەڕێ بکە**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:35] + "..."
                else:
                    songname = replied.audio.file_name[:35] + "..."
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://l.top4top.io/p_2363dcjiw1.jpg",
                    caption=f"""
**🏷️ ناونیشان : [{songname}]({link})
💬 ناسنامەی چات : {chat_id}
🎧 لە لایەن  : {m.from_user.mention}
💻 چەناڵ🕷️🖤 : [ چەناڵی سەرچاوە ](t.me/xv7amo)**
""",
                )
            else:
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.replyhttps_photo(
                    photo="https://l.top4top.io/p_2363dcjiw1.jpg",
                    caption=f"""
**▶ گۆرانیەکە پێکراوە🖤 
**🏷️ ناونیشان : [{songname}]({link})
💬 ناسنامەی چات : {chat_id}
🎧 لە لایەن : {m.from_user.mention}
💻 چەناڵ🕷️🖤 : [ چەناڵی سەرچاوە ](t.me/xv7amo)**
""",
                )

    else:
        if len(m.command) < 2:
            await m.reply("پێویستە وەڵامی گۆرانییەکە بدەیتەوە یان ناوی لەگەڵ فەرمانەکە بنووسە")
        else:
            await m.delete()
            huehue = await m.reply("🔎 لە گەڕاندایە تکایە کەمێك چاوەڕێ بکە ... ")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await huehue.edit("- هیچ شتێك نەدۆزرایەوە ")
            else:
                songname = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**- ببورە، شتێك هەڵەیە** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await huehue.delete()
                        await m.reply_photo(
                            photo=f"{thumbnail}",
                            caption=f"""
**🏷️  ناونیشان : [{songname}]({url})
⏱️ ماوەکەیی : {duration}
💬 ناسنامەی چات : {chat_id}
🎧 لە لایەن  : {m.from_user.mention}
💻 چەناڵ🕷️🖤 : [ چەناڵی سەرچاوە ](t.me/xv7amo)**
""",
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await huehue.delete()
                            # await m.reply_to_message.delete()
                            await m.reply_photo(
                                photo=f"{thumbnail}",
                                caption=f"""
**▶ گۆرانییەکە پەخشکرا
**🏷️  ناونیشان : [{songname}]({url})
⏱️ ماوەکەیی : {duration}
💬 ناسنامەی چات : {chat_id}
🎧 لەلایەن : {m.from_user.mention}💻
💻 چەناڵ🕷️🖤 : [ چەناڵی سەرچاوە ](t.me/xv7amo)**
""",
                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")


@Client.on_message(filters.command(["playvid"], prefixes=f"{HNDLR}"))
async def vplay(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    m.chat.title
    if replied:
        if replied.video or replied.document:
            await m.delete()
            huehue = await replied.reply("**🔄 پڕۆسەکە تەواو بوو**")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await huehue.edit(
                        "- ڕێگەپێدراوە تەنیا بە خولەكی 720, 480, 360 \n گەڕانەکە بە وردی ئەنجام دەدرێت 720p"
                    )

            if replied.video:
                songname = replied.video.file_name[:35] + "..."
            elif replied.document:
                songname = replied.document.file_name[:35] + "..."

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://l.top4top.io/p_2363dcjiw1.jpg",
                    caption=f"""
#⃣ ڤیدیۆ ... {pos}
**🏷️  ناونیشان : [{songname}]({url})
💬 ناسنامەی چات : {chat_id}
🎧 لەلایەن  : {m.from_user.mention}
💻 چەناڵ🕷️🖤 : [ چەناڵی سەرچاوە ](t.me/xv7amo)**
""",
                )
            else:
                if Q == 720:
                    hmmm = HighQualityVideo()
                elif Q == 480:
                    hmmm = MediumQualityVideo()
                elif Q == 360:
                    hmmm = LowQualityVideo()
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(dl, HighQualityAudio(), hmmm),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://l.top4top.io/p_2363dcjiw1.jpg",
                    caption=f"""
**🏷️  ناونیشان : [{songname}]({url})
💬 ناسنامەی چات : {chat_id}
🎧 لەلایەن  : {m.from_user.mention}
💻 چەناڵ🕷️🖤 : [ چەناڵی سەرچاوە ](t.me/xv7amo)**
""",
                )

    else:
        if len(m.command) < 2:
            await m.reply(
                "**یپێویستە وەڵامی ڤیدیۆکە بدەیتەوە یان ناوەکە دابنێی بۆ گەڕان بۆی و پەخشی بکە**"
            )
        else:
            await m.delete()
            huehue = await m.reply("**🔎 Aot")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            hmmm = HighQualityVideo()
            if search == 0:
                await huehue.edit(
                    "**هیچ شتێك لە گەڕانەکەدا نەدۆزرایەوە**"
                )
            else:
                songname = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**شتێکی هەڵە هەیە ⚠️** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await huehue.delete()
                        # await m.reply_to_message.delete()
                        await m.reply_photo(
                            photo=f"{thumbnail}",
                            caption=f"""
**🏷️  ناونیشان : [{songname}]({url})
⏱️ ماوەیی : {duration}
💬 ناسنامەی چات : {chat_id}
🎧 لەلایەن : {m.from_user.mention}
💻 چەناڵ🕷️🖤 : [ چەناڵی سەرچاوە ](t.me/xv7amo)**
""",
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(ytlink, HighQualityAudio(), hmmm),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await huehue.delete()
                            # await m.reply_to_message.delete()
                            await m.reply_photo(
                                photo=f"{thumbnail}",
                                caption=f"""
**🏷️  ناونیشان : [{songname}]({url})
⏱️ ماوەیی : {duration}
💬 ناسنامەی چات : {chat_id}
🎧 لەلایەن : {m.from_user.mention}
💻 چەناڵ🕷️🖤 : [ چەناڵی سەرچاوە ](t.me/jepthon)**
""",
                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")


@Client.on_message(filters.command(["playrandom"], prefixes=f"{HNDLR}"))
async def playfrom(client, m: Message):
    chat_id = m.chat.id
    if len(m.command) < 2:
        await m.reply(
            f"**بەکارهێنەر:** \n\n`{HNDLR} playrandom [ناسنامەی چات/ناوی بەکارهێنەر]` \n`{HNDLR} playrandom [ناسنامەی چات/ناوی بەکارهێنەر]`"
        )
    else:
        args = m.text.split(maxsplit=1)[1]
        if ";" in args:
            chat = args.split(";")[0]
            limit = int(args.split(";")[1])
        else:
            chat = args
            limit = 10
            lmt = 9
        await m.delete()
        hmm = await m.reply(f"🔎 بیهێنە {limit}  گۆرانی هەڕەمەکی  {chat}**")
        try:
            async for x in bot.search_messages(chat, limit=limit, filter="audio"):
                location = await x.download()
                if x.audio.title:
                    songname = x.audio.title[:30] + "..."
                else:
                    songname = x.audio.file_name[:30] + "..."
                link = x.link
                if chat_id in QUEUE:
                    add_to_queue(chat_id, songname, location, link, "Audio", 0)
                else:
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(location),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, location, link, "Audio", 0)
                    # await m.reply_to_message.delete()
                    await m.reply_photo(
                        photo="https://l.top4top.io/p_2363dcjiw1.jpg",
                        caption=f"""
**▶ دەستبکە بە پەخشکردنی گۆرانی لە {chat}
🏷️ ناونیشان : [{songname}]({link})
💬 ناسنامەی چات : {chat_id}
🎧 لەلایەن : {m.from_user.mention}
💻 چەناڵ🕷️🖤 : [ چەناڵی سەچاوە ](t.me/xv7amo)**
""",                  
         )
            await hmm.delete()
            await m.reply(  
                   f"➕ زیادبکە {lmt} گۆرانی لە لیستی پەخشکردن \n• بنێرە {HNDLR}playl بۆ زیادکردنی گۆرانی لە لیستی پەخشکردن**" 
                         )
        except Exception as e:
            await hmm.edit(f"**شتێك هەڵەیە  ** \n`{e}`")


@Client.on_message(filters.command(["playlist", "playlist"], prefixes=f"{HNDLR}"))
async def playlist(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await m.delete()
            await m.reply(
                f"**🎧 گۆرانی پەخشکراوە  :** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",
                disable_web_page_preview=True,
            )
        else:
            QUE = f"**🎧 گۆرانی پەخشکراوە ئێستا:** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}` \n\n**⏯ لیستی پەخشکراوەکان  :**"
            l = len(chat_queue)
            for x in range(1, l):
                hmm = chat_queue[x][0]
                hmmm = chat_queue[x][2]
                hmmmm = chat_queue[x][3]
                QUE = QUE + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`\n"
            await m.reply(QUE, disable_web_page_preview=True)
    else:
        await m.reply("**• هیچ شتێك پەخشنەکراوە ئەسڵەن**")
