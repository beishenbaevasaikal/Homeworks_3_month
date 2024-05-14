from aiogram import Router
from aiogram import types
from config import bot
from const import PROFILE_TEXT
from database import queries
from database.db import AsyncDatabase
from keyboards.Profile import my_profile_keyboard
from aiogram.types import CallbackQuery
from keyboards.like_dislike import like_dislike_keyboard

router = Router()


@router.callback_query(lambda call: call.data == 'my_profile')
async def random_profiles_call(call: types.CallbackQuery, db: AsyncDatabase):
    profile = await db.execute_query(
        query=queries.SELECT_PROFILE_QUERY,
        params=(
            call.from_user.id,
        ),
        fetch='one'
    )
    print(profile)
    photo = types.FSInputFile(profile['photo'])
    await bot.send_photo(
        chat_id=call.from_user.id,
        photo=photo,
        caption=PROFILE_TEXT.format(
            nickname=profile['nickname'],
            bio=profile['bio'],
        ),
        reply_markup=await my_profile_keyboard()
    )