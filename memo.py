import re
import time
import threading
from datetime import datetime, timedelta
import database

def extract_time_and_date(user_text):
    time_pattern = r"alle\s(\d{1,2})(?::(\d{2}))?"
    date_pattern = r"\b(luned[ìi]|marted[ìi]|mercoled[ìi]|gioved[ìi]|venerd[ìi]|sabato|domenica|domani|oggi)\b"

    time_match = re.search(time_pattern, user_text)
    date_match = re.search(date_pattern, user_text)

    memo_hour = "09"
    memo_minutes = "00"
    date_found = None

    if time_match:
        memo_hour = time_match.group(1)
        if time_match.group(2):
            memo_minutes = time_match.group(2)

    if date_match:
        date_found = date_match.group(1)

    day_map = {
        "lunedì": 0, "lunedi": 0,
        "martedì": 1, "martedi": 1,
        "mercoledì": 2, "mercoledi": 2,
        "giovedì": 3, "giovedi": 3,
        "venerdì": 4, "venerdi": 4,
        "sabato": 5,
        "domenica": 6 
    }

    today = datetime.now()
    
    if date_found is None or date_found == "oggi":
        memo_date = today
    elif date_found == "domani":
        memo_date = today + timedelta(days=1)
    else:
        target_weekday = day_map[date_found]
        current_weekday = today.weekday()

        difference_days = target_weekday - current_weekday 

        if difference_days <= 0:
            difference_days += 7

        memo_date = today + timedelta(days=difference_days)

    memo_title = re.sub(time_pattern, "", user_text).strip()
    memo_title = re.sub(date_pattern, "", memo_title).strip()

    memo_time = f"{memo_hour}:{memo_minutes}"

    memo_date = memo_date.strftime("%d/%m/%Y")

    return memo_title, memo_time, memo_date

def write_memo(user_message, chat_id):
    PREFIX_LIST = ["ricordami di ", "crea un promemoria ", "crea una nota ", "scrivi un promemoria ", "scrivi una nota ", "mi ricordi di "]

    for prefix in PREFIX_LIST:
        if user_message.startswith(prefix):
            user_text = user_message[len(prefix):]
            break

    if not user_text.strip():
        return "Non mi ha detto cosa devo ricordarti."
    
    title, time, date = extract_time_and_date(user_text)
    
    database.add_memo(chat_id, title, time, date)

    return f"Fatto! Ho annotato '{title}' alle {time} il {date}." 

def memo_alert(bot):
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_date = now.strftime("%d/%m/%Y")
    
        expired_memos = database.check_memo(current_time, current_date)
        
        if expired_memos:
            for memo in expired_memos:
                bot.send_message(memo[1], f"<b>PROMEMORIA!</b>\n\nNon scordarti di <b><i>{memo[2]}</i></b>!", parse_mode="HTML")

        time.sleep(60)

def start_memo_alert(bot):
    memo_checking_thread = threading.Thread(target=memo_alert, args=(bot,), daemon=True)
    memo_checking_thread.start()

def read_memos(chat_id):
    memos = database.get_memo_list(chat_id)

    memo_reply = "La lista dei promemoria è vuota!"

    if memos:
        memo_reply = "Ecco i tuoi promemoria:\n"
        
        for memo in memos:
            memo_reply += f"* {memo[0]} - {memo[1]} {memo[2]}\n"

    return memo_reply

def clean_memos(chat_id):
    database.clean_memo_list(chat_id)

    return "La lista dei promemoria è stata svuotata!"