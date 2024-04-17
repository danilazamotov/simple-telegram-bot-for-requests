from aiogram.fsm.state import StatesGroup, State


class RequestStates(StatesGroup):
    payment_recipient_name = State()
    payment_phone_number = State()
    editing_value = State()
    modify = State()
    manager_id = State()
    manager_name = State()
    phone_request = State()
    payment_date = State()
    currency = State()
    amount = State()
    payment_to_whom = State()
    purpose_of_payment = State()
    payment_format = State()
    due_date = State()
    summary = State()
    unapproved_requests = State()


class Mode(StatesGroup):
    manager_state = State()
    director_state = State()
    accounting_state = State()
