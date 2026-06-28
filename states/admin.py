from aiogram.fsm.state import StatesGroup, State

#CANCEL STATE
class AdminCancelOrder(StatesGroup):
    waiting_for_reason = State()

class AddItem(StatesGroup):
    waiting_for_name = State()
    waiting_for_price = State()
    waiting_for_photo = State()