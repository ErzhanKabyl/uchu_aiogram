from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from keybords.profile import profile_menu_kb, break_action_and_back_to_main_menu, apply_deposit__action_kb
from repositories.user import UserRepo
from states.profile import UserDepositState

profile_router = Router()

@profile_router.message(F.text == "Профиль")
async def user_profile_info(
        message: Message,
        user_repo: UserRepo,
        state: FSMContext,
        ):
    user = await user_repo.get_user_by_tg_id(message.from_user.id)


    await message.answer(
        f"<b>{message.from_user.full_name}</b>\n\n"
        f"Username: {user.username or 'Пусто'}\n"
        f"ID: <code>{user.tg_id}</code>\n"
        f"Ваш баланс : {user.view_balance} тг.",
        parse_mode=ParseMode.HTML,
        reply_markup=profile_menu_kb()
    )

@profile_router.callback_query(F.data == 'deposit')
async def user_deposit_action(
        callback_query: CallbackQuery,
        state: FSMContext,
):
    await callback_query.message.edit_text("Введите сумму пополнения: ",
                                           reply_markup=break_action_and_back_to_main_menu())
    await state.set_state(UserDepositState.INPUT_AMOUNT)


@profile_router.callback_query(StateFilter(UserDepositState), F.data == 'cancel_deposit')
async def user_deposit_action_cancel(
        callback_query: CallbackQuery,
        state: FSMContext,
        user_repo: UserRepo,
):
    await state.clear()
    await callback_query.answer()

    user = await user_repo.get_user_by_tg_id(callback_query.from_user.id)

    await callback_query.message.edit_text(
        f"<b>{callback_query.from_user.full_name}</b>\n\n"
        f"Username: {user.username or 'Пусто'}\n"
        f"ID: <code>{user.tg_id}</code>\n"
        f"Ваш баланс : {user.view_balance} тг.",
        parse_mode=ParseMode.HTML,
        reply_markup=profile_menu_kb()
    )

@profile_router.message(UserDepositState.INPUT_AMOUNT)
async def user_deposit_amount(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите целое число")
        return
    amount = int(message.text)

    await state.set_data({"amount": amount})
    await message.answer(
        f"Подтвердите пополнение баланса на {amount} тг.",
        reply_markup=apply_deposit__action_kb()
    )
    await state.set_state(UserDepositState.APPLY_DEPOSIT)

@profile_router.callback_query(UserDepositState.APPLY_DEPOSIT)
async def apply_user_deposit(
        callback_query: CallbackQuery,
        state: FSMContext,
        user_repo: UserRepo
):
    state_data = await state.get_data()
    deposit_amount = state_data.get("amount")

    await user_repo.update_balance(
        callback_query.from_user.id,
        deposit_amount*100
    )
    await callback_query.message.edit_text(
        f"Ваш баланс успешно пополнен на {deposit_amount} тг.",
        reply_markup=break_action_and_back_to_main_menu("Назад в профиль"
        )
    )

    await callback_query.answer()
