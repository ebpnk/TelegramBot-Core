from bot_setup import bot, setup_main_menu_handlers

if __name__ == '__main__':
    setup_main_menu_handlers()
    bot.polling()