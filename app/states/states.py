from aiogram.fsm.state import StatesGroup, State



class Expense(StatesGroup):
    idle_expense = State()
    category_expense = State()
    title_expense = State()
    value_expense = State()

class Income(StatesGroup):
    idle_income = State()
    category_income = State()
    title_income = State()
    value_income = State()