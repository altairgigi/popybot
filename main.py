import telebot
import random
from difflib import SequenceMatcher
import greet
import memo
import config

bot = telebot.TeleBot(config.TOKEN)

INTENTS = {
    "greeting": ["ciao", "buongiorno", "buon pomeriggio", "buona sera", "buonanotte", "arrivederci"],
    "memo": ["ricordami di", "crea un promemoria", "scrivi una nota", "imposta promemoria per", "mi ricordi di"],
    "weather": ["che tempo fa", "oggi piove", "che temperatura c'è", "quali sono le previsioni", "dimmi il meteo"]
}

def calculate_similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() * 100

def decode_intent(user_message):
    best_guess = "unknown"
    best_score = 0
    threshold = 65

    for intent, examples_list in INTENTS.items():
        for example in examples_list:
            score = calculate_similarity(user_message, example)

            if score > threshold and score > best_score:
                best_score = score
                best_guess = intent

    return best_guess

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
