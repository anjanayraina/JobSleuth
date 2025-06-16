# telegram_bot/bot.py
import telebot
from helper.config import ConfigSingleton

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Put in .env and load via config in prod
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Job Automation Bot!")

# Add more handlers as needed

def run_bot():
    bot.polling()

if __name__ == "__main__":
    run_bot()
