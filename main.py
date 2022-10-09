import logging
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, admin
import keyboard as k
import functions as fc
import text as tx
import sqlite3

# Логи в консоль
logging.basicConfig(level=logging.INFO)

# Инициализация
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

connection = sqlite3.connect('data.db')
q = connection.cursor()


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    q.execute(f"SELECT * FROM users WHERE user_id = {message.chat.id}")
    result = q.fetchall()
    if len(result) == 0:
        q.execute(f"INSERT INTO users (user_id, balance)"
                  f"VALUES ('{message.chat.id}', '0')")
        connection.commit()
        await message.answer(tx.sogl, parse_mode='Markdown', reply_markup=k.accept)
    else:
        await message.answer(
            f'Привет, {message.from_user.mention}, кликай и зарабатывай! За каждый клик вам начисляется 50 дублеек на баланс.',
            reply_markup=k.menu)


@dp.message_handler(content_types=["text"])
async def reaction(message: types.Message):
    chat_id = message.chat.id
    fc.first(chat_id=chat_id)
    if message.text == '👤 Баланс':
        bal = q.execute(f'SELECT balance FROM users WHERE user_id = "{message.chat.id}"').fetchone()
        connection.commit()
        await message.answer(f'Ваш баланс: {fc.toFixed(bal[0], 1)}#')
    elif message.text == '💸 Клик':
        q.execute(f'UPDATE users SET balance = balance + 0.5 WHERE user_id IS "{message.chat.id}"')
        connection.commit()
    elif message.text == '/admin':
        if str(chat_id) == str(admin):
            await message.answer('Добро пожаловать в админ панель:', reply_markup=k.apanel)
        else:
            await message.answer('Черт! Ты меня взломал🙃')


@dp.callback_query_handler(lambda call: True)  # Inline часть
async def cal(call):
    chat_id = call.message.chat.id
    if call.data == 'stats':
        re = q.execute(f'SELECT * FROM users').fetchall()
        kol = len(re)
        bal = q.execute(f"SELECT sum(balance) FROM users").fetchone()
        connection.commit()
        await call.message.answer(
            f'Всего пользователей: {kol}\nОбщий баланс всех пользователей: {fc.toFixed(bal[0], 1)}#')
    elif call.data == 'back':
        await call.message.answer('Назад..', reply_markup=k.menu)
    elif call.data == 'accept':
        await call.message.answer(
            f'Привет, {call.from_user.mention}, кликай и зарабатывай! За каждый клик вам начисляется 50 дублеек на баланс.',
            reply_markup=k.menu)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True) # Запуск
