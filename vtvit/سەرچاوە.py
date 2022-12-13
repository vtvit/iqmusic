import os
import sys
from datetime import datetime
from time import time

from pyrogram import Client, filters
from pyrogram.types import Message

from config import HNDLR, SUDO_USERS, OWNER_NAME, CHANNEL

START_TIME = datetime.utcnow()
TIME_DURATION_UNITS = (
    ("یەکشەممە", 60 * 60 * 24 * 7),
    ("ڕۆژ", 60 * 60 * 24),
    ("کاتژمێر", 60 * 60),
    ("خولەك", 60),
    ("چرکە", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else ""))
    return ", ".join(parts)


@Client.on_message(filters.command(["پینگ"], prefixes=f"{HNDLR}"))
async def ping(client, m: Message):
    await m.delete()
    start = time()
    current_time = datetime.utcnow()
    m_reply = await m.reply_text("⚡")
    delta_ping = time() - start
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m_reply.edit(
        f"<b>🏓 پینگ/b> `{delta_ping * 1000:.3f} بە چرکە` \n<b>⏳ کار دەکات</b> - `{uptime}`"
    )


@Client.on_message(
    filters.user(SUDO_USERS) & filters.command(["دەستپێکردنەوە"], prefixes=f"{HNDLR}")
)
async def restart(client, m: Message):
    await m.delete()
    jepthon = await m.reply("1")
    await jepthon.edit("2")
    await jepthon.edit("3")
    await jepthon.edit("4")
    await jepthon.edit("5")
    await jepthon.edit("6")
    await jepthon.edit("7")
    await jepthon.edit("8")
    await jepthon.edit("9")
    await jepthon.edit("**سەرچاوەی میوزیك بەسەرکەوتوویی دەستیپێکردەوە ✓**")
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()


@Client.on_message(filters.command(["فەرمانەکان"], prefixes=f"{HNDLR}"))
async def help(client, m: Message):
    await m.delete()
    JEPM = f"""
👋 اهلا {m.from_user.mention}!
𝘰𝘳𝘥𝘦𝘳𝘴 𝘮𝘶𝘴𝘪𝘤 [ {OWNER_NAME} ](t.me/{CHANNEL})
——————×—————
⧉ | بۆ پەخشکردنی گۆرانی لە پەیوەندی دەنگی ⇦ [ `{HNDLR}play  + ناوی گۆرانی` ]
⧉ | بۆ پەخشکردنی گۆرانی لە پەیوەندی دەنگی  ⇦ [ `{HNDLR}playvid  + ناوی گۆرانی` ]
———————×———————
⧉ | بۆ وەستاندنی گۆرانی و ڤیدیۆ بۆ ماوەیەکی کاتی  ⇦ [ `{HNDLR}pause` ] 
⧉ | دووبارە دەستپێکردنەوەی گۆرانی ⇦  [ `{HNDLR}reuse` ]
⧉ | وەستاندنی گۆرانی  ⇦ [ `{HNDLR}stop` ] 
⧉ | بۆ تێپەڕاندنی گۆرانی بۆ دانەیەکی تر ⇦ [ `{HNDLR}skip` ]
⧉ | بۆ پەخشکردنی گۆرانی هەڕەمەکی لە گرووپ و چەناڵ  ⇦ [ `{HNDLR}playrandom` ]
———————×———————
⧉ | بۆ داگرتنی دەنگی  ⇦ [ `{HNDLR}داگرتن + ناوی گۆرانی یان بەستەر` ]
⧉ | بۆ داگرتنی ڤیدیۆ   ⇦  [ `{HNDLR}داگرتنی ڤیدیۆ + ناوی ڤیدیۆ یان بەستەر` ]
———————×———————
⧉ | بۆ دووبارە دەستپێکردنەوەی  دامەزراندن ⇦  [ `{HNDLR}دەستپێکردنەوە` ]
———————×———————
گەشەپێدەر 💻 : @VTVIT
چەناڵ 🎈 : @xv7amo
"""
    await m.reply(JEPM)


@Client.on_message(filters.command(["سەرچاوە"], prefixes=f"{HNDLR}"))
async def repo(client, m: Message):
    await m.delete()
    JEPM = f"""
<b>- مرحبا {m.from_user.mention}!
🎶 ئەمە سەرچاوەی بۆتی زیرەكی میوزیکە
🤖  لێهاتوویی ئەم بۆتەیە بۆ پەخشکردنی کلیپی دەنگی یان ڤیدیۆ لە پەیوەندی دەنگیدا.
⚒️ بۆ پیشاندانی فەرمانی سەرچاوە بنێرە  {HNDLR}فەرمانەکان
📚 • چەناڵی سەرچاوە  : @xv7amo</b>
"""
    await m.reply(JEPM, disable_web_page_preview=True)
