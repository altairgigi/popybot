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