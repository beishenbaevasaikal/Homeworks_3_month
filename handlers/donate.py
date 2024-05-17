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


router = Router()

class DonateStatesGroup(StatesGroup):
    amount = State()

@router.callback_query(lambda call: "donate_" in call.data)
async def detect_donate_call(call: types.CallbackQuery,
                             state: FSMContext,
                               db=AsyncDatabase()):
    recipient_id = call.data.replace('donate_', '')
    print(recipient_id)
    donate_user = await db.execute_query(
        query=queries.SELECT_USER,
        params=(
            call.from_user.id,
        ),
        fetch='one'
    )
    print(donate_user)
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="How much do you want to donate?\n"
             f"Your balance is: {donate_user['BALANCE']}"
    )

    await state.update_data(owner_id=recipient_id)
    await state.update_data(balance_limit=donate_user['BALANCE'])
    await state.set_state(DonateStatesGroup.amount)

@router.message(DonateStatesGroup.amount)
async def process_donate_amount(message: types.Message,
                                state: FSMContext,
                                db=AsyncDatabase()):

    recipient_id = await state.get_data()
    print(recipient_id)
    data = await state.get_data()
    print(data)

    try:
        int(message.text)
        if int (message.text) < 1:
            await bot.send_message(
                chat_id=message.chat.id,
                text="Please send more!"
            )
            await state.clear()
            return
        elif int(message.text) <= data['balance_limit']:

            await db.execute_query(
                query=queries.UPDATE_SENDER_BALANCE_QUERY,
                params=(
                    int(message.text),
                    message.from_user.id,
                ),
                fetch='none'
            )

            await db.execute_query(
                query=queries.UPDATE_RECIPIENT_BALANCE_QUERY,
                params=(
                    int(message.text),
                    data['owner_id'],
                ),
                fetch='none'
            )

            await db.execute_query(
                query=queries.INSERT_DONATE_TRANSACTIONS_QUERY,
                params=(
                    None,
                    message.from_user.id,
                    data['owner_id'],
                    int(message.text),
                ),
                fetch='none'
            )

            await bot.send_message(
                chat_id=data['owner_id'],
                text="Someone sent you a donate\n"
                     f"Amount donate: {message.text}"
            )

            await bot.send_message(
                chat_id=message.from_user.id,
                text="Your donate transaction sent successfully"
            )

        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text="Not enough money"
            )

    except ValueError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Please use numeric answer"
        )
        await state.clear()
        return
