import telebot
import info
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = '6748439128:AAFQ_Y3jQ-pv0Ncx2vZA3Avcva5MebCS-Mk'
bot = telebot.TeleBot(API_TOKEN)
level = 0


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("/help")
    keyboard.add("/game")
    bot.send_message(message.chat.id, info.start_text, reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("/start")
    keyboard.add("/help")
    keyboard.add("/game")
    bot.send_message(message.chat.id, info.help_text, reply_markup=keyboard)


def save_progress(user_id, level):
    cur_progress = {str(user_id): level}
    try:
        with open('progress.json', 'r') as file:
            progress = json.load(file)
        progress[str(user_id)] = level
        with open('progress.json', 'w') as file:
            json.dump(progress, file)
    except:
        with open('progress.json', 'w') as file:
            json.dump(cur_progress, file)


def load_progress(user_id):
    global level
    try:
        with open('progress.json', 'r') as file:
            level = json.load(file)
            return level.get(str(user_id))
    except FileNotFoundError:
        return None


@bot.message_handler(commands=['restart'])
def restart(message):
    global level
    level = 1
    level1(message)


@bot.message_handler(commands=['game'])
def level1(message):
    global user_id
    user_id = message.from_user.id
    with open("locations.json", "r", encoding="UTF-8") as read_file:
        data = json.load(read_file)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for option in data['location0']['options']:
        keyboard.add(option)
    bot.send_photo(message.chat.id, info.location0, caption=data["location0"]["description"], reply_markup=keyboard)
    bot.register_next_step_handler(message, level2)


@bot.message_handler(content_types=['text'])
def level2(message):
    global user_id
    global level
    level += 1
    save_progress(user_id, level)
    if message.text == "Останусь в вольере":
        with open("locations.json", "r", encoding="UTF-8") as read_file:
            data = json.load(read_file)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("/restart")
        bot.send_photo(message.chat.id, info.location1, caption=data["location1"]["description"], reply_markup=keyboard)
    elif message.text == "Уйду один(-а)":
        with open("locations.json", "r", encoding="UTF-8") as read_file:
            data = json.load(read_file)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("/restart")
        bot.send_photo(message.chat.id, info.location2, caption=data["location2"]["description"], reply_markup=keyboard)
    elif message.text == "Подойду к другой капибаре":
        with open("locations.json", "r", encoding="UTF-8") as read_file:
            data = json.load(read_file)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        for option in data['location3']['options']:
            keyboard.add(option)
        bot.send_photo(message.chat.id, info.location3, caption=data["location3"]["description"], reply_markup=keyboard)
        bot.register_next_step_handler(message, level3)
    elif message.text == "Пойду к реке":
        with open("locations.json", "r", encoding="UTF-8") as read_file:
            data = json.load(read_file)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('/restart')
        bot.send_photo(message.chat.id, info.location4, caption=data["location4"]["description"], reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def level3(message):
    global user_id
    global level
    level += 1
    if message.text == ("Убегу"):
        with open("locations.json", "r", encoding="UTF-8") as read_file:
            data = json.load(read_file)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("/restart")
        bot.send_photo(message.chat.id, info.location5, caption=data["location5"]["description"], reply_markup=keyboard)
    elif message.text == ("Вступлю в бой"):
        with open("locations.json", "r", encoding="UTF-8") as read_file:
            data = json.load(read_file)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("/restart")
        bot.send_photo(message.chat.id, info.location6, caption=data["location6"]["description"], reply_markup=keyboard)


bot.polling()
