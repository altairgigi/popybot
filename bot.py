import os
import random
import telebot
import speech_recognition
from dotenv import load_dotenv
from src import greet, memo, voice, weather, engine
import config

load_dotenv()

TOKEN = os.environ.get("TELEGRAM_TOKEN")

bot = telebot.TeleBot(TOKEN)

def process_message(message, user_text):
    user_intent = engine.decode_intent(user_text)

    if user_intent is not None:
        entities = engine.extract_entities(user_text, user_intent)

        if user_intent == config.INTENTS['greet']:
            bot.send_message(message.chat.id, greet.greet_user())

        elif user_intent == config.INTENTS['memo']:
            title = entities['action']
            time = entities['time']
            date = entities['date']
            bot.send_message(message.chat.id, memo.write_memo(message.chat.id, title, time, date))

        elif user_intent == config.INTENTS['weather']:
            location = entities['location']
            when = entities['date']
            bot.send_message(message.chat.id, weather.get_weather(location, when), parse_mode="HTML")
    else:
        replies_list = config.RESPONSES['unknown_replies']
        random_choice = random.choice(replies_list)
        bot.reply_to(message, random_choice)


@bot.message_handler(commands = ['start'])
def welcome(message):
    bot.send_message(message.chat.id, config.RESPONSES['start'])

@bot.message_handler(commands = ['help'])
def help(message):
    bot.send_message(message.chat.id, config.RESPONSES['help'])

@bot.message_handler(commands = ['memo'])
def memo_list(message):
    bot.send_message(message.chat.id, memo.read_memos(message.chat.id))

@bot.message_handler(commands = ['clean'])
def memo_list(message):
    bot.send_message(message.chat.id, memo.clean_memos(message.chat.id))

@bot.message_handler(content_types=['voice'])
def voice_handler(message):
    file_info = bot.get_file(message.voice.file_id)
    raw_audio = bot.download_file(file_info.file_path)

    with open(config.AUDIO_PATH['ogg_path'], "wb") as file:
        file.write(raw_audio)

    try:
        transcribed_text = voice.transcribe_audio(config.AUDIO_PATH['ogg_path'])

        user_text = transcribed_text.lower()    

        process_message(message, user_text)
    except speech_recognition.UnknownValueError:
        bot.send_message(message.chat.id, config.RESPONSES['voice_issue'])
    
    except speech_recognition.RequestError:
        bot.send_message(message.chat.id, config.RESPONSES['voice_connection_issue'])

    finally:   
        if os.path.exists(config.AUDIO_PATH['ogg_path']):
            os.remove(config.AUDIO_PATH['ogg_path'])
        if os.path.exists(config.AUDIO_PATH['wav_path']):
            os.remove(config.AUDIO_PATH['wav_path'])

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    user_text = message.text.lower()

    process_message(message, user_text)
