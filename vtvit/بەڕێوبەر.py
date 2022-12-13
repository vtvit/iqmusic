from pyrogram import Client, filters
from pyrogram.types import Message

from config import HNDLR, call_py
from Musicjepthon.helpers.decorators import authorized_users_only
from Musicjepthon.helpers.handlers import skip_current_song, skip_item
from Musicjepthon.helpers.queues import QUEUE, clear_queue


@Client.on_message(filters.command(["skip"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def skip(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("**- هیچ شتێک لە لیستەکەدا نییە بۆ تێپەڕاندن**")
        elif op == 1:
            await m.reply("**")
        else:
            await m.reply(
                f"**⏭ تێپەڕاندنی پەخشکردن** \n**🎧 دۆخی کارکردن  ** - [{op[0]}]({op[1]}) | `{op[2]}`",
                disable_web_page_preview=True,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "**🗑️ ئەم گۆرانییانەی خوارەوە لە لیستەکە لابران : **"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#⃣{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(filters.command(["stop", "stop"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def stop(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("**✅ بەسەرکەوتوویی کۆتایی پێ هات **")
        except Exception as e:
            await m.reply(f"**شتێکی هەڵە هەیە ** \n`{e}`")
    else:
        await m.reply("**❌ هیچ گۆرانیەك لێرە دا کارناکات !**")


@Client.on_message(filters.command(["pause"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def pause(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                f"**⏸ وەستاندنی کاتی ئەنجامدرا.**\n\n•دەستپێکردنەوەی کارکردن ، بەکاربهێنە فەرمانی  » {HNDLR}reuse"
            )
        except Exception as e:
            await m.reply(f"**هەڵەیە** \n`{e}`")
    else:
        await m.reply("**- هیچ شتێك کارناکات!**")


@Client.on_message(filters.command(["reuse"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def resume(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                f"**▶ پەخش کردن دەستی پێکردەوە بۆ گۆرانی وەستاوەکە **\n\n•  بۆ وەستاندنی پەخشکردنی کاتی  ، بەکاربهێنە فەرمانی » {HNDLR}pause**"
            )
        except Exception as e:
            await m.reply(f"**هەڵەیە** \n`{e}`")
    else:
        await m.reply("** هیچ شتێك نە وەستێندراوە ❌**")
