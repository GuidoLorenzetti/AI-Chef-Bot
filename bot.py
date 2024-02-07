import telebot
from telebot.types import ForceReply, ReplyKeyboardMarkup
import threading
import logging
from chatbot import *
from graph import *
from decouple import config

clasificador = pickle.load(open('clasificador.pickle', 'rb'))
vectorizer = pickle.load(open('vectorizer.pickle', 'rb'))

TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')

bot = telebot.TeleBot(TELEGRAM_TOKEN) # You can set parse_mode by default. HTML or MARKDOWN

usuarios = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_message = (
        "¡Bienvenido a LinguinIA, tu asistente culinario! 🍳👩‍🍳\n"
        "Estoy aquí para ayudarte a descubrir nuevas recetas y mejorar tus habilidades en la cocina.\n\n"
        "Puedes pedirme una receta especifíca y te ayudaré a encontrarla.\n\n"
        "O Puedes utilizar los siguientes comandos:\n"
        "/perfil - Completa tu perfil para recibir recomendaciones personalizadas.\n"
        "/hoy - Descubre la sugerencia del día para tu comida.\n"
        "/ingredientes - Proporciona una lista de ingredientes y te diré qué recetas puedes preparar.\n"
        "/tips - Obtén consejos útiles para mejorar tus habilidades culinarias.\n"
        "¡Explora las recetas, sorprende a tus seres queridos y disfruta de la magia de la cocina!"
    )
    bot.send_message(message.chat.id, welcome_message)


@bot.message_handler(commands=['perfil'])
def profile(message):
    markup = ForceReply()
    name = bot.send_message(message.chat.id,"¿Cuál es tu nombre?", reply_markup=markup)
    bot.register_next_step_handler(name, process_name_step)

def process_name_step(message):
    usuarios[message.chat.id] = {}
    usuarios[message.chat.id]['nombre'] = message.text
    chat_id = message.chat.id
    markup = ForceReply()
    age = bot.send_message(chat_id, "¿Cuál es tu edad?", reply_markup=markup)
    bot.register_next_step_handler(age, process_age_step)

def process_age_step(message):
    usuarios[message.chat.id]['edad'] = message.text.replace(" ", "")
    chat_id = message.chat.id
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Pulsa un botón", resize_keyboard=True)
    markup.add("Vegana","Vegetariana", "Cetogenica", "Sin restricciones")
    diet = bot.send_message(chat_id, "¿Sigues alguna dieta en particular?", reply_markup=markup)
    bot.register_next_step_handler(diet, process_diet_step)

def process_diet_step(message):
    chat_id = message.chat.id
    if message.text != "Vegana" and message.text != "Vegetariana" and message.text != "Cetogenica" and message.text != "Sin restricciones":
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Pulsa un botón", resize_keyboard=True)
        markup.add("Vegana","Vegetariana", "Cetogenica", "Sin restricciones")
        diet = bot.send_message(chat_id, "Por favor, selecciona una opción válida", reply_markup=markup)
        bot.register_next_step_handler(diet, process_diet_step)
    else:
        usuarios[message.chat.id]['dieta'] = message.text
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Pulsa un botón", resize_keyboard=True)
        markup.add("Celiaquia", "Sin restricciones")
        sensitivity = bot.send_message(chat_id, "¿Tienes algún tipo de sensibilidad al gluten?", reply_markup=markup)
        bot.register_next_step_handler(sensitivity, process_sensitivity_step)

def process_sensitivity_step(message):
    chat_id = message.chat.id
    if message.text != "Celiaquia" and message.text != "Sin restricciones":
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder="Pulsa un botón", resize_keyboard=True)
        markup.add("Celiaquia", "Sin restricciones")
        sensitivity = bot.send_message(chat_id, "Por favor, selecciona una opción válida", reply_markup=markup)
        bot.register_next_step_handler(sensitivity, process_sensitivity_step)
    else:
        usuarios[message.chat.id]['sensibilidad'] = message.text
        markup = ForceReply()
        diet = bot.send_message(chat_id, "¿Tienes alergias alimentarias? (Por favor añade todas las correspondientes separadas por coma, si no tienes alergias escribe Ninguna)", reply_markup=markup)
        bot.register_next_step_handler(diet, process_allergy_step)

def process_allergy_step(message):
    chat_id = message.chat.id
    allergy = message.text.replace(" ", "").split(",")
    usuarios[message.chat.id]['alergias'] = allergy
    markup = ForceReply()
    diet = bot.send_message(chat_id, "¿Cuáles son tus comidas preferidas? (Por favor añade todas las correspondientes separadas por coma)", reply_markup=markup)
    bot.register_next_step_handler(diet, process_favfood_step)

def process_favfood_step(message):
    chat_id = message.chat.id
    favfood = message.text.replace(" ", "").split(",")
    usuarios[message.chat.id]['comidas_preferidas'] = favfood
    markup = ForceReply()
    diet = bot.send_message(chat_id, "¿Cuáles son tus comidas menos preferidas? (Por favor añade todas las correspondientes separadas por coma)", reply_markup=markup)
    bot.register_next_step_handler(diet, save_profile)

def save_profile(message):
    chat_id = message.chat.id
    leastfavfood = message.text.replace(" ", "").split(",")
    usuarios[message.chat.id]['comidas_menos_preferidas'] = leastfavfood
    texto = 'Datos introducidos:\n'
    for key, value in usuarios[message.chat.id].items():
        texto += f"{key}: {value}\n"
    bot.send_message(chat_id, "¡Gracias por completar tu perfil!")
    print(usuarios[message.chat.id])
    create_graph(usuarios[message.chat.id], message.chat.id)

@bot.message_handler(commands=['hoy'])
def send_today_recipe(message):
    bot_response = get_answer(retriever, "Dame una receta aleatoria para el día de hoy")
    bot.reply_to(message, bot_response)

@bot.message_handler(commands=['ingredientes'])
def make_recipe(message):
    message_text = message.text
    # Obtener la parte del mensaje después de "/ingredientes"
    ingredientes_str = message_text[len("/ingredientes"):].strip()
    if len(ingredientes_str) == 0:
        message.reply("Por favor, ingresa los ingredientes que tienes disponibles.")
        return
    else:
        # Aquí puedes llamar a una función para procesar los ingredientes y sugerir recetas
        suggested_recipes = get_answer(retriever, "Dame una receta con los ingredientes: " + ", ".join(ingredientes_str))

    bot.reply_to(message, suggested_recipes)

@bot.message_handler(commands=['tips'])
def send_tip(message):
    bot_response = get_answer(retriever, "Dame un tip o dato curioso de cocina.")
    bot.reply_to(message, bot_response)

@bot.message_handler()
def handle_text(message) -> None:
    # Obtén el mensaje de texto del usuario
    user_message = message.text
    print("Mensaje:", user_message)
    bot_response = clas(user_message, clasificador, vectorizer, retriever)
    if isinstance(bot_response, list):
        for i in bot_response:
            bot.reply_to(message, i)
            sleep(1)
    else:
        bot.reply_to(message, bot_response)

# Configurar el registro (log)
logging.basicConfig(level=logging.INFO)

def load_data():

    global retriever
    try:
        retriever = load_model()
        logging.info('Carga de datos exitosa.')
    except Exception as e:
        logging.error('Error al cargar modelo: %s', str(e))

data_loading_thread = threading.Thread(target=load_data)
data_loading_thread.start()

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
    print('Bot is stopped')