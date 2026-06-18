from aiogram.fsm.state import StatesGroup, State

#NEEDED TO WAIT FOR PHONE NUMBER
class Registration(StatesGroup):
    waiting_for_phone = State()