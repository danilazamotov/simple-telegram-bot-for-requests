import asyncio
import os

from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher.router import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv
from sqlalchemy.testing.plugin.plugin_base import logging

from database.DatabaseInitialize import requests_initialize_database
from database.DatabaseManager import DatabaseManager
from gui.kb import keyboard_start_buttons, keyboard_main_manager_buttons, keyboard_main_director_buttons, \
    keyboard_main_accounting_buttons, keyboard_request_manager_buttons, keyboard_currency_manager_buttons, \
    keyboard_send_summary_manager_buttons, keyboard_modify_request_manager_buttons, \
    keyboard_purpose_of_payment_manager_buttons, keyboard_format_purpose_of_payment_manager_buttons
from gui.states import RequestStates

router_manager = Router()
router_director = Router()
router_accounting = Router()

load_dotenv()
token_api = os.getenv("TELEGRAM_BOT_API_KEY")
director_id = int(os.getenv("DIRECTOR_ID"))
accounting_id = int(os.getenv("ACCOUNTING_ID"))
bot = Bot(token_api)


def generate_summary(data):
    summary = (
        f"Итоговая информация о заявке:\n"
        f"Сотрудник: {data['manager_name']} \n"
        f"Телефон: {data['phone_request']}\n"
        f"Дата платежа: {data['payment_date']}\n"
        f"Валюта: {data['currency']}\n"
        f"Сумма: {data['amount']}\n"
        f"Получатель платежа: {data['payment_to_whom']}\n"
        f"Назначение платежа: {data['purpose_of_payment']}\n"
        f"Форма оплаты: {data['payment_format']}\n"
    )
    if data['payment_format'] == 'Перевод на карту':
        summary += f"Телефон: {data['payment_phone_number']}\n" \
                   f"ФИО владельца: {data['payment_recipient_name']}\n"
    summary += f"Срок оплаты: {data['due_date']}\n"
    return summary


field_names = {
    "manager_name": "Сотрудник",
    "purpose_of_payment": "Назначение платежа",
    "payment_date": "Дата платежа",
    "due_date": "Срок оплаты",
    "payment_format": "Форма оплаты",
    "payment_phone_number": "Номер телефона",
    "payment_recipient_name": "ФИО получателя",
    "currency": "Валюта",
    "amount": "Сумма",
    "payment_to_whom": "Получатель платежа",
    "phone_request": "Телефон",
}


def get_start_keyboard() -> ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(keyboard=keyboard_start_buttons, resize_keyboard=True)


def get_keyboard_main_manager_buttons() -> ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(keyboard=keyboard_main_manager_buttons, resize_keyboard=True)


def get_keyboard_main_director_buttons() -> ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(keyboard=keyboard_main_director_buttons, resize_keyboard=True)


def get_keyboard_main_accounting_buttons() -> ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(keyboard=keyboard_main_accounting_buttons, resize_keyboard=True)


def get_keyboard_request_manager_buttons() -> ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(keyboard=keyboard_request_manager_buttons, resize_keyboard=True)


def get_inline_keyboard_currency_manager_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder(markup=keyboard_currency_manager_buttons)
    return builder.as_markup()


def get_keyboard_send_summary_manager_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder(markup=keyboard_send_summary_manager_buttons)
    return builder.as_markup()


def get_keyboard_modify_request_manager_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder(markup=keyboard_modify_request_manager_buttons)
    return builder.as_markup()


def get_keyboard_purpose_of_payment_manager_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder(markup=keyboard_purpose_of_payment_manager_buttons)
    return builder.as_markup()


def get_keyboard_format_purpose_of_payment_manager_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder(markup=keyboard_format_purpose_of_payment_manager_buttons)
    return builder.as_markup()


async def send_summary_to_director(bot_tg, director_id_tg, request_id, data):
    request_director_buttons = [
        [types.InlineKeyboardButton(text="Принять", callback_data=f"director_approve:{request_id}"),
         types.InlineKeyboardButton(text="Отклонить", callback_data=f"director_reject:{request_id}")]
    ]

    builder = InlineKeyboardBuilder(request_director_buttons)

    message_text = f"⚪️Итоговая информация о заявке id-{request_id}\n" \
                   f"Сотрудник: {data['manager_name']} \n" \
                   f"Телефон: {data['phone_request']}\n" \
                   f"Дата платежа: {data['payment_date']}\n" \
                   f"Валюта: {data['currency']}\n" \
                   f"Сумма: {data['amount']}\n" \
                   f"Получатель платежа: {data['payment_to_whom']}\n" \
                   f"Назначение платежа: {data['purpose_of_payment']}\n" \
                   f"Форма оплаты: {data['payment_format']}\n"

    if data['payment_format'] == 'Перевод на карту':
        message_text += f"Телефон: {data.get('payment_phone_number', 'Нет данных')}\n" \
                        f"ФИО владельца: {data.get('payment_recipient_name', 'Нет данных')}\n"

    message_text += f"Срок оплаты: {data['due_date']}"

    await bot_tg.send_message(director_id_tg, message_text,
                              reply_markup=builder.as_markup())


async def send_summary_to_accountant(bot_tg, accountant_id, request_id, approval):
    config = requests_initialize_database()
    db_manager = DatabaseManager(config)
    data = db_manager.get_request_data_by_id(request_id)
    if not data:
        print("Данные по заявке не найдены")
        return
    message_text = f"️Итоговая информация о заявке id-{request_id}\n" \
                   f"Сотрудник: {data['manager_name']} \n" \
                   f"Телефон: {data['phone_request']}\n" \
                   f"Дата платежа: {data['payment_date']}\n" \
                   f"Валюта: {data['currency']}\n" \
                   f"Сумма: {data['amount']}\n" \
                   f"Получатель платежа: {data['payment_to_whom']}\n" \
                   f"Назначение платежа: {data['purpose_of_payment']}\n" \
                   f"Форма оплаты: {data['payment_format']}\n"

    if data['payment_format'] == 'Перевод на карту':
        message_text += f"Телефон: {data.get('payment_phone_number', 'Нет данных')}\n" \
                        f"ФИО владельца: {data.get('payment_recipient_name', 'Нет данных')}\n"

    message_text += f"Срок оплаты: {data['due_date']}"

    if approval == 'отклонено':
        return message_text

    keyboard_request_accounting_buttons = [
        [types.InlineKeyboardButton(text="Принять", callback_data=f"accounting_approve:{request_id}"),
         types.InlineKeyboardButton(text="Отклонить", callback_data=f"accounting_reject:{request_id}")]
    ]
    builder = InlineKeyboardBuilder(keyboard_request_accounting_buttons)

    await bot_tg.send_message(accountant_id, "⚪" + message_text, reply_markup=builder.as_markup())

    return message_text


async def send_feedback_to_manager(request_id, status, str_data):
    config = requests_initialize_database()
    db_manager = DatabaseManager(config)

    data = db_manager.get_request_data_by_id(request_id)
    if not data:
        print("Данные по заявке не найдены")
        return

    manager_id = data['manager_id']
    if status == 'одобрена':
        message_text = f"Заявка id-{request_id} {status} директором. \n"
    elif status == 'отклонена':
        message_text = f"Заявка id-{request_id} {status} директором. \n"
    else:
        return

    message_text += str_data
    await bot.send_message(manager_id, message_text)


async def send_feedback_to_director(request_id, director, manager, status, data):
    if not data:
        logging(f"Данные по заявке не найдены id-{request_id}")
        return

    if status == 'принята бухгалтером':
        message_text = f"🟢 Заявка id-{request_id} {status} \n"
    elif status == 'отклонена бухгалтером':
        message_text = f"🔴 Заявка id-{request_id} {status} \n"
    else:
        return

    message_text += data
    await bot.send_message(director, message_text)
    await bot.send_message(manager, message_text)


def show_request_details(request):
    title = ""
    if not request:
        return

    if request.director_approval == 'подтверждено':
        title = f"Заявка id-{request.id} одобрена директором\n"

    summary = (
        f"Информация о заявке id-{request.id}\n"
        f"Сотрудник: {request.manager_name}\n"
        f"Телефонный номер: {request.phone_request}\n"
        f"Дата платежа: {request.payment_date}\n"
        f"Валюта: {request.currency}\n"
        f"Сумма: {request.amount}\n"
        f"Получатель платежа: {request.payment_to_whom}\n"
        f"Назначение платежа: {request.purpose_of_payment}\n"
        f"Формат оплаты: {request.payment_format}\n"
    )

    if request.payment_format == 'Перевод на карту':
        summary += (
            f"Телефон получателя: {request.payment_phone_number or 'Нет данных'}\n"
            f"ФИО владельца карты: {request.payment_recipient_name or 'Нет данных'}\n"
        )
    summary += f"Срок оплаты: {request.due_date}\n" \
               f"Дата создания: {request.date_created}\n"

    return title + summary


def get_keyboard_request_phone_manager_buttons():
    keyboard_phone_manager_buttons = [
        [types.KeyboardButton(text="Отправить номер телефона", request_contact=True)],
        [types.KeyboardButton(text="Отмена")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=keyboard_phone_manager_buttons, resize_keyboard=True)


def setup_routers(dp: Dispatcher):
    @dp.message(CommandStart())
    async def command_start_handler(message: types.Message):
        await message.answer(f"Добро пожаловать, {message.from_user.full_name}!")
        await message.answer("Выберите режим:", reply_markup=get_start_keyboard())

    @dp.message(lambda message: message.text == "Назад")
    async def accountant_mode(message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer("Выберите режим:", reply_markup=get_start_keyboard())

    @router_manager.message(lambda message: message.text == "Режим сотрудника" or message.text == "Отмена")
    async def manager_mode(message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer("Вы в режиме сотрудника.", reply_markup=get_keyboard_main_manager_buttons())

    @router_manager.message(lambda message: message.text == "Создать заявку")
    async def start_request(message: types.Message, state: FSMContext):
        await state.clear()
        await state.update_data(manager_id=message.from_user.id, manager_name=message.from_user.full_name)
        # await state.set_state(RequestStates.manager_id)
        await message.answer(
            "Для продолжения используйте кнопку ниже для отправки вашего контакта или введите номер вручную",
            reply_markup=get_keyboard_request_phone_manager_buttons())
        await state.set_state(RequestStates.phone_request)

    @router_manager.message(RequestStates.phone_request)
    async def process_phone_request(message: types.Message, state: FSMContext):
        try:
            phone_number_user = str(message.contact.phone_number)
        except:
            phone_number_user = str(message.text)
        await state.update_data(phone_request=phone_number_user)
        await message.answer("Введите дату платежа в формате дд.мм.гггг:",
                             reply_markup=get_keyboard_request_manager_buttons())
        await state.set_state(RequestStates.payment_date)

    @router_manager.message(RequestStates.payment_date)
    async def process_payment_date(message: types.Message, state: FSMContext):
        await state.update_data(payment_date=message.text)
        await message.answer("Выберите валюту (RUB, USD, EUR или другая):",
                             reply_markup=get_inline_keyboard_currency_manager_buttons())

    @router_manager.callback_query(lambda c: c.data.startswith('currency:'))
    async def process_currency_selection(query: types.CallbackQuery, state: FSMContext):
        currency = query.data.split(':')[1]
        if currency == "other":
            await query.message.edit_text("Введите валюту вручную:")
            await state.set_state(RequestStates.currency)
        else:
            await state.update_data(currency=currency)
            await query.message.edit_text(f"Выбрана валюта: {currency}", reply_markup=None)
            await query.message.answer("Введите сумму платежа (цифрами без пробелов):")
            await state.set_state(RequestStates.amount)
        await query.answer()

    @router_manager.message(RequestStates.currency)
    async def process_manual_currency_input(message: types.Message, state: FSMContext):
        await state.update_data(currency=message.text)
        await message.answer(f"Вы указали валюту: {message.text}.")
        await message.answer("Введите сумму платежа (цифрами без пробелов):")
        await state.set_state(RequestStates.amount)

    @router_manager.message(RequestStates.amount)
    async def process_amount(message: types.Message, state: FSMContext):
        await state.update_data(amount=message.text)
        await message.answer("Укажите, кому предназначен платеж (например, ООО 'Ромашка'):")
        await state.set_state(RequestStates.payment_to_whom)

    @router_manager.message(RequestStates.payment_to_whom)
    async def process_payment_to_whom(message: types.Message, state: FSMContext):
        await state.update_data(payment_to_whom=message.text)
        await message.answer("Введите назначение платежа:")
        await state.set_state(RequestStates.purpose_of_payment)

    @router_manager.message(RequestStates.purpose_of_payment)
    async def process_purpose_of_payment(message: types.Message, state: FSMContext):
        await state.update_data(purpose_of_payment=message.text)
        await message.answer("Укажите формат оплаты (например, безналичный):",
                             reply_markup=get_keyboard_purpose_of_payment_manager_buttons())
        await state.set_state(RequestStates.payment_format)

    @router_manager.callback_query(lambda c: c.data.startswith("payment:") or c.data.startswith("format:"))
    async def process_payment_type(query: types.CallbackQuery, state: FSMContext):
        action_type, payment_type = query.data.split(":")

        if action_type == 'format':
            await state.update_data(payment_format=payment_type)

        if payment_type == "card_transfer":
            await state.update_data(payment_format="Перевод на карту")
            await query.message.answer(f"Выбран формат оплаты: Перевод на карту")
            await asyncio.sleep(0.5)
            await query.message.edit_text("Введите номер телефона получателя:")
            await state.set_state(RequestStates.payment_phone_number)
        elif payment_type == "bank_account" or payment_type == "cash":
            format_text = "Расчетный счет" if payment_type == "bank_account" else "Наличные"
            await state.update_data(payment_format=format_text)
            await query.message.answer(f"Выбран формат оплаты: {format_text}")
            await query.message.answer("Введите срок оплаты в формате дд.мм.гггг:")
            await state.set_state(RequestStates.due_date)
        await query.answer()

    @router_manager.message(RequestStates.payment_phone_number)
    async def process_phone_number(message: types.Message, state: FSMContext):
        await state.update_data(payment_phone_number=message.text)
        await message.answer("Введите ФИО получателя:")

        await state.set_state(RequestStates.payment_recipient_name)

    @router_manager.message(RequestStates.payment_recipient_name)
    async def process_recipient_name(message: types.Message, state: FSMContext):
        await state.update_data(payment_recipient_name=message.text)
        await message.answer("Введите срок оплаты в формате дд.мм.гггг:")
        await state.set_state(RequestStates.due_date)

    @router_manager.message(RequestStates.due_date)
    async def process_commission_payer(message: types.Message, state: FSMContext, update_due_date=True):
        if update_due_date:
            await state.update_data(due_date=message.text)

        data = await state.get_data()
        summary = generate_summary(data)

        await message.answer(summary)
        await message.answer("Всё верно? Отправьте заявку или измените данные.",
                             reply_markup=get_keyboard_send_summary_manager_buttons())

        await state.set_state(RequestStates.summary)

    @router_manager.callback_query(lambda c: c.data == "modify_request_manager")
    async def modify_request(query: types.CallbackQuery, state: FSMContext):
        await query.message.edit_reply_markup(reply_markup=None)
        # await query.message.edit_text("Выберите поле для изменения:")
        await query.message.answer("Какое поле вы хотите изменить?",
                                   reply_markup=get_keyboard_modify_request_manager_buttons())
        await state.set_state(RequestStates.modify)

    @router_manager.callback_query(lambda c: c.data == "edit:payment_format")
    async def edit_payment_format(query: types.CallbackQuery):
        await query.message.edit_text("Выберите новую форму оплаты:",
                                      reply_markup=get_keyboard_format_purpose_of_payment_manager_buttons())

    @router_manager.callback_query(lambda c: c.data.startswith("edit:"))
    async def edit_field(query: types.CallbackQuery, state: FSMContext):
        field = query.data.split(":")[1]
        field_name = field_names.get(field,
                                     field)
        await query.message.edit_text(f"Введите новое значение для {field_name}:")
        await state.update_data(editing_field=field)
        await state.set_state(RequestStates.editing_value)

    @router_manager.message(RequestStates.editing_value)
    async def process_new_value(message: types.Message, state: FSMContext):
        data = await state.get_data()
        field_to_update = data.get('editing_field')

        if field_to_update:
            await state.update_data({field_to_update: message.text})

            await state.update_data(editing_field=None)

            await process_commission_payer(message, state, update_due_date=False)
        else:
            await message.answer("Ошибка: не найдено поле для обновления.")

    @router_manager.callback_query(lambda c: c.data == "submit_request_manager")
    async def submit_request(query: types.CallbackQuery, state: FSMContext):
        await query.message.edit_text("Заявка подтверждена вами.", reply_markup=None)
        data = await state.get_data()

        data_to_send = {key: value for key, value in data.items() if key in [
            'manager_id', 'manager_name', 'phone_request', 'payment_date', 'currency', 'amount',
            'payment_to_whom', 'purpose_of_payment', 'payment_format', 'due_date',
            'payment_recipient_name', 'payment_phone_number'
        ]}

        config = requests_initialize_database()
        db_manager = DatabaseManager(config)
        try:
            request_id = db_manager.add_request(**data_to_send)
            print(request_id)
            if request_id:
                await query.message.answer(f"Заявка отправлена директору, ей присвоено id-{request_id}",
                                           reply_markup=get_keyboard_main_manager_buttons())
                if director_id:
                    await send_summary_to_director(bot, director_id, request_id, data)
                    db_manager.update_request_approval(request_id=request_id, approval=True, role='manager')
        except Exception as e:
            await query.message.answer(f"Возникла ошибка при отправке заявки, повторите попытку или обратитесь к администратору: {e}",
                                       reply_markup=get_keyboard_main_manager_buttons())
        finally:
            await state.clear()

    @router_director.message(lambda message: message.text == "Режим директора")
    async def director_mode(message: types.Message, state: FSMContext):
        await state.clear()
        user_id = message.from_user.id
        if str(user_id) == str(director_id):
            await message.answer("Вы в режиме директора.", reply_markup=get_keyboard_main_director_buttons())
        else:
            await message.answer("У вас нет доступа к этому режиму.", reply_markup=get_start_keyboard())

    @router_director.callback_query(lambda query: query.data.startswith("director_approve:"))
    async def approve_request(query: types.CallbackQuery):
        _, request_id = query.data.split(':')
        request_id = int(request_id)
        await query.message.edit_reply_markup(reply_markup=None)
        await query.message.answer(text=f"Заявка с id-{request_id} подтверждена вами и отправлена бухгалтеру.")

        config = requests_initialize_database()
        db_manager = DatabaseManager(config)
        if db_manager.update_request_approval(request_id, 'подтверждено', role='director'):
            data = await send_summary_to_accountant(bot_tg=bot, accountant_id=accounting_id,
                                                    request_id=request_id, approval='подтверждено')
            data_final = "🟢" + data
            await query.message.answer(data_final)
            await send_feedback_to_manager(request_id, status='одобрена', str_data=data_final)
        else:
            await query.message.edit_text("Произошла ошибка при одобрении заявки.")

    @router_director.callback_query(lambda query: query.data.startswith("director_reject:"))
    async def reject_request(query: types.CallbackQuery):
        _, request_id = query.data.split(':')
        request_id = int(request_id)
        await query.message.edit_reply_markup(reply_markup=None)
        await query.message.answer(text=f"Вами отклонена заявка с id-{request_id}.")

        config = requests_initialize_database()
        db_manager = DatabaseManager(config)
        if db_manager.update_request_approval(request_id, 'отклонено', role='director'):
            data = await send_summary_to_accountant(bot_tg=bot, accountant_id=accounting_id, request_id=request_id,
                                                    approval='отклонено')
            data_final = "🔴" + data
            await query.message.answer(data_final)
            await send_feedback_to_manager(request_id, status='отклонена', str_data=data_final)
        else:
            await query.message.edit_text("Произошла ошибка при отклонении заявки.")

    @router_accounting.message(lambda message: message.text == "Режим бухгалтера")
    async def accountant_mode(message: types.Message, state: FSMContext):
        await state.clear()
        user_id = message.from_user.id
        if str(user_id) == str(accounting_id):
            await message.answer("Вы в режиме бухгалтера.", reply_markup=get_keyboard_main_accounting_buttons())
        else:
            await message.answer("У вас нет доступа к этому режиму.", reply_markup=get_start_keyboard())

    @router_accounting.callback_query(lambda query: query.data.startswith("accounting_approve:"))
    async def approve_request(query: types.CallbackQuery):
        _, request_id = query.data.split(':')

        await query.message.edit_reply_markup(reply_markup=None)
        await query.message.answer(text=f"🟢Вами одобрена заявка с id-{request_id}.")

        request_id = int(request_id)
        config = requests_initialize_database()
        db_manager = DatabaseManager(config)
        if db_manager.update_request_approval(request_id, 'подтверждено', role='accountant'):

            data = db_manager.get_request_data_by_id(request_id)
            data_str = generate_summary(data)

            await send_feedback_to_director(request_id=request_id, director=director_id,
                                            manager=int(data['manager_id']), status='принята бухгалтером',
                                            data=data_str)
            await query.message.answer("🟢" + data_str)
        else:
            await query.message.edit_text("Произошла ошибка при одобрении заявки.")

    @router_accounting.callback_query(lambda query: query.data.startswith("accounting_reject:"))
    async def reject_request(query: types.CallbackQuery):
        _, request_id = query.data.split(':')

        await query.message.edit_reply_markup(reply_markup=None)
        await query.message.answer(text=f"🔴Вами отклонена заявка с id-{request_id}.")

        request_id = int(request_id)
        config = requests_initialize_database()
        db_manager = DatabaseManager(config)
        if db_manager.update_request_approval(request_id, 'отклонено', role='accountant'):

            data = db_manager.get_request_data_by_id(request_id)
            data_str = generate_summary(data)

            await send_feedback_to_director(request_id=request_id, director=director_id,
                                            manager=int(data['manager_id']), status='отклонена бухгалтером',
                                            data=data_str)
            await query.message.answer("🔴" + data_str)
        else:
            await query.message.edit_text("Произошла ошибка при одобрении заявки.")

    @dp.message(lambda message: message.text == "Статистика")
    async def show_statistics(message: types.Message, state: FSMContext):
        await state.clear()
        config = requests_initialize_database()
        db_manager = DatabaseManager(config)
        if message.from_user.id == director_id:
            unapproved_requests = db_manager.get_unapproved_requests_first(person='director')
            if unapproved_requests:
                data_str = show_request_details(unapproved_requests)

                request_director_buttons = [
                    [types.InlineKeyboardButton(text="Принять",
                                                callback_data=f"director_approve:{unapproved_requests.id}"),
                     types.InlineKeyboardButton(text="Отклонить",
                                                callback_data=f"director_reject:{unapproved_requests.id}")]
                ]
                builder = InlineKeyboardBuilder(markup=request_director_buttons).as_markup()
                await message.answer("⚪" + data_str, reply_markup=builder)
            else:
                await message.answer("Нет непринятых заявок.")

        if message.from_user.id == accounting_id:
            unapproved_requests = db_manager.get_unapproved_requests_first(person='accountant')
            if unapproved_requests:
                data_str = show_request_details(unapproved_requests)

                request_director_buttons = [
                    [types.InlineKeyboardButton(text="Принять",
                                                callback_data=f"accounting_approve:{unapproved_requests.id}"),
                     types.InlineKeyboardButton(text="Отклонить",
                                                callback_data=f"accounting_reject:{unapproved_requests.id}")]
                ]
                builder = InlineKeyboardBuilder(markup=request_director_buttons).as_markup()
                await message.answer("⚪" + data_str, reply_markup=builder)
            else:
                await message.answer("Нет непринятых заявок.")
        else:
            await message.answer("У вас нет полномочий использовать данную функцию")

    dp.include_router(router_manager)
    dp.include_router(router_director)
    dp.include_router(router_accounting)
