import sqlite3

from aiogram.utils.deep_linking import create_start_link

from const import START_MENU_TEXT
from database import queries
from database.db import AsyncDatabase
from aiogram import Router, types
from aiogram.filters import Command
from config import ADMIN_ID, MEDIA_PATH
from config import bot
from keyboards.start import start_menu_keyboard
from scraper.news_scraper import SerialScraper

router = Router()

@router.message(Command('start'))
async def start_menu(message: types.Message, db=AsyncDatabase()):

    command = message.text
    token = command.split()
    print(token)
    if len(token) > 1:
        await process_reference_link(token[1],
                                     message)

    await db.execute_query(query=queries.INSERT_USER, params=(None, message.from_user.first_name, message.from_user.id, None, 0))
    await bot.send_message(
        chat_id=message.chat.id,
        text=f'Hello {message.from_user.first_name}'
    )


    animation_file = types.FSInputFile(MEDIA_PATH + "RK67baKq9A79.gif")
    await bot.send_animation(
        chat_id=message.from_user.id,
        animation=animation_file,
        caption=START_MENU_TEXT.format(
            user=message.from_user.first_name
        ),
        reply_markup=await start_menu_keyboard()
    )

async def process_reference_link(token, message, db=AsyncDatabase()):
    link = await create_start_link(bot=bot, payload=token)
    owner = await db.execute_query(
        query=queries.SELECT_USEER_BY_LINK_QUERY,
        params=(
            link,
        ),
        fetch='one'
    )

    if owner['tg_id'] == message.from_user.id:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="You can't use this link"
        )
        return

    try:
        await db.execute_query(
            query=queries.INSERT_REFERENCE_USER_QUERY,
            params=(
                None,
                owner['tg_id'],
                message.from_user.id
            ),
            fetch='none'
        )

        await db.execute_query(
                query=queries.UPDATE_USER_BALANCE_QUERY,
                params=(
                    owner['tg_id'],
                ),
                fetch='none'
            )

        await bot.send_message(
            chat_id=owner['tg_id'],
            text="You have new reference user\n"
                 "Congratulations!"
        )
    except sqlite3.IntegrityError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="You have used this link"
        )

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

    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="You haven't access!!!"
        )

@router.callback_query(lambda call: call.data == "serials")
async def latest_serial_links(call: types.CallbackQuery,
                               db=AsyncDatabase()):
    scraper = SerialScraper()
    data = scraper.scrape_data()
    for serial in data:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text="https://serial-time.net/top/" + serial
        )
