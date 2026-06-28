import telebot
import random
import greet
import memo
import config

bot = telebot.TeleBot(config.TOKEN)

def decode_intent(user_message):
    user_text = user_message.lower()

    memo_words = ["ricorda", "ricordami", "annot", "scrivi", "promemoria", "nota"]
    weather_words = ["meteo", "tempo", "pioggia", "pioverà", "gradi", "temperatura", "ombrello", "sole"]
    greet_words = ["ciao", "buongiorno", "buonasera", "buon pomeriggio", "salve"]

    for word in memo_words:
        if word in user_text:
            return "memo"

    for word in weather_words:
        if word in user_text:
            return "weather"

    for word in greet_words:
        if word in user_text:
            return"greeting"
        
    return "unknown"

@bot.message_handler(commands = ["start"])
def welcome(message):
    bot.send_message(message.chat.id, "PRONTI!")

@bot.message_handler(commands = ["help"])
def help(message):
    bot.send_message(message.chat.id, "Per adesso non so fare molto. Posso salutare, dirti il meteo o ricordarti le cose... più o meno")

@bot.message_handler(commands = ["memolist"])
def memo_list(message):
    bot.send_message(message.chat.id, memo.read_memo())

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    user_message = message.text

    user_intent = decode_intent(user_message)

    if user_intent == "greeting":
        bot.reply_to(message, greet.greet_user())

    elif user_intent == "memo":
        bot.reply_to(message, memo.write_memo(user_message))

    elif user_intent == "weather":
        bot.reply_to(message, "Aspetta che guardo fuori e ti dico...")

    else:
        replies_list = [
            "6 7",
            "C'hai detto?",
            "'Nche senso, scusa?"
        ]

        random_choice = random.choice(replies_list)
        bot.reply_to(message, random_choice)

print("Bot listening...")
bot.infinity_polling()
