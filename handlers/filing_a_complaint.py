from aiogram import Router, F, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from bot_config import database

filing_a_complaint_router = Router()

class ComplaintFromUser(StatesGroup):
    name = State()
    instagram_account = State()
    user_complaint = State()

@filing_a_complaint_router.callback_query(F.data == "complaint")
async def start_process(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Напишите ваше имя:")
    await state.set_state(ComplaintFromUser.name)

@filing_a_complaint_router.message(ComplaintFromUser.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    if not name.isalpha():
        await message.answer("Имя должно быть написано буквами")
        return
    if len(name) < 3 or len(name) > 10:
        await message.answer("Количество символов должно быть от 3 до 10")
        return
    await state.update_data(name=name)
    await message.answer("Ваш instagram аккаунт:")
    await state.set_state(ComplaintFromUser.instagram_account)

@filing_a_complaint_router.message(ComplaintFromUser.instagram_account)
async def process_instagram_account(message: types.Message, state: FSMContext):
    instagram_account = message.text
    if len(instagram_account) >= 15:
        await message.answer("Название вашего instagram аккаунта не должно превышать 15 символов")
        return
    await state.update_data(instagram_account=instagram_account)
    await message.answer("Опишите вашу жалобу:")
    await state.set_state(ComplaintFromUser.user_complaint)

@filing_a_complaint_router.message(ComplaintFromUser.user_complaint)
async def process_user_complaint(message: types.Message, state: FSMContext):
    user_complaint = message.text
    if len(user_complaint) <= 10 or len(user_complaint) > 1000:
        await message.answer("Ваша жалоба должна быть в пределе 10-1000 символов")
        return
    await state.update_data(user_complaint=user_complaint)
    data = await state.get_data()
    print(data)
    database.save_complaints(data)
    await message.answer(f"Мы попытаемся как можно быстрее обработать вашу жалобу, {data['name']}")
    await state.clear()
