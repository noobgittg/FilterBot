from pyrogram import filters, Client
from pyrogram.types import Message
from utils import JOIN_REQUEST_USERS
from info import ADMINS
from pyrogram import Client
from pyrogram.types import ChatJoinRequest
from database.users_chats_db import db

@Client.on_chat_join_request()
async def join_request_handler(client, update: ChatJoinRequest):
    user_id = update.from_user.id
    chat_id = update.chat.id

    auth_channels = await db.get_auth_channels()
    if chat_id in auth_channels:
        if user_id not in JOIN_REQUEST_USERS:
            JOIN_REQUEST_USERS[user_id] = set()
        JOIN_REQUEST_USERS[user_id].add(chat_id)

@Client.on_message(filters.command("clear_join_users") & filters.user(ADMINS))
async def clear_join_users(_, message: Message):
    JOIN_REQUEST_USERS.clear()
    await message.reply_text("✅ Cleared all join request users.")
