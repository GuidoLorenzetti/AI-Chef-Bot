import telebot
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import time
import logging
import re
from chatbot import *

TELEGRAM_TOKEN = '6965899907:AAEXwFsBL7l5WRwzpNSlsxyQwg2qYnysO-M'

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def handle_text(message: types.Message) -> None:
    # Obtén el mensaje de texto del usuario
    user_message = message.text
    print("Mensaje:", user_message)
    bot_response = get_answer(retriever, user_message)

    # Envía la respuesta al usuario
    await message.reply(bot_response)

# Configurar el registro (log)
logging.basicConfig(level=logging.INFO)

def load_data():
    global retriever
    logging.info('Iniciando carga de modelo...')
    try:
        retriever = load_model()
        logging.info('Carga de datos exitosa.')
    except Exception as e:
        logging.error('Error al cargar modelo: %s', str(e))

data_loading_thread = threading.Thread(target=load_data)
data_loading_thread.start()

if __name__ == '__main__':
    print('Bot is running...')
    executor.start_polling(dp, skip_updates=True)
    print('Bot is stopped')