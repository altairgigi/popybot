import time
import threading
import shlex
from datetime import datetime
from src import database
import config

def set_routine(message):
    try:   
        args = shlex.split(message.text)
    except ValueError:
        return config.RESPONSES['routine_error']

    if len(args) == 3:
        try:
            datetime.strptime(args[2], "%H:%M")
        except ValueError:
            return config.RESPONSES['routine_error']

        title = args[1]

        database.add_routine(message.chat.id, title, args[2])
        return config.RESPONSES['routine_set']
    else:
        return config.RESPONSES['routine_error']

def check_routine(bot):
    while True:
        wait_time = 60 - datetime.now().second
        time.sleep(wait_time)

        time_now = datetime.now().strftime("%H:%M")

        routines = database.get_routines(time_now)

        if len(routines) >= 1:
            for chat_id, title in routines:
                routine = config.TEMPLATES['memo_alert'].format(memo=title)

                bot.send_message(chat_id, routine, parse_mode="HTML")
                time.sleep(0.05)

def start_routine(bot):
    digest_checking_thread = threading.Thread(target=check_routine, args=(bot,), daemon=True)
    digest_checking_thread.start()

def read_routines(chat_id):
    routines = database.get_routine_list(chat_id)

    routine_reply = config.RESPONSES['empty_routines']

    if routines:
        routine_reply = config.RESPONSES['reply_routines']
        
        for routine in routines:
            routine_reply += f"* {routine[0]} - {routine[1]}\n"

    return routine_reply

def clean_routines(chat_id):
    database.clean_routines(chat_id)

    return config.RESPONSES['clean_routines']

def delete_routine(message):
    chat_id = message.chat.id
    args = message.text.split()

    if len(args) > 1:
        number = int(args[1])

    database.delete_routine(chat_id, number)

    return config.RESPONSES['delete_routine']