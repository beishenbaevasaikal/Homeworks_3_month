import random

from aiogram import Router, types

from config import bot
from const import PROFILE_TEXT
from database import queries
from database.db import AsyncDatabase
from keyboards.like_dislike import like_dislike_keyboard

router = Router()

@router.callback_query(lambda call: call.data == 'view_profiles')
async def random_profiles_call(call: types.CallbackQuery,
                               db=AsyncDatabase()):
    if call.message.caption.startswith('Nickname'):
        await call.message.delete()
    profiles = await db.execute_query(
        query=queries.SELECT_PROFILE_TABLE_QUERY,
        params=(
            call.from_user.id,
            call.from_user.id,
        ),
        fetch='all'
    )
    if profiles:
        random_profile = random.choice(profiles)
        print(profiles)
        print(random_profile)
        photo = types.FSInputFile(random_profile['photo'])
        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=photo,
            caption=PROFILE_TEXT.format(
                nickname=random_profile['nickname'],
                bio=random_profile['bio'],
            ),
            reply_markup=await like_dislike_keyboard(tg_id=random_profile['TELEGRAM_ID'])
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text='You have liked all profiles, come later!'
        )
@router.callback_query(lambda call: 'like_' in call.data)
async def like_detect_call(call: types.CallbackQuery,
                           db=AsyncDatabase()):
    print(call.data.replace('like_', ''))

    await db.execute_query(
        query=queries.INSERT_LIKE_QUERY,
        params=(
            None,
            call.from_user.id,
            1
        ),
        fetch='none'
    )
    await random_profiles_call(call=call)



    @router.callback_query(lambda call: 'dislike' in call.data)
    async def dislike_detect_call(call: types.CallbackQuery,
                               db=AsyncDatabase()):
        print(call.data.replace('dislike', ''))

        await db.execute_query(
            query=queries.INSERT_DISLIKE_QUERY,
            params=(
                None,
                call.from_user.id,
                0
            ),
            fetch='none'
        )
        await random_profiles_call(call=call)