from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from const import PROFILE_TEXT
from aiogram import Router, types
from config import bot

router = Router()

class RegistrationStates(StatesGroup):
    nickname = State()
    bio = State()
    photo = State()
    birthday = State()
    gender = State()

@router.callback_query(lambda call: call.data == "registration")
async def registraion_start(call: types.CallbackQuery,
                            state: FSMContext):

    await bot.send_message(
        chat_id=call.from_user.id,
        text="Send me your Nickname,please!"
    )
    await state.send_state(RegistrationStates.nickname)
@router.message(RegistrationStates.nickname)
async def process_nickname(message: types.Message,
                           state: FSMContext):
    await state.update_data(nickname=message.text)


    await bot.send_message(
        chat_id=message.from_user.id,
        text="Tell me about yourself,please!"
    )
    data = await state.get_data()
    print(data)
    await state.set_state(RegistrationStates.bio)
@router.message(RegistrationStates.bio)
async def process_bio(message: types.Message,
                               state: FSMContext):
    await state.update_data(bio=message.text)


    await bot.send_message(
        chat_id=message.from_user.id,
        text="Send me your photo,please!"
    )
    data = await state.get_data()
    print(data)
    await state.set_state(RegistrationStates.photo)
@router.message(RegistrationStates.photo)
async def process_bio(message: types.Message,
                      state: FSMContext, data=None):
        

    file_id = message.photo[-1]
    print(message.photo)
    file = await bot.get_file(file_id)
    file_path = file.file_path
    media_final_path = 'media/' + file_path
    await bot.download_file(
        file_path,
        'media/' + file_path
    )

    await bot.send_message(
        chat_id=message.from_user.id,
        text="How old are you? "
    )
    await state.set_state(RegistrationStates.birthday)
@router.message(RegistrationStates.birthday)
async def process_birthday(message: types.Message,
                           state: FSMContext):
    await state.update_data(birthday=message.date)



    await bot.send_message(
        chat_id=message.from_user.id,
        text="Write your gender, please"
    )
    await state.set_state(RegistrationStates.gender)


@router.message(RegistrationStates.gender)
async def process_gender(message: types.Message,
                         state: FSMContext, data=None, file_path=None):
    await state.update_data(gender=message.date)


    photo = FSInputFile('media/' + file_path)
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=photo,
        caption=PROFILE_TEXT.format(
            nickname=data['nickname'],
            bio=data['bio'],
            birthday=data['birthday'],
            gender=data['gender']
        )
    )
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Congratulation, you have registered succesfully!"
    )


class UserRegistration():
    states = 'user_name'