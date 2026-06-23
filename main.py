import telebot
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start'])
def welcome(message):
    bot.reply_to(message, "Pronti!")

@bot.message_handler(commands = ['help'])
def help(message):
    bot.reply_to(message, "6 7")

bot.infinity_polling()
