import sqlite3
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Вставь свой токен бота
BOT_TOKEN = "7682423816:AAFb0cCPsf123JpYvABgsNs2IfN6SMf85Xw"

bot = telebot.TeleBot(BOT_TOKEN)

# Подключение к базе данных
conn = sqlite3.connect("game.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        coins INTEGER DEFAULT 0,
        per_click INTEGER DEFAULT 1
    )
""")
conn.commit()

def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        return (user_id, 0, 1)
    return user

@bot.message_handler(commands=["start"])
def start_game(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Начать играть", web_app=WebAppInfo(url="https://scamedcoin.netlify.app/")))
    bot.send_message(message.chat.id, "Привет! Добро пожаловать в ScamBot\nТапай и Зарабатывай токен $Scam", reply_markup=keyboard)

if __name__ == "__main__":
    bot.polling(none_stop=True)
