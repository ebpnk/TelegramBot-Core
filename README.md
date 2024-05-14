# Telegram Bot Setup and Usage Guide

This guide provides instructions on how to set up and run a Telegram bot using Python.

## Configuration

You need to create a configuration file to store your bot token. Create a file `cfg/core.json` with the following structure:

```
json
{
    "telegram": {
        "TOKEN": "your_token_here"
    }
}
```
Replace "your_token_here" with your actual Telegram bot token.

## Project Structure
bot_setup.py: This script initializes the bot, loads modules, and sets up the main menu.

main.py: The entry point of the bot. It starts the bot and sets up the menu handlers.

cfg/core.json: Configuration file containing the bot token.

modules/: Directory where additional bot modules are stored.


## Running the Bot
```
python main.py

```

## Ru

## Руководство по настройке и использованию бота Telegram

В этом руководстве представлены инструкции по настройке и запуску бота Telegram с использованием Python.

## Конфигурация

Вам необходимо создать файл конфигурации для хранения токена вашего бота. Создайте файл `cfg/core.json` со следующей структурой:

```
{
    "telegram": {
        "TOKEN": "your_token_here"
    }
}
```

Замените `«your_token_here»` своим фактическим токеном бота Telegram.

## Структура проекта

bot_setup.py: этот скрипт инициализирует бота, загружает модули и настраивает главное меню.

main.py: точка входа бота. Он запускает бота и настраивает обработчики меню.

cfg/core.json: файл конфигурации, содержащий токен бота.

модули/: каталог, в котором хранятся дополнительные модули бота.

Запуск бота

```
python main.py

```


## Example of creating modules

```

from telebot import types
from bot_setup import additional_menu
import logging
import threading

logging.basicConfig(level=logging.INFO)

# Словарь для управления состоянием каждого пользователя
user_sessions = {}

def setup(bot, chat_id):
    # Глобальная регистрация команды "Калькулятор"
    @bot.message_handler(func=lambda message: message.text == "Калькулятор")
    def calculator(message):
        chat_id = message.chat.id
        if chat_id not in user_sessions:
            user_sessions[chat_id] = True
            start_calculator_session(message, bot)
        else:
            bot.send_message(chat_id, "Вы уже находитесь в сессии калькулятора. Введите выражение или нажмите 'Назад'.")

def start_calculator_session(message, bot):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    back_button = types.KeyboardButton("Назад")
    markup.add(back_button)
    msg = bot.send_message(chat_id, "Введите выражение для расчёта (например, 2+2):", reply_markup=markup)
    bot.register_next_step_handler(msg, process_calculation, bot)

def process_calculation(message, bot):
    chat_id = message.chat.id
    if message.text == "Назад":
        additional_menu(message)
        del user_sessions[chat_id]  # Удаляем состояние сессии
        return

    expression = message.text
    try:
        if not set(expression).difference('0123456789+-*/.() '):
            result = eval(expression)  # Выполнение расчета
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            back_button = types.KeyboardButton("Назад")
            markup.add(back_button)
            msg = bot.send_message(chat_id, f"Результат: {result}\nВведите следующее выражение или нажмите 'Назад'.", reply_markup=markup)
            bot.register_next_step_handler(msg, process_calculation, bot)
        else:
            msg = bot.send_message(chat_id, "Ошибка: используйте только числа и знаки операций (+, -, *, /). Попробуйте снова.")
            bot.register_next_step_handler(msg, process_calculation, bot)
    except Exception as e:
        msg = bot.send_message(chat_id, f"Ошибка при вычислении: {str(e)}\nПопробуйте снова.")
        bot.register_next_step_handler(msg, process_calculation, bot)

def menu_info():
    return {
        "title": "Калькулятор",
        "command": "Калькулятор"
    }

```
