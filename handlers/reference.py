import binascii
import os

from aiogram import Router, types
from aiogram.utils.deep_linking import create_start_link

from config import bot
from database import queries
from database.db import AsyncDatabase
from keyboards.reference import reference_menu_keyboard

router = Router()

@router.callback_query(lambda call: call.data == "reference_menu")
async def reference_menu(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Hi this is Reference menu\n"
             "You can create Reference Link, share with your friends\n"
             "We will send to your account wallet 100 points",
        reply_markup = await reference_menu_keyboard()
    )

@router.callback_query(lambda call: call.data == "reference_link")
async def reference_link_creation(call: types.CallbackQuery,
                                  db=AsyncDatabase()):
    token = binascii.hexlify(os.urandom(8)).decode()
    print(token)
    link = await create_start_link(bot=bot, payload="token")
    print(link)

    await db.execute_query(
        query=queries.UPDATE_USER_LINK_QUERY,
        params=(link,
                call.from_user.id,
                ),
        fetch='none'
    )
