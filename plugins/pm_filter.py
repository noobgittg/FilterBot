import asyncio
import re
import ast
import math
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import ADMINS, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, P_TTI_SHOW_OFF, IMDB, \
    SINGLE_BUTTON, SPELL_CHECK_REPLY, IMDB_TEMPLATE
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings, create_invite_links
from database.users_chats_db import db
from info import HYPER_MODE
from database.ia_filterdb import Media, get_file_details, get_search_results
from database.filters_mdb import (
    del_all,
    find_filter,
    get_filters,
)
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}
SPELL_CHECK = {}


@Client.on_message(filters.group & filters.text & filters.incoming)
async def give_filter(client, message):
    k = await manual_filters(client, message)
    if k == False:
        await auto_filter(client, message)

@Client.on_message(filters.private & filters.text & filters.incoming)
async def pm_text(bot, message):
    content = message.text
    user = message.from_user.first_name
    user_id = message.from_user.id

    if content.startswith("/") or content.startswith("#"):
        return

    await message.reply_text(
        "<b>🚫 ᴘᴇʀꜱᴏɴᴀʟ ᴄʜᴀᴛ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ !</b>\n\n"
        "<blockquote>🗣️ ᴅᴇᴀʀ ᴜꜱᴇʀ, ɪ'ᴍ ɴᴏᴛ ᴀᴄᴛɪᴠᴇ ɪɴ ᴘᴍ.\n"
        "🎬 ꜱᴇᴀʀᴄʜ ᴍᴏᴠɪᴇꜱ, ᴀꜱᴋ ꜰᴏʀ ʀᴇǫᴜᴇꜱᴛꜱ, ᴇᴛᴄ., ɪɴ ᴏᴜʀ ɢʀᴏᴜᴘ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ.</blockquote>",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🍿 ʀᴇǫᴜᴇꜱᴛ / ꜱᴇᴀʀᴄʜ ʜᴇʀᴇ", url="https://t.me/+kHxHj29XTaxkYzg1")]]
        )
    )

    await bot.send_message(
        chat_id=LOG_CHANNEL,
        text=(
            f"<b>Name:</b> {user}\n"
            f"<b>ID:</b> <code>{user_id}</code>\n"
            f"<b>Message:</b>\n<blockquote>{content}</blockquote>"
        )
    )  
    

@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer("**Search for Yourself**🔎", show_alert=True)

    try:
        offset = int(offset)
    except:
        offset = 0

    search = BUTTONS.get(key)
    if not search:
        await query.answer(script.OLD_MES, show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return

    settings = await get_settings(query.message.chat.id)

    if HYPER_MODE:
        cap_lines = []
        for file in files:
            file_link = f"https://t.me/{temp.U_NAME}?start=file_{file.file_id}"
            cap_lines.append(f"📁 {get_size(file.file_size)} - [{file.file_name}]({file_link})")
        cap_text = "\n".join(cap_lines)
        btn = []
    else:
        if settings['button']:
            btn = [
                [
                    InlineKeyboardButton(
                        text=f"📂[{get_size(file.file_size)}] ➵ {file.file_name}", callback_data=f'files#{file.file_id}'
                    ),
                ]
                for file in files
            ]
        else:
            btn = [
                [
                    InlineKeyboardButton(
                        text=f"{file.file_name}", callback_data=f'files#{file.file_id}'
                    ),
                    InlineKeyboardButton(
                        text=f"{get_size(file.file_size)}", callback_data=f'files_#{file.file_id}'
                    ),
                ]
                for file in files
            ]

    if 0 < offset <= 10:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - 10

    if n_offset == 0:
        btn.append(
            [
                InlineKeyboardButton("◀️ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f"📃 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}", callback_data="pages")
            ]
        )
    elif off_set is None:
        btn.append(
            [
                InlineKeyboardButton(f"📃 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}", callback_data="pages"),
                InlineKeyboardButton("NEXT ▶️", callback_data=f"next_{req}_{key}_{n_offset}")
            ]
        )
    else:
        btn.append(
            [
                InlineKeyboardButton("◀️ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f"📃 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}", callback_data="pages"),
                InlineKeyboardButton("NEXT ▶️", callback_data=f"next_{req}_{key}_{n_offset}")
            ]
        )

    try:
        if HYPER_MODE:
            await query.edit_message_text(
                text=cap_text,
                reply_markup=InlineKeyboardMarkup(btn),
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
        else:
            await query.edit_message_reply_markup(
                reply_markup=InlineKeyboardMarkup(btn)
            )
    except MessageNotModified:
        pass

    await query.answer()

@Client.on_callback_query(filters.regex(r"^spol")) 
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("Search for Yourself🔎", show_alert=True)
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movies = SPELL_CHECK.get(query.message.reply_to_message.id)
    if not movies:
        return await query.answer(script.OLD_MES, show_alert=True)#script change
    movie = movies[(int(movie_))]
    await query.answer(script.CHK_MOV_ALRT)#script change
    k = await manual_filters(bot, query.message, text=movie)
    if k == False:
        files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
        if files:
            k = (movie, files, offset, total_results)
            await auto_filter(bot, query, k)
        else:
            k = await query.message.edit(script.MOV_NT_FND)#script change
            await asyncio.sleep(10)
            await k.delete()


async def auto_filter(client, msg, spoll=False):
    if not spoll:
        message = msg
        settings = await get_settings(message.chat.id)
        if message.text.startswith("/"): return  # ignore commands
        if re.findall(r"((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if 2 < len(message.text) < 100:
            search = message.text
            files, offset, total_results = await get_search_results(search.lower(), offset=0, filter=True)
            if not files:
                if settings["spell_check"]:
                    return await advantage_spell_chok(client, msg)
                else:
                    return
        else:
            return
    else:
        settings = await get_settings(msg.message.chat.id)
        message = msg.message.reply_to_message  # msg is CallbackQuery
        search, files, offset, total_results = spoll

    pre = 'filep' if settings['file_secure'] else 'file'

    if HYPER_MODE:
        cap_lines = []
        for file in files:
            file_link = f"https://t.me/{temp.U_NAME}?start={pre}_{file.file_id}"
            cap_lines.append(f"📁 {get_size(file.file_size)} - [{file.file_name}]({file_link})")
        cap_text = "\n".join(cap_lines)

        btn = []
        if offset != "":
            key = f"{message.chat.id}-{message.id}"
            BUTTONS[key] = search
            req = message.from_user.id if message.from_user else 0
            btn.append([
                InlineKeyboardButton(text=f"📃 1/{math.ceil(int(total_results) / 10)}", callback_data="pages"),
                InlineKeyboardButton(text="NEXT ▶️", callback_data=f"next_{req}_{key}_{offset}")
            ])
        else:
            btn.append([InlineKeyboardButton(text="📃 1/1", callback_data="pages")])
    else:
        if settings["button"]:
            btn = [
                [
                    InlineKeyboardButton(
                        text=f"📂[{get_size(file.file_size)}]--{file.file_name}", callback_data=f'{pre}#{file.file_id}'
                    ),
                ]
                for file in files
            ]
        else:
            btn = [
                [
                    InlineKeyboardButton(
                        text=f"{file.file_name}",
                        callback_data=f'{pre}#{file.file_id}',
                    ),
                    InlineKeyboardButton(
                        text=f"{get_size(file.file_size)}",
                        callback_data=f'{pre}#{file.file_id}',
                    ),
                ]
                for file in files
            ]
        if offset != "":
            key = f"{message.chat.id}-{message.id}"
            BUTTONS[key] = search
            req = message.from_user.id if message.from_user else 0
            btn.append([
                InlineKeyboardButton(text=f"📃 1/{math.ceil(int(total_results) / 10)}", callback_data="pages"),
                InlineKeyboardButton(text="NEXT ▶️", callback_data=f"next_{req}_{key}_{offset}")
            ])
        else:
            btn.append([InlineKeyboardButton(text="📃 1/1", callback_data="pages")])

    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    TEMPLATE = settings['template']
    if imdb:
        cap = TEMPLATE.format(
            query=search,
            title=imdb['title'],
            votes=imdb['votes'],
            aka=imdb["aka"],
            seasons=imdb["seasons"],
            box_office=imdb['box_office'],
            localized_title=imdb['localized_title'],
            kind=imdb['kind'],
            imdb_id=imdb["imdb_id"],
            cast=imdb["cast"],
            runtime=imdb["runtime"],
            countries=imdb["countries"],
            certificates=imdb["certificates"],
            languages=imdb["languages"],
            director=imdb["director"],
            writer=imdb["writer"],
            producer=imdb["producer"],
            composer=imdb["composer"],
            cinematographer=imdb["cinematographer"],
            music_team=imdb["music_team"],
            distributors=imdb["distributors"],
            release_date=imdb['release_date'],
            year=imdb['year'],
            genres=imdb['genres'],
            poster=imdb['poster'],
            plot=imdb['plot'],
            rating=imdb['rating'],
            url=imdb['url'],
            **locals()
        )
    else:
        mention = message.from_user.mention if message.from_user else "User"
        cap = script.RESULT_TXT.format(mention=mention, query=search)

    if imdb and imdb.get('poster'):
        try:
            delauto = await message.reply_photo(
                photo=imdb.get('poster'),
                caption=cap[:1024],
                reply_markup=InlineKeyboardMarkup(btn)
            )
            await asyncio.sleep(300)
            await delauto.delete()
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            delau = await message.reply_photo(
                photo=poster,
                caption=cap[:1024],
                reply_markup=InlineKeyboardMarkup(btn)
            )
            await asyncio.sleep(300)
            await delau.delete()
        except Exception as e:
            logger.exception(e)
            audel = await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(300)
            await audel.delete()
    else:
        if HYPER_MODE:
            autodel = await message.reply_text(
                cap_text,
                reply_markup=InlineKeyboardMarkup(btn),
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
        else:
            autodel = await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))

        await asyncio.sleep(300)
        await autodel.delete()

    if spoll:
        await msg.message.delete()

#SPELL CHECK RE EDITED BY GOUTHAMSER
async def advantage_spell_chok(client, msg):
    mv_id = msg.id
    mv_rqst = msg.text
    reqstr1 = msg.from_user.id if msg.from_user else 0
    reqstr = await client.get_users(reqstr1)
    settings = await get_settings(msg.chat.id)
    query = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)",
        "", msg.text, flags=re.IGNORECASE)  # plis contribute some common words
    query = query.strip() + " movie"
    try:
        movies = await get_poster(mv_rqst, bulk=True)
    except Exception as e:
        logger.exception(e)
        reqst_gle = mv_rqst.replace(" ", "+")
        button = [[
                 InlineKeyboardButton('ENG', 'esp'),
                 InlineKeyboardButton('MAL', 'msp'),
                 InlineKeyboardButton('HIN', 'hsp'),
                 InlineKeyboardButton('TAM', 'tsp')
        ],[
                 InlineKeyboardButton('🔍 ɢᴏᴏɢʟᴇ 🔎', url=f"https://www.google.com/search?q={reqst_gle}")
             ]]
        
        k = await msg.reply_text(
            text=script.SPOLL_NOT_FND, #IN SCRIPT CHANGE DONOT CHANGE CODE
            reply_markup=InlineKeyboardMarkup(button),
            reply_to_message_id=msg.id
        )
        await asyncio.sleep(45)
        await k.delete()      
        return
    movielist = []
    if not movies:
        reqst_gle = mv_rqst.replace(" ", "+")
        button = [[
                 InlineKeyboardButton('ENG', 'esp'),
                 InlineKeyboardButton('MAL', 'msp'),
                 InlineKeyboardButton('HIN', 'hsp'),
                 InlineKeyboardButton('TAM', 'tsp')
        ],[
                 InlineKeyboardButton('🔍 ɢᴏᴏɢʟᴇ 🔎', url=f"https://www.google.com/search?q={reqst_gle}")
             ]]
        
        k = await msg.reply_text(
            text=script.SPOLL_NOT_FND, 
            reply_markup=InlineKeyboardMarkup(button),
            reply_to_message_id=msg.id
        )
        await asyncio.sleep(60)
        await k.delete()
        return
    movielist = [movie.get('title') for movie in movies]
    SPELL_CHECK[mv_id] = movielist
    btn = [
        [
            InlineKeyboardButton(
                text=movie_name.strip(),
                callback_data=f"spol#{reqstr1}#{k}",
            )
        ]
        for k, movie_name in enumerate(movielist)
    ]
    btn.append([InlineKeyboardButton(text="✘ ᴄʟᴏsᴇ ✘", callback_data=f'spol#{reqstr1}#close_spellcheck')])
    spell_check_del = await msg.reply_text(
        text="<b>Sᴘᴇʟʟɪɴɢ Mɪꜱᴛᴀᴋᴇ Bʀᴏ ‼️\n\nᴅᴏɴ'ᴛ ᴡᴏʀʀʏ 😊 Cʜᴏᴏꜱᴇ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ ᴏɴᴇ ʙᴇʟᴏᴡ 👇</b>",
        reply_markup=InlineKeyboardMarkup(btn),
        reply_to_message_id=msg.id
    )
    await asyncio.sleep(180)
    await spell_check_del.delete()



async def manual_filters(client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await client.send_message(
                                group_id, 
                                reply_text, 
                                disable_web_page_preview=True,
                                reply_to_message_id=reply_id)
                        else:
                            button = eval(btn)
                            await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                    elif btn == "[]":
                        await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                    else:
                        button = eval(btn)
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False
