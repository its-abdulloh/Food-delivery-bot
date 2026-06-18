from aiogram.fsm.state import StatesGroup, State

#CHECKOUT STATE
class Checkout(StatesGroup):
    waiting_for_name = State()
    waiting_for_location = State()
    waiting_for_payment = State()