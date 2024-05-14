import telebot
from telebot import types
import importlib
import os
import json

# Load configuration
with open('cfg/core.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
TOKEN = config['telegram']['TOKEN']

bot = telebot.TeleBot(TOKEN)

user_states = {}

def load_modules(bot, chat_id):
    modules_folder = 'modules'
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    additional_button = types.KeyboardButton("Меню бота")
    markup.add(additional_button)
    user_states[chat_id] = {}  # Инициализация состояния для пользователя
    for module_name in os.listdir(modules_folder):
        if module_name.endswith('.py') and not module_name.startswith('__'):
            module_path = f'{modules_folder}.{module_name[:-3]}'
            module = importlib.import_module(module_path)
            if hasattr(module, 'setup'):
                module.setup(bot, chat_id)
                user_states[chat_id][module_name] = module  # Сохранение модуля в состоянии пользователя
    bot.send_message(chat_id, "Основное меню:", reply_markup=markup)

def setup_main_menu_handlers():
          
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        load_modules(bot, message.chat.id)

@bot.message_handler(func=lambda message: message.text == "Меню бота")
def additional_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    back_button = types.KeyboardButton("Назад")
    markup.add(back_button)
    module_buttons = []
    for module_name in os.listdir('modules'):
        if module_name.endswith('.py') and not module_name.startswith('__'):
            module_path = f'modules.{module_name[:-3]}'
            module = importlib.import_module(module_path)
            if hasattr(module, 'menu_info'):
                info = module.menu_info()
                button = types.KeyboardButton(info['title'])
                markup.add(button)
                module_buttons.append((info['title'], module))
    
    bot.send_message(message.chat.id, "Дополнительные функции:", reply_markup=markup)

    # Регистрация обработчиков для кнопок модулей
    for title, module in module_buttons:
        @bot.message_handler(func=lambda msg: msg.text == title)
        def handle_module_command(msg, mod=module):
            mod.setup(bot, msg.chat.id)

@bot.message_handler(func=lambda message: message.text == "Назад")
def back_to_main(message):
        load_modules(bot, message.chat.id)
