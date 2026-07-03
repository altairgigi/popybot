import os
import random
import telebot
from dotenv import load_dotenv
import database
import greet
import memo
import voice
import weather

load_dotenv()

TOKEN = os.environ.get("TELEGRAM_TOKEN")

bot = telebot.TeleBot(TOKEN)

database.initialise()
memo.start_memo_alert(bot)

def decode_intent(user_message):

    memo_words = ["ricord", "ricordami", "annot", "scrivi", "promemoria", "nota", "segna"]
    weather_words = ["meteo", "tempo", "pioggia", "piove", "gradi", "temperatura", "ombrello", "sole"]
    greet_words = ["ciao", "buongiorno", "buonasera", "buon pomeriggio", "salve", "buondì"]

    for word in memo_words:
        if word in user_message:
            return "memo"

    for word in weather_words:
        if word in user_message:
            return "weather"

    for word in greet_words:
        if word in user_message:
            return"greeting"
        
    return "unknown"

def process_intent(message, user_text):
    user_intent = decode_intent(user_text)

    if user_intent == "greeting":
        bot.send_message(message.chat.id, greet.greet_user())

    elif user_intent == "memo":
        bot.send_message(message.chat.id, memo.write_memo(user_text, message.chat.id))

    elif user_intent == "weather":
        bot.send_message(message.chat.id, weather.get_weather(user_text), parse_mode="HTML")

    else:
        replies_list = [
            "6 7",
            "C'hai detto?",
            "'Nche senso, scusa?"
        ]

        random_choice = random.choice(replies_list)
        bot.reply_to(message, random_choice)

@bot.message_handler(commands = ["start"])
def welcome(message):
    bot.send_message(message.chat.id, "PRONTI!")

@bot.message_handler(commands = ["help"])
def help(message):
    bot.send_message(message.chat.id, "Per adesso non so fare molto. Posso salutare, dirti il meteo o ricordarti le cose.")

@bot.message_handler(commands = ["memo"])
def memo_list(message):
    bot.send_message(message.chat.id, memo.read_memos(message.chat.id))

@bot.message_handler(commands = ["clean"])
def memo_list(message):
    bot.send_message(message.chat.id, memo.clean_memos(message.chat.id))

@bot.message_handler(content_types=['voice'])
def voice_handler(message):
    file_info = bot.get_file(message.voice.file_id)
    raw_audio = bot.download_file(file_info.file_path)

    with open("audio/voice.ogg", "wb") as file:
        file.write(raw_audio)

    transcribed_text = voice.transcribe_audio("audio/voice.ogg")

    message.text = transcribed_text
    
    if os.path.exists("audio/voice.ogg"):
        os.remove("audio/voice.ogg")

    user_text = message.text.lower()

    process_intent(message, user_text)

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    user_text = message.text.lower()

    process_intent(message, user_text)

print("Bot listening...")
bot.infinity_polling()
