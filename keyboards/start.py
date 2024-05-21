from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)



async def start_menu_keyboard():
    registration_button = InlineKeyboardButton(
        text="Registration",
        callback_data="registration"
    )

    my_profile_button = InlineKeyboardButton(
        text="My profile",
        callback_data="my_profile"
    )

    profiles_button = InlineKeyboardButton(
        text="View Profiles",
        callback_data="view_profiles"
    )

    reference_button = InlineKeyboardButton(
        text="Reference Menu",
        callback_data="reference_menu"
    )

    history_button = InlineKeyboardButton(
        text="Liked profiles",
        callback_data="history"
    )

    wallet_button = InlineKeyboardButton(
        text="Your wallet",
        callback_data="wallet_button"
    )

    serials_button = InlineKeyboardButton(
        text="Your serials",
        callback_data="serials_button"
    )

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [registration_button],
            [profiles_button],
            [my_profile_button],
            [reference_button],
            [history_button],
            [wallet_button],
            [serials_button],
        ]
    )

    return markup