from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Запись в дневнике", callback_data="diary_menu")],
        [InlineKeyboardButton(text="Моя статистика", callback_data="stats_menu")],
        [InlineKeyboardButton(text="Аккаунт", callback_data="account_menu")],
        [InlineKeyboardButton(text="📞 Контакты", callback_data="contacts")]
    ]
)

account_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Удалить аккаунт", callback_data="delete_account_confirmation")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)

delete_account_confirmation_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить", callback_data="delete_account")],
        [InlineKeyboardButton(text="Отмена", callback_data="account_menu")],
    ]
)

report = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🏠 К отчетам", callback_data="stats_menu")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)


stats_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Письменный отчет", callback_data="written_report")],
        [InlineKeyboardButton(text="Визуализация", callback_data="visual_report")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)

home = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)

restart = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="restart")],
    ]
)

diary_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Расходы", callback_data="expenses_menu")],
        [InlineKeyboardButton(text="Доходы", callback_data="incomes_menu")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)

expenses_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Добавить запись", callback_data="add_expense")],
        [InlineKeyboardButton(text="Последняя запись", callback_data="last_expense")],
        [InlineKeyboardButton(text="К дневнику", callback_data="diary_menu")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)


incomes_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Добавить запись", callback_data="add_income")],
        [InlineKeyboardButton(text="Последняя запись", callback_data="last_expense")],
        [InlineKeyboardButton(text="К дневнику", callback_data="diary_menu")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)


text_report = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="К статистике", callback_data="stats_menu")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)


report = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="К статистике", callback_data="stats_menu")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)