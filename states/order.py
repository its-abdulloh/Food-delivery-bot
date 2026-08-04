from aiogram.fsm.state import StatesGroup, State

class AddCart(StatesGroup):
    menu_pressed = State()
    item_selected = State()