import telebot
import sqlite3
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE,
    balance REAL DEFAULT 0
)
""")
conn.commit()

def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE telegram_id=?", (user_id,))
    return cursor.fetchone()

def add_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO users (telegram_id) VALUES (?)", (user_id,))
    conn.commit()

def add_balance(user_id, amount):
    cursor.execute("UPDATE users SET balance = balance + ? WHERE telegram_id=?", (amount, user_id))
    conn.commit()

def get_balance(user_id):
    cursor.execute("SELECT balance FROM users WHERE telegram_id=?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 0

@bot.message_handler(commands=['start'])
def start(msg):
    user_id = msg.chat.id
    add_user(user_id)
    bot.send_message(user_id, "أهلاً بك 👋\nاستخدم /ads للربح")

@bot.message_handler(commands=['ads'])
def ads(msg):
    user_id = msg.chat.id
    add_user(user_id)

    bot.send_message(user_id, "شاهد الإعلان:\nhttps://example.com")

    add_balance(user_id, 1)
    balance = get_balance(user_id)

    bot.send_message(user_id, f"تم إضافة 1 نقطة ✅\nرصيدك: {balance}")

@bot.message_handler(commands=['balance'])
def balance(msg):
    user_id = msg.chat.id
    bal = get_balance(user_id)
    bot.send_message(user_id, f"رصيدك: {bal}")

bot.infinity_polling()
