from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

btnProfile = KeyboardButton('Профиль')
btnSub = KeyboardButton('Подписка')
btnSubbed = KeyboardButton('Канал')

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btnProfile, btnSub, btnSubbed)
# mainMenu2 = ReplyKeyboardMarkup(resize_keyboard=True)
# mainMenu.add(btnSub, btnSubbed)
# mainMenu3 = ReplyKeyboardMarkup(resize_keyboard=True)
# mainMenu.add(btnSub)

sub_inline_markup = InlineKeyboardMarkup(row_width=1)
sub_channel = InlineKeyboardMarkup(row_width=1)
btnSubMonth = InlineKeyboardButton(text='150 руб./месяц', callback_data='submonth')
btnChannelURL = InlineKeyboardButton(text='Перейти в канал', url='https://t.me/+LxMA2TiWQ6U1NzAy')
sub_inline_markup.insert(btnSubMonth)
sub_channel.insert(btnChannelURL)
