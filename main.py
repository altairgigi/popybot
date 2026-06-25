import telebot
from config import TOKEN
from difflib import SequenceMatcher

bot = telebot.TeleBot(TOKEN)

INTENTS = {
    "greeting": ["ciao", "buongiorno", "buona sera", "buonanotte", "arrivederci"],
    "memo": ["ricordami di", "crea un promemoria", "scrivi una nota", "imposta promemoria", "sveglia"],
    "weather": ["che tempo fa", "oggi piove", "temperatura", "previsioni", "meteo"]
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

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    user_message = message.text

    user_intent = decode_intent(user_message)

    if user_intent == "greeting":
        bot.reply_to(message, "Ciao, come posso aiutarti?")

    elif user_intent == "memo":
        bot.reply_to(message, "Si, mo' me lo scrivo")

    elif user_intent == "weather":
        bot.reply_to(message, "Aspetta che guardo fuori e ti dico...")

    else:
        bot.reply_to(message, "6 7")

print("Bot listening...")
bot.infinity_polling()
