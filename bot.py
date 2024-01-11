import telebot
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import time
import logging
import re
from chatbot import *

TELEGRAM_TOKEN = '6813772856:AAF2Xkq-mDlgh82KX2Q-lJPT11xJtdJ4mE4'

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    welcome_message = (
        "¡Bienvenido a LinguinIA, tu asistente culinario! 🍳👩‍🍳\n"
        "Estoy aquí para ayudarte a descubrir nuevas recetas y mejorar tus habilidades en la cocina.\n\n"
        "Puedes utilizar los siguientes comandos:\n"
        "/hoy - Descubre la sugerencia del día para tu comida.\n"
        "/ingredientes - Proporciona una lista de ingredientes y te diré qué recetas puedes preparar.\n"
        "/tips - Obtén consejos útiles para mejorar tus habilidades culinarias.\n"
        "O puedes pedirme una receta especifíca y te ayudaré a encontrarla.\n\n"
        "¡Explora las recetas, sorprende a tus seres queridos y disfruta de la magia de la cocina!"
    )
    await message.reply(welcome_message)

@dp.message_handler(commands=['hoy'])
async def send_today_recipe(message: types.Message):
    bot_response = get_answer(retriever, "Dame una receta aleatoria para el día de hoy")
    await message.reply(bot_response)

@dp.message_handler(commands=['ingredientes'])
async def make_recipe(message: types.Message):
    reply_message = (
        "¡Perfecto! Añade los ingredientes que tienes en tu cocina y te diré qué recetas puedes preparar.\n"
        "Por favor, envía los ingredientes separados por comas."
    )
    await message.reply(reply_message)

    user_input = await dp.wait_for(types.Message, timeout=60)  # Espera la respuesta durante 60 segundos
    ingredients = user_input.text.split(',')

    # Aquí puedes llamar a una función para procesar los ingredientes y sugerir recetas
    suggested_recipes = get_answer(retriever, "Dame una receta con los ingredientes: " + ", ".join(ingredients))
    reply_message = f"Aquí tienes algunas recetas que puedes preparar con los ingredientes que tienes:\n\n"
    reply_message += "\n".join(suggested_recipes)

    await message.reply(reply_message)

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