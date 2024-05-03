from database import queries
from database.db import AsyncDatabase
from aiogram import Router, types
from aiogram.filters import Command
from config import ADMIN_ID
from config import bot


router = Router()

@router.message(Command('start'))
async def start_menu(message: types.Message, db=AsyncDatabase()):
    await db.execute_query(query=queries.INSERT_USER, params=(None, message.from_user.first_name, message.from_user.id))
    await bot.send_message(
        chat_id=message.chat.id,
        text=f'Hello {message.from_user.first_name}'
    )
    print(message)

@router.message(lambda message: message.text == 'sake')
async def sake(message: types.Message, db=AsyncDatabase()):
    if message.from_user.id == int(ADMIN_ID):
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f'Hello admin {message.from_user.first_name}'
        )
        USERS = await db.execute_query(query=queries.SELECT_USER, fetch='all')
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f'{USERS}'
        )
