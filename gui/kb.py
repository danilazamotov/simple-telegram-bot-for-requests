from aiogram import types

keyboard_start_buttons = [
    [types.KeyboardButton(text="Режим сотрудника")],
    [types.KeyboardButton(text="Режим директора")],
    [types.KeyboardButton(text="Режим бухгалтера")]
]

keyboard_main_manager_buttons = [
    [types.KeyboardButton(text="Создать заявку")],
    [types.KeyboardButton(text="Назад")]
]

keyboard_currency_manager_buttons = [
    [types.InlineKeyboardButton(text="RUB", callback_data="currency:RUB")],
    [types.InlineKeyboardButton(text="USD", callback_data="currency:USD")],
    [types.InlineKeyboardButton(text="EUR", callback_data="currency:EUR")],
    [types.InlineKeyboardButton(text="Другая", callback_data="currency:other")]
]

keyboard_send_summary_manager_buttons = [
    [types.InlineKeyboardButton(text="Отправить", callback_data="submit_request_manager")],
    [types.InlineKeyboardButton(text="Изменить", callback_data="modify_request_manager")],
]

keyboard_purpose_of_payment_manager_buttons = [
    [types.InlineKeyboardButton(text="Расчётный счёт", callback_data="payment:bank_account")],
    [types.InlineKeyboardButton(text="Перевод на карту", callback_data="payment:card_transfer")],
    [types.InlineKeyboardButton(text="Наличные", callback_data="payment:cash")]
]

keyboard_format_purpose_of_payment_manager_buttons = [
    [types.InlineKeyboardButton(text="Расчётный счёт", callback_data="format:bank_account")],
    [types.InlineKeyboardButton(text="Перевод на карту", callback_data="format:card_transfer")],
    [types.InlineKeyboardButton(text="Наличные", callback_data="format:cash")]
]

keyboard_modify_request_manager_buttons = [
    [types.InlineKeyboardButton(text="Телефон", callback_data="edit:phone_request")],
    [types.InlineKeyboardButton(text="Дата платежа", callback_data="edit:payment_date")],
    [types.InlineKeyboardButton(text="Валюта", callback_data="edit:currency")],
    [types.InlineKeyboardButton(text="Сумма", callback_data="edit:amount")],
    [types.InlineKeyboardButton(text="Получатель платежа", callback_data="edit:payment_to_whom")],
    [types.InlineKeyboardButton(text="Назначение платежа", callback_data="edit:purpose_of_payment")],
    [types.InlineKeyboardButton(text="Форма оплаты", callback_data="edit:payment_format")],
    [types.InlineKeyboardButton(text="Срок оплаты", callback_data="edit:due_date")],
]

keyboard_request_manager_buttons = [
    [types.KeyboardButton(text="Отмена")]
]

keyboard_main_director_buttons = [
    [types.KeyboardButton(text="Статистика")],
    [types.KeyboardButton(text="Назад")]
]

keyboard_main_accounting_buttons = [
    [types.KeyboardButton(text="Статистика")],
    [types.KeyboardButton(text="Назад")]
]

