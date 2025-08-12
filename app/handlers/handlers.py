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

from aiogram.types import BufferedInputFile

from app.requests.get_cat_error import get_cat_error_async as get_cat_error
from app.requests.login import login
from app.requests.delete_account import delete_account
from app.requests.get_categories import get_categories
from app.requests.get_text_report import get_text_report
from app.requests.get_visual_report import get_visual_report
from app.requests.delete_last_expense import delete_last_expense
from app.requests.delete_last_income import delete_last_income
from app.requests.post_expense import post_expense
from app.requests.post_income import post_income
from app.requests.get_last_expense import get_last_expense
from app.requests.get_last_income import get_last_income



#===========================================================================================================================
# Конфигурация основных маршрутов
#===========================================================================================================================

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    data = await login(telegram_id=message.from_user.id)
    if data is None:
        logging.error("Error while logging in")
        await message.answer("Ошибка авторизации, попробуйте позже 😔", reply_markup=inline_keyboards.restart)
        return
    await state.update_data(telegram_id = data.get("telegram_id"))
    await message.reply("Привет! 👋")
    await message.reply("Я твой личный финансовый консультант 🧑‍💼")
    await message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)
    await set_user_info(message=message, state = state)

@router.callback_query(F.data == "restart")
async def callback_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    data = await login(telegram_id=callback.from_user.id)
    if data is None:
        logging.error("Error while logging in")
        await callback.message.answer("Ошибка авторизации, попробуйте позже 😔", reply_markup=inline_keyboards.restart)
        return
    await state.update_data(telegram_id = data.get("telegram_id"))
    await callback.message.reply("Привет! 👋")
    await callback.message.reply("Я твой личный финансовый консультант 🧑‍💼")
    await callback.message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.reply(text="Этот бот помогает вести финансовый дневник и правильно планировать свой бюджет 📚\n\nОн может выполнять несколько интересных функций, связанных с дневником личных финансов.\n\nВам также доступны аналитические функции бота. Они представлены в разделе 'Статистика' 📈\n\nЕсли остались вопросы, пиши ему: @dianabol_metandienon_enjoyer", reply_markup=inline_keyboards.home)

@router.message(Command("contacts"))
async def cmd_contacts(message: Message):
    text = "Связь с разрабом: 📞\n\n\\@dianabol\\_metandienon\\_enjoyer 🤝\n\n[GitHub](https://github.com/Segun228)"
    await message.reply(text=text, reply_markup=inline_keyboards.home, parse_mode='MarkdownV2')

@router.callback_query(F.data == "contacts")
async def contacts_callback(callback: CallbackQuery):
    await callback.answer()
    text = "Связь с разрабом: 📞\n\n\\@dianabol\\_metandienon\\_enjoyer 🤝\n\n[GitHub](https://github.com/Segun228)"
    await callback.message.edit_text(text=text, reply_markup=inline_keyboards.home, parse_mode='MarkdownV2')


@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)


#===========================================================================================================================
# Взаимодействие с аккаунтом
#===========================================================================================================================
@router.callback_query(F.data == "account_menu")
async def account_menu_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Что вы хотите сделать с вашим аккаунтом? 👤", reply_markup=inline_keyboards.account_menu)


@router.callback_query(F.data == "delete_account_confirmation")
async def delete_account_confirmation_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Вы уверены что хотите удалить аккаунт? 😳 Восстановить записи будет невозможно... 🗑️", reply_markup=inline_keyboards.delete_account_confirmation_menu)


@router.callback_query(F.data == "delete_account")
async def delete_account_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await delete_account(telegram_id=callback.from_user.id)
    await state.clear()
    await callback.message.edit_text("Аккаунт удален 😢", reply_markup=inline_keyboards.restart)


#===========================================================================================================================
# Дневник и записи
#===========================================================================================================================

@router.callback_query(F.data == "diary_menu")
async def diary_menu_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text("Запишите ваши траты или доходы! ✍️", reply_markup=inline_keyboards.diary_menu)
    categories = await get_categories(telegram_id=callback.from_user.id)
    if categories is None:
        await state.update_data(
            expense_categories=default_expenses,
            income_categories=default_incomes
        )
    else:
        await state.update_data(
            expense_categories=categories.get("expenses"),
            income_categories=categories.get("incomes")
        )



@router.callback_query(F.data == "expenses_menu")
async def expenses_menu_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    categories = await get_categories(telegram_id=callback.from_user.id)
    if categories is None:
        await state.update_data(
            expense_categories=default_expenses,
            income_categories=default_incomes
        )
    else:
        await state.update_data(
            expense_categories=categories.get("expenses"),
            income_categories=categories.get("incomes")
        )
    await callback.message.edit_text("Запишите ваши траты 🛒", reply_markup=inline_keyboards.expenses_menu)


@router.callback_query(F.data == "incomes_menu")
async def incomes_menu_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    categories = await get_categories(telegram_id=callback.from_user.id)
    if categories is None:
        await state.update_data(
            expense_categories=default_expenses,
            income_categories=default_incomes
        )
    else:
        await state.update_data(
            expense_categories=categories.get("expenses"),
            income_categories=categories.get("incomes")
        )
    await callback.message.edit_text("Запишите ваши доходы! 💸", reply_markup=inline_keyboards.incomes_menu)


#===========================================================================================================================
# Доходы
#===========================================================================================================================

@router.callback_query(F.data == "add_income")
async def choose_income_category_callback(callback:CallbackQuery, state: FSMContext):
    await callback.answer()
    income_categories = (await state.get_data()).get("income_categories", default_incomes)
    await callback.message.answer("Выберите категорию 💼", reply_markup= await inline_keyboards.get_inline_income_options(options=income_categories))


@router.callback_query(F.data.startswith("income_"))
async def add_income_category_callback(callback:CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Income.category_income)
    category_slug = callback.data.split("_")[1]
    await state.update_data(category_income = category_slug)
    await callback.message.answer("Введите название дохода 📝")



@router.message(Income.category_income)
async def add_income_title_callback(message:Message, state: FSMContext):
    user_input = message.text
    if not user_input:
        await message.reply("Пожалуйста, введите корректное название 🧐")
        return
    await state.set_state(Income.title_income)
    await state.update_data(title_income = user_input.strip())
    await message.answer("Введите сумму 💲")


@router.message(Income.title_income)
async def add_income_value_callback(message:Message, state: FSMContext):
    user_input = message.text
    if not user_input or not user_input.isdigit():
        await message.reply("Пожалуйста, введите сумму в числовом формате 🔢")
        return
    await state.set_state(Income.value_income)
    user_category = (await state.get_data()).get("category_income")
    user_title = (await state.get_data()).get("title_income")
    response = await post_income(user_category = user_category, user_value = user_input, user_title= user_title, telegram_id= message.from_user.id)
    if response:
        await message.answer("Запись успешно добавлена ✅")
        await message.answer(f"Категория: {user_category}\n\nНазвание: {user_title}\n\nСумма: {user_input}\n\n", reply_markup= inline_keyboards.incomes_menu)
        await state.clear()
    else:
        await message.answer("К сожалению не удалось создать запись, извините 😔", reply_markup= inline_keyboards.incomes_menu)
        await state.clear()



@router.callback_query(F.data == "last_income")
async def last_income_callback(callback:CallbackQuery, state: FSMContext):
    await callback.answer()
    last_income = await get_last_income(telegram_id=callback.from_user.id)
    if not last_income:
        await callback.message.answer("Извините, не удалось получить последнюю запись 😞", reply_markup=inline_keyboards.incomes_menu)
        return
    user_category = last_income.get("category")
    user_title = last_income.get("title")
    user_input = last_income.get("value")
    await callback.message.answer(f"Категория: {user_category}\n\nНазвание: {user_title}\n\nСумма: {user_input}\n\n", reply_markup= inline_keyboards.last_income_menu)



@router.callback_query(F.data == "delete_last_income")
async def delete_last_income_callback(callback:CallbackQuery, state: FSMContext):
    await callback.answer()
    result = await delete_last_income(telegram_id=callback.from_user.id)
    if result:
        await callback.message.answer("Запись успешно удалена 🗑️", reply_markup=inline_keyboards.incomes_menu)
    else:
        await callback.message.answer("Извините, не удалось удалить запись 😔", reply_markup=inline_keyboards.incomes_menu)
#===========================================================================================================================
# Расходы
#===========================================================================================================================

@router.callback_query(F.data == "add_expense")
async def choose_expense_category_callback(callback:CallbackQuery, state: FSMContext):
    await callback.answer()
    expense_categories = (await state.get_data()).get("expense_categories", default_expenses)
    await callback.message.answer("Выберите категорию 🛒", reply_markup= await inline_keyboards.get_inline_expense_options(options=expense_categories))


@router.callback_query(F.data.startswith("expense_"))
async def add_expense_category_callback(callback:CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Expense.category_expense)
    category_slug = callback.data.split("_")[1]
    await state.update_data(category_expense = category_slug)
    await callback.message.answer("Введите название расхода 📝")



@router.message(Expense.category_expense)
async def add_expense_title_callback(message:Message, state: FSMContext):
    user_input = message.text
    if not user_input:
        await message.reply("Пожалуйста, введите корректное название 🧐")
        return
    await state.set_state(Expense.title_expense)
    await state.update_data(title_expense = user_input.strip())
    await message.answer("Введите сумму 💲")


@router.message(Expense.title_expense)
async def add_expense_value_callback(message:Message, state: FSMContext):
    user_input = message.text
    if not user_input or not user_input.isdigit():
        await message.reply("Пожалуйста, введите сумму в числовом формате 🔢")
        return
    await state.set_state(Expense.value_expense)
    user_category = (await state.get_data()).get("category_expense")
    user_title = (await state.get_data()).get("title_expense")
    response = await post_expense(user_category = user_category, user_value = user_input, user_title= user_title, telegram_id= message.from_user.id)
    if response:
        await message.answer("Запись успешно добавлена ✅")
        await message.answer(f"Категория: {user_category}\n\nНазвание: {user_title}\n\nСумма: {user_input}\n\n", reply_markup= inline_keyboards.expenses_menu)
        await state.clear()
    else:
        await message.answer("К сожалению не удалось создать запись, извините 😔", reply_markup= inline_keyboards.expenses_menu)
        await state.clear()



@router.callback_query(F.data == "last_expense")
async def last_expense_callback(callback:CallbackQuery, state: FSMContext):
    await callback.answer()
    last_expense = await get_last_expense(telegram_id=callback.from_user.id)
    if not last_expense:
        await callback.message.answer("Извините, не удалось получить последнюю запись 😞", reply_markup=inline_keyboards.expenses_menu)
        return
    user_category = last_expense.get("category")
    user_title = last_expense.get("title")
    user_input = last_expense.get("value")
    await callback.message.answer(f"Категория: {user_category}\n\nНазвание: {user_title}\n\nСумма: {user_input}\n\n", reply_markup= inline_keyboards.last_expense_menu)



@router.callback_query(F.data == "delete_last_expense")
async def delete_last_expense_callback(callback:CallbackQuery, state: FSMContext):
    await callback.answer()
    result = await delete_last_expense(telegram_id=callback.from_user.id)
    if result:
        await callback.message.answer("Запись успешно удалена 🗑️", reply_markup=inline_keyboards.expenses_menu)
    else:
        await callback.message.answer("Извините, не удалось удалить запись 😔", reply_markup=inline_keyboards.expenses_menu)


#===========================================================================================================================
# Аналитика
#===========================================================================================================================

@router.callback_query(F.data == "stats_menu")
async def stats_menu_callback(callback:CallbackQuery):
    await callback.answer()
    await callback.message.answer("Что будем анализировать? 🧐", reply_markup=inline_keyboards.stats_menu)



@router.callback_query(F.data == "written_report")
async def written_report_callback(callback:CallbackQuery, state:FSMContext):
    await callback.answer()
    stats_data = await get_text_report(telegram_id=callback.from_user.id)
    if stats_data is None:
        await callback.message.answer(text="Извините, сейчас не можем создать вам статистику 😔", reply_markup=inline_keyboards.home)
        return
    total_expenses = stats_data['expenses']['total']['total_expenses']
    total_incomes = stats_data['incomes']['total']['total_incomes']
    total_profit = stats_data['profit']['total']['total_profit']
    
    total_year_expenses = stats_data['expenses']['total']['total_year_expenses']
    total_year_incomes = stats_data['incomes']['total']['total_year_incomes']
    total_year_profit = stats_data['profit']['total']['total_year_profit']
    
    total_month_expenses = stats_data['expenses']['total']['total_month_expenses']
    total_month_incomes = stats_data['incomes']['total']['total_month_incomes']
    total_month_profit = stats_data['profit']['total']['total_month_profit']
    
    max_month_expense = stats_data['expenses']['max_month_expense']
    max_year_expense = stats_data['expenses']['max_year_expense']
    max_expense = stats_data['expenses']['max_expense']
    ballance = stats_data['expenses']['ballance']
    message_text = (
        "📊 **Ваша финансовая аналитика:**\n\n"
        "**Показатели:**\n"
        f"💰 Балланс: `{ballance}`\n"
        f"💸 Максимальная месячная трата: `{max_month_expense}`\n"
        f"📈 Максимальная годовая трата: `{max_year_expense}`\n"
        f"📈 Максимальная трата: `{max_expense}`\n\n"
        "**Итог за последний месяц:**\n"
        f"💰 Доходы: `{total_month_incomes}`\n"
        f"💸 Расходы: `{total_month_expenses}`\n"
        f"📈 Прибыль: `{total_month_profit}`\n"
        "\n**Итог за последний год:**\n"
        f"💰 Доходы: `{total_year_incomes}`\n"
        f"💸 Расходы: `{total_year_expenses}`\n"
        f"📈 Прибыль: `{total_year_profit}`\n\n"
        "**Общий итог за всё время:**\n"
        f"💰 Доходы: `{total_incomes}`\n"
        f"💸 Расходы: `{total_expenses}`\n"
        f"📈 Прибыль: `{total_profit}`\n\n"
    )

    await callback.message.answer(message_text, reply_markup=inline_keyboards.text_report, parse_mode="MarkdownV2")

    all_expenses = stats_data['expenses']['records']['all_expenses_records']
    year_expenses = stats_data['expenses']['records']['last_year_expenses_records']
    month_expenses = stats_data['expenses']['records']['last_month_expenses_records']
    
    all_incomes = stats_data['incomes']['records']['all_income_records']
    year_incomes = stats_data['incomes']['records']['last_year_income_records']
    month_incomes = stats_data['incomes']['records']['last_month_income_records']
    await state.update_data(all_expenses = all_expenses)
    await state.update_data(year_expenses = year_expenses)
    await state.update_data(month_expenses = month_expenses)
    await state.update_data(all_incomes = all_incomes)
    await state.update_data(year_incomes = year_incomes)
    await state.update_data(month_incomes = month_incomes)


@router.callback_query(F.data == "visual_report")
async def visual_report_callback(callback: CallbackQuery):
    await callback.answer()
    image_bytes_list = await get_visual_report(telegram_id=callback.from_user.id)

    if not image_bytes_list:
        logging.error("Failed to get visual report images from API.")
        await callback.message.answer(
            "К сожалению, не удалось сгенерировать отчёт. Возможно, недостаточно данных 😔",
            reply_markup=inline_keyboards.report)
        await callback.answer()
        return
    
    first_photo = BufferedInputFile(image_bytes_list[0], filename="report_1.png")
    caption_text = "📊 Вот ваш визуальный отчёт о финансах! 📈"
    await callback.message.answer_photo(
        photo=first_photo,
        caption=caption_text
    )

    for ind, photo_bytes in enumerate(image_bytes_list[1:], start=2):
        if photo_bytes is None:
            continue
            
        photo_file = BufferedInputFile(photo_bytes, filename=f"report_{ind}.png")
        await callback.message.answer_photo(
            photo=photo_file
        )
    await callback.message.answer("Готово! 🎉", reply_markup=inline_keyboards.report)

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

async def set_user_info(message:Message, state:FSMContext):
    stats_data = await get_text_report(telegram_id=message.from_user.id)
    if stats_data is None:
        return

    all_expenses = stats_data['expenses']['records']['all_expenses_records']
    year_expenses = stats_data['expenses']['records']['last_year_expenses_records']
    month_expenses = stats_data['expenses']['records']['last_month_expenses_records']
    
    all_incomes = stats_data['incomes']['records']['all_income_records']
    year_incomes = stats_data['incomes']['records']['last_year_income_records']
    month_incomes = stats_data['incomes']['records']['last_month_income_records']
    await state.update_data(all_expenses = all_expenses)
    await state.update_data(year_expenses = year_expenses)
    await state.update_data(month_expenses = month_expenses)
    await state.update_data(all_incomes = all_incomes)
    await state.update_data(year_incomes = year_incomes)
    await state.update_data(month_incomes = month_incomes)