# Telegram Bot Setup and Usage Guide

This guide provides instructions on how to set up and run a Telegram bot using Python.

## Configuration

You need to create a configuration file to store your bot token. Create a file `cfg/core.json` with the following structure:

```json
{
    "telegram": {
        "TOKEN": "your_token_here"
    }
}
````
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
