from aiogram.fsm.state import StatesGroup, State

#CANCEL STATE
class AdminCancelOrder(StatesGroup):
    waiting_for_reason = State()