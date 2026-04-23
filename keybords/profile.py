from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def profile_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
                text="Пополнить баланс", callback_data="deposit"
            )
        ]
    ]
    )


def break_action_and_back_to_main_menu(text: str = "Отменить"):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
                text=text, callback_data="cancel_deposit"
            )
        ]
    ]
    )


def apply_deposit__action_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
                text="Да", callback_data="apply_deposit"
            ),
            InlineKeyboardButton(
                text="Нет", callback_data="cancel_deposit"
            )
        ]
    ]
    )
