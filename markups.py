from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


btnProfile = KeyboardButton('Профиль')
btnSub = KeyboardButton('Подписка')

# создание клавиатуры
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btnProfile, btnSub)

# создание инлайн-кнопок
sub_inline_markup = InlineKeyboardMarkup(row_width=1)
btnSubMonth = InlineKeyboardButton(text='150 руб./месяц', callback_data='submonth')
sub_inline_markup.insert(btnSubMonth)
