from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

async def reference_menu_keyboard():
    link_button = InlineKeyboardButton(
        text="Link",
        callback_data=f"reference_link"
    )

    # dislike_button = InlineKeyboardButton(
    #     text="Dislike",
    #     callback_data=f"dislike{tg_id}"
    # )

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [link_button],
        ]
    )

    return markup