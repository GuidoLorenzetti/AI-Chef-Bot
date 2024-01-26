import telebot
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import time
import logging
import re
from chatbot import *
from decouple import config

TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    welcome_message = (
        "¡Bienvenido a LinguinIA, tu asistente culinario! 🍳👩‍🍳\n"
        "Estoy aquí para ayudarte a descubrir nuevas recetas y mejorar tus habilidades en la cocina.\n\n"
        "Puedes pedirme una receta especifíca y te ayudaré a encontrarla.\n\n"
        "O Puedes utilizar los siguientes comandos:\n"
        "/hoy - Descubre la sugerencia del día para tu comida.\n"
        "/ingredientes - Proporciona una lista de ingredientes y te diré qué recetas puedes preparar.\n"
        "/tips - Obtén consejos útiles para mejorar tus habilidades culinarias.\n"
        "¡Explora las recetas, sorprende a tus seres queridos y disfruta de la magia de la cocina!"
    )
    await message.reply(welcome_message)

@dp.message_handler(commands=['hoy'])
async def send_today_recipe(message: types.Message):
    bot_response = get_answer(retriever, "Dame una receta aleatoria para el día de hoy")
    await message.reply(bot_response)

@dp.message_handler(commands=['ingredientes'])
async def make_recipe(message: types.Message):
    message_text = message.text
    # Obtener la parte del mensaje después de "/ingredientes"
    ingredientes_str = message_text[len("/ingredientes"):].strip()
    if len(ingredientes_str) == 0:
        await message.reply("Por favor, ingresa los ingredientes que tienes disponibles.")
        return
    else:
        # Aquí puedes llamar a una función para procesar los ingredientes y sugerir recetas
        suggested_recipes = get_answer(retriever, "Dame una receta con los ingredientes: " + ", ".join(ingredientes_str))

        await message.reply(suggested_recipes)

@dp.message_handler(commands=['tips'])
async def send_today_recipe(message: types.Message):
    bot_response = get_answer(retriever, "Dame un tip o dato curioso de cocina.")
    await message.reply(bot_response)

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