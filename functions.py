from aiogram import Bot, Dispatcher, executor, types
import sqlite3

connection = sqlite3.connect('data.db')
q = connection.cursor()


def toFixed(numObj, digits=0):
	return f"{numObj:.{digits}f}"

def first(chat_id):
	q.execute(f"SELECT * FROM users WHERE user_id = {chat_id}")
	result = q.fetchall()
	if len(result) == 0:
			q.execute(f"INSERT INTO users (user_id, balance)"
						f"VALUES ('{chat_id}', '0')")
			connection.commit()
