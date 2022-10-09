from aiogram import Bot, Dispatcher, executor, types



# Клавиатура
menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(
	types.KeyboardButton('👤 Баланс'),
	types.KeyboardButton('💸 Клик'),
)

accept = types.InlineKeyboardMarkup(row_width=3)
accept.add(
    types.InlineKeyboardButton(text='✅ Принимаю', callback_data='accept')
)

apanel = types.InlineKeyboardMarkup(row_width=3)
apanel.add(
    types.InlineKeyboardButton(text='Статистика', callback_data='stats')
    )