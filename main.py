import logging
import time
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from aiogram.types.message import ContentType
import markups as nav
from db import Database

TOKEN = "5311979121:AAEAqOiCioTdpR_OjSQQqTFWwqVur07tRuM"
YOOTOKEN = "381764678:TEST:39941"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db = Database('database.db')


# функция перевода времени в секунды
def days_to_seconds(days):
    return days * 24 * 60 * 60


# функция расчета оставшегося времени подписки
def time_sub_day(get_time):
    # получение нынешнего времени
    time_now = int(time.time())
    # получение времени между окончанием подписки и нынешним временем
    middle_time = int(get_time) - time_now

    if middle_time <= 0:
        return False
    else:
        # перевод в секунды
        dt = str(datetime.timedelta(seconds=middle_time))
        return dt


# функция проверки подписки на канал
def check_sub_channel(chat_member):
    print(chat_member['status'])
    if chat_member['status'] != 'left':
        return True
    else:
        return False


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # проверка, существует ли пользователь в БД
    if not db.user_exists(message.from_user.id):
        # добавление нового пользователя в БД
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, 'Введите имя: ')
    else:
        await bot.send_message(message.from_user.id, 'Вы уже зарегестрированы!', reply_markup=nav.mainMenu)


@dp.message_handler(commands=['sub'])
async def sub(message: types.Message):
    # проверка подписки на канал
    if check_sub_channel(await bot.get_chat_member(-1001748883099, message.from_user.id)):
        # вывод меню и сообщения о существующей подписке
        await bot.send_message(message.from_user.id, 'Вы уже подписаны!', reply_markup=nav.mainMenu)
    else:
        # вывод предложения купить подписку с инлайн-кпонкой для оплаты
        await bot.send_message(message.from_user.id, 'Покупка подписки', reply_markup=nav.sub_inline_markup)


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        # при нажатии на кнопку "Профиль"
        if message.text == 'Профиль':
            # получение имени пользователя из БД
            user_name = 'Ваше имя: ' + db.get_name(message.from_user.id)
            # получение оставшегося времени подписки из БД и перевод в дни
            user_sub = time_sub_day(db.get_time_sub(message.from_user.id))
            if not user_sub:
                user_sub = 'нет'
                # если время подписки истекло, бот отписывает пользователя от канала баном
                await bot.ban_chat_member(-1001748883099, message.from_user.id)
                # разбан пользователя для возможности осуществить повторную подписку
                await bot.unban_chat_member(-1001748883099, message.from_user.id)

            user_sub = '\nПодписка: ' + user_sub

            # вывод имени пользователя и времени до окончания подписки
            await bot.send_message(message.from_user.id, user_name + user_sub)
        elif message.text == 'Подписка':
            # проверка подписки на канал
            if check_sub_channel(await bot.get_chat_member(-1001748883099, message.from_user.id)):
                # вывод меню и сообщения о существующей подписке
                await bot.send_message(message.from_user.id, 'Вы уже подписаны!', reply_markup=nav.mainMenu)
            else:
                # вывод предложения купить подписку с инлайн-кпонкой для оплаты
                await bot.send_message(message.from_user.id, 'Покупка подписки', reply_markup=nav.sub_inline_markup)
        else:
            # setname - значение поля signup по умолчанию
            if db.get_signup(message.from_user.id) == 'setname':
                # установка нового значение в поле name из сообщения пользователя
                db.set_name(message.from_user.id, message.text)
                # автоматическая установка нового значение в поле signup
                db.set_signup(message.from_user.id, 'done')
                await bot.send_message(message.from_user.id,
                                       'Вы успешно зарегестрированы! Чтобы оформить подписку, введите /sub')
            else:
                # ответ на сообщение от пользователя вне регистрации
                await bot.send_message(message.from_user.id, '?')


# обработка запроса submonth
@dp.callback_query_handler(text='submonth')
async def submonth(call: types.CallbackQuery):
    # удаление предыдущего сообщения
    await bot.delete_message(call.from_user.id, call.message.message_id)
    # вывод данных о подписке
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
    # подтверждение оплаты
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# оплата прошла успешно
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == 'month_sub':
        # установка отсчета до окончания подписки
        time_sub = int(time.time()) + days_to_seconds(30)
        # занесение времени в БД
        db.set_time_sub(message.from_user.id, time_sub)

        # создание одноразовой ссылки на 1 один день с отсчетом от нынешнего времени
        expire_date = datetime.datetime.now() + datetime.timedelta(days=1)
        # ссылка доступна только одному пользователю
        link = await bot.create_chat_invite_link(-1001748883099, expire_date, 1)
        # вывод меню и сообщения с информацией о ссылке
        await bot.send_message(message.from_user.id,
                               f'Вам выдана подписка на месяц!\n\n'
                               f'Ссылка действительна <b>один</b> день.\n'
                               f'По ней может присоединиться только <b>один</b> пользователь.',
                               parse_mode=ParseMode.HTML,
                               reply_markup=nav.mainMenu)
        # вывод ссылки
        await bot.send_message(message.from_user.id, link.invite_link)


if __name__ == '__main__':
    # запуск бота
    executor.start_polling(dp, skip_updates=True)
