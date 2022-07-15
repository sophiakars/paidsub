import logging
import time
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
import markups as nav
from db import Database

TOKEN = "5311979121:AAEAqOiCioTdpR_OjSQQqTFWwqVur07tRuM"
YOOTOKEN = "381764678:TEST:39941"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db = Database('database.db')


def days_to_seconds(days):
    return days*24*60*60


def time_sub_day(get_time):
    time_now = int(time.time())
    middle_time = int(get_time) - time_now

    if middle_time <= 0:
        return False
    else:
        dt = str(datetime.timedelta(seconds=middle_time))
        return dt


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, 'Введите имя: ')
    else:
        await bot.send_message(message.from_user.id, 'Вы уже зарегестрированы!', reply_markup=nav.mainMenu)


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        if message.text == 'Профиль':
            user_name = 'Ваше имя: ' + db.get_name(message.from_user.id)
            user_sub = time_sub_day(db.get_time_sub(message.from_user.id))
            if not user_sub:
                # await bot.ban_chat_member(1001748883099, message.from_user.id)
                user_sub = 'нет'

            user_sub = '\nПодписка: ' + user_sub

            await bot.send_message(message.from_user.id, user_name + user_sub)
        elif message.text == 'Подписка':
            await bot.send_message(message.from_user.id, 'Описание', reply_markup=nav.sub_inline_markup)
        elif message.text == 'Канал':
            if db.get_sub_status(message.from_user.id):
                await bot.unban_chat_member(1001748883099, message.from_user.id)
                await bot.send_message(message.from_user.id, 'Теперь вы можете присоединиться!',
                                       reply_markup=nav.sub_channel)
            else:
                await bot.send_message(message.from_user.id, 'Купите подписку!')
        else:
            if db.get_signup(message.from_user.id) == 'setname':
                db.set_name(message.from_user.id, message.text)
                db.set_signup(message.from_user.id, 'done')
                await bot.send_message(message.from_user.id, 'Вы успешно зарегестрированы!', reply_markup=nav.mainMenu)
            else:
                await bot.send_message(message.from_user.id, '?')


@dp.callback_query_handler(text='submonth')
async def submonth(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_invoice(chat_id=call.from_user.id,
                           title="Оформление подписки",
                           description="Тестовое описание",
                           payload="month_sub",
                           provider_token=YOOTOKEN,
                           currency="RUB",
                           start_parameter="test1",
                           prices=[types.LabeledPrice(label='rub', amount=15000)])


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == 'month_sub':
        time_sub = int(time.time()) + days_to_seconds(30)
        db.set_time_sub(message.from_user.id, time_sub)
        await bot.send_message(message.from_user.id, 'Вам выдана подписка на месяц!', reply_markup=nav.sub_channel)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
