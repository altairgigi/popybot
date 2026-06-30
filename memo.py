import os
import re
import time
import threading
from datetime import datetime, timedelta

FILE = "memo.txt"

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
    
    memo_date = memo_date.strftime("%d/%m/%Y")

    memo_title = re.sub(time_pattern, "", user_text).strip()
    memo_title = re.sub(date_pattern, "", memo_title).strip()

    return f"{memo_title} - {memo_hour}:{memo_minutes} {memo_date}"

def write_memo(user_message, chat_id):
    PREFIX_LIST = ["ricordami di ", "crea un promemoria ", "crea una nota ", "scrivi un promemoria ", "scrivi una nota ", "mi ricordi di "]
    user_text = user_message.lower()
    for prefix in PREFIX_LIST:
        if user_text.startswith(prefix):
            user_text = user_message[len(prefix):]
            break

    if not user_text.strip():
        return "Non mi ha detto cosa devo ricordarti."
    
    user_memo = extract_time_and_date(user_text)
    
    with open(FILE, "a", encoding="utf-8") as file:
        file.write(f"* {chat_id} - {user_memo}\n")

    return f"Fatto! Ho annotato '{user_memo}'." 

def check_memo(bot):
    while True:
        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            current_date = now.strftime("%d/%m/%Y")

            unexpired_memos = []
            expired_memos = []
        
            try:
                with open(FILE, "r", encoding="utf-8") as file:
                    lines = file.readlines()
            except FileNotFoundError:
                lines = []
            
            for line in lines:
                if current_time in line and current_date in line:
                    chat_id = line.replace("*", "").split("-")[0].strip()
                    memo_title = line.split("-")[1].strip()
                    expired_memos.append(memo_title)
                else:
                    unexpired_memos.append(line)
            
            if expired_memos:
                for memo in expired_memos:
                    bot.send_message(chat_id, f"<b>PROMEMORIA!</b>\n\nNon scordarti di <b><i>{memo}</i></b>!", parse_mode="HTML")

                with open(FILE, "w", encoding="utf-8") as file:
                    file.writelines(unexpired_memos)
        
        except Exception as e:
            print(f"Error in memo check loop: {e}")

        time.sleep(60)

def start_check_memo(bot):
    memo_checking_thread = threading.Thread(target=check_memo, args=(bot,), daemon=True)
    memo_checking_thread.start()

def read_memo():
    if not os.path.exists(FILE) or os.path.getsize(FILE) == 0:
        return "Non hai ancora nessun promemoria"

    with open(FILE, "r", encoding="utf-8") as file:
        memo_list = file.readlines()

    memo_reply = "Ecco i tuoi promemoria:\n"

    return memo_reply + "".join(memo_list)
