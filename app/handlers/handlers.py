from app.handlers.router import router
import asyncio
import logging
import random
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram import F
from aiogram.fsm.context import FSMContext

from app.keyboards import inline as inline_keyboards

from app.states.states import Expense, Income

from app.handlers.templates import default_expenses, default_incomes

from app.requests.get_cat_error import get_cat_error_async as get_cat_error
from app.requests.login import login
from app.requests.delete_account import delete_account
from app.requests.get_categories import get_categories




#TODO запись категорий в стейт
#===========================================================================================================================
# Конфигурация основных маршрутов
#===========================================================================================================================

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    data = await login(telegram_id=message.from_user.id)
    if data is None:
        logging.error("Error while logging in")
        await message.answer("Ошибка авторизации, попробуйте позже", reply_markup=inline_keyboards.restart)
        return
    await state.update_data(telegram_id = data.get("telegram_id"))
    await message.reply("Привет! 👋")
    await message.reply("Я твой личный финансовый консультант")
    await message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)

@router.callback_query(F.data == "restart")
async def callback_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    data = await login(telegram_id=callback.from_user.id)
    if data is None:
        logging.error("Error while logging in")
        await callback.message.answer("Ошибка авторизации, попробуйте позже", reply_markup=inline_keyboards.restart)
        return
    await state.update_data(telegram_id = data.get("telegram_id"))
    await callback.message.reply("Привет! 👋")
    await callback.message.reply("Я твой личный финансовый консультант")
    await callback.message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.reply(text="Этот бот помогает вести финансовый дневник и правильно планировать свой бюджет 📚\n\nОн может выполнять несколько интересных функций, связанных с дневником личных финансов.\n\nВам также доступны аналитические функции бота. Они представлены в разделе 'Статистика'\n\nЕсли остались вопросы, пиши ему: @dianabol_metandienon_enjoyer", reply_markup=inline_keyboards.home)
@router.message(Command("contacts"))
async def cmd_contacts(message: Message):
    text = "Связь с разрабом: 📞\n\n\\@dianabol\\_metandienon\\_enjoyer 🤝\n\n[GitHub](https://github.com/Segun228)"
    await message.reply(text=text, reply_markup=inline_keyboards.home, parse_mode='MarkdownV2')

@router.callback_query(F.data == "contacts")
async def contacts_callback(callback:CallbackQuery):
    text = "Связь с разрабом: 📞\n\n\\@dianabol\\_metandienon\\_enjoyer 🤝\n\n[GitHub](https://github.com/Segun228)"
    await callback.message.edit_text(text=text, reply_markup=inline_keyboards.home, parse_mode='MarkdownV2')
    await callback.answer()

@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback:CallbackQuery):
    await callback.message.edit_text("Я много что умею 👇", reply_markup=inline_keyboards.main)
    await callback.answer()

#===========================================================================================================================
# 
#===========================================================================================================================



#===========================================================================================================================
# Взаимодействие с аккаунтом
#===========================================================================================================================
@router.callback_query(F.data == "account_menu")
async def account_menu_callback(callback:CallbackQuery):
    await callback.message.edit_text("Что вы хотите сделать с вашим аккаунтом?", reply_markup=inline_keyboards.account_menu)
    await callback.answer()

@router.callback_query(F.data == "delete_account_confirmation")
async def delete_account_confirmation_callback(callback:CallbackQuery):
    await callback.message.edit_text("Вы уверены что хотите удалить аккаунт? Восстановить записи будет невозможно...", reply_markup=inline_keyboards.delete_account_confirmation_menu)
    await callback.answer()

@router.callback_query(F.data == "delete_account")
async def delete_account_callback(callback:CallbackQuery, state:FSMContext):
    await delete_account(telegram_id=callback.from_user.id)
    await state.clear()
    await callback.message.edit_text("Аккаунт удален", reply_markup=inline_keyboards.restart)
    await callback.answer()

#===========================================================================================================================
# Дневник и записи
#===========================================================================================================================

@router.callback_query(F.data == "diary_menu")
async def diary_menu_callback(callback:CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Запишите ваши траты или доходы!", reply_markup=inline_keyboards.diary_menu)
    categories = await get_categories(telegram_id=callback.from_user.id)
    if categories is None:
        await state.update_data(expense_categories = default_expenses)
        await state.update_data(income_categories = default_incomes)
    else:
        await state.update_data(expense_categories = categories.get("expenses"))
        await state.update_data(income_categories = categories.get("incomes"))
    await callback.answer()


@router.callback_query(F.data == "expenses_menu")
async def expenses_menu_callback(callback:CallbackQuery):
    await callback.message.edit_text("Запишите ваши траты или доходы!", reply_markup=inline_keyboards.expenses_menu)
    await callback.answer()

@router.callback_query(F.data == "incomes_menu")
async def incomes_menu_callback(callback:CallbackQuery):
    await callback.message.edit_text("Запишите ваши траты или доходы!", reply_markup=inline_keyboards.incomes_menu)
    await callback.answer()

#===========================================================================================================================
# Аналитика
#===========================================================================================================================

@router.callback_query(F.data == "stats_menu")
async def stats_menu_callback(callback:CallbackQuery):
    await callback.message.edit_text("Что будем анализировать?", reply_markup=inline_keyboards.stats_menu)
    await callback.answer()


@router.callback_query(F.data == "written_report")
async def written_report_callback(callback:CallbackQuery):
    await callback.message.answer("Вот ваш отчет!")
    await callback.message.answer("Заглушка отчета", reply_markup=inline_keyboards.report)
    await callback.answer()

@router.callback_query(F.data == "visual_report")
async def visual_report_callback(callback:CallbackQuery):
    await callback.message.answer("Вот ваш отчет!")
    await callback.message.answer("Заглушка visual_report", reply_markup=inline_keyboards.report)
    await callback.answer()
#===========================================================================================================================
# Заглушка
#===========================================================================================================================

@router.message()
async def all_other_messages(message: Message):
    await message.answer("Неизвестная команда 🧐")
    photo_data = await get_cat_error()
    if photo_data:
        photo_to_send = BufferedInputFile(photo_data, filename="cat_error.jpg")
        await message.bot.send_photo(chat_id=message.chat.id, photo=photo_to_send)



