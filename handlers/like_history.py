import random
from idlelib import query

from aiogram import Router
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup
from aiogram.types import user
from aiogram.fsm.state import StatesGroup, State

from config import bot
from const import PROFILE_TEXT
from database import queries
from database.db import AsyncDatabase
from keyboards.Profile import my_profile_keyboard
from keyboards.like_dislike import history_keyboard

router = Router()


@router.callback_query(lambda call: call.data == "history")
async def detect_like_history_call(call: types.CallbackQuery,
                               db=AsyncDatabase()):
    profiles = await db.execute_query(
        query=queries.SELECT_LIKED_PROFILES,
        params=(
            call.from_user.id,
        ),
        fetch='all'
    )

    print(profiles)
    randomizer = random.choice(profiles)
    random_profile = await db.execute_query(
        query=queries.SELECT_PROFILE_QUERY,
        params=(
            randomizer['OWNER_TELEGRAM_ID'],
        ),
        fetch='one'
    )

    photo = types.FSInputFile(random_profile['PHOTO'])
    await bot.send_photo(
        chat_id=call.from_user.id,
        photo=photo,
        caption=PROFILE_TEXT.format(
            nickname=random_profile['NICKNAME'],
            bio=random_profile['BIO'],
            birthday=random_profile['BIRTHDAY'],
            gender=random_profile['GENDER']
        ),
        reply_markup=await history_keyboard(tg_id=random_profile['TELEGRAM_ID'])
    )


