import binascii
import os

from aiogram import Router, types
from aiogram.types import CallbackQuery, user
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

    user = await db.execute_query(
        query=queries.SELECT_USER,
        params=(
            call.from_user.id,
        ),
        fetch='one'
    )
    print(user)
    if user['REFERENCE_LINK']:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"Your old link is {user['REFERENCE_LINK']}"
        )

    else:
        await db.execute_query(
            query=queries.UPDATE_USER_LINK_QUERY,
            params=(link,
                    call.from_user.id,
                    ),
            fetch='none'
        )

        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"Your new link is {link}"
        )

@router.callback_query(lambda call: call.data == "reference_balance")
async def view_balance(call: CallbackQuery,
                       db=AsyncDatabase()):
    user = await db.execute_query(
        query=queries.SELECT_USER,
        params=(
            call.from_user.id,
        ),
        fetch='one'
    )

    await bot.send_message(
        chat_id=call.from_user.id,
        text=f"Your balance : {user['BALANCE']}"
    )

@router.callback_query(lambda call: call.data == "view_reference_list")
async def references_list(call: CallbackQuery,
                       db=AsyncDatabase()):
    referral_list = await db.execute_query(
        query=queries.SELECT_REFERENCES_LIST,
        params=(
            call.from_user.id,
        ),
        fetch='all'
    )

    if not references_list:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="You don't have any references."
        )
    else:
        message = "Your references list:\n"
        for references in references_list:
            message += f"{references['username']} - {references['references_points']} points\n"


        await bot.send_message(
            chat_id=call.from_user.id,
            text=message
        )