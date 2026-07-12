import re
import time
import threading
import dateparser
from datetime import datetime
from src import database
import config

def extract_time_and_date(time_raw, date_raw):
    memo_hour = config.DEFAULT_HOUR
    memo_minutes = config.DEFAULT_MINUTES
    memo_date = datetime.now()

    translation_rules = config.TRANSLATIONS.get(config.LANG, {"idiomatic_times": {}, "removables": []})

    components = []
    if date_raw:
        date_clean = str(date_raw).lower().strip()

        date_clean = re.sub(config.ARTICLE_TO_QUANTITY, "1", date_clean)

        for prefix in translation_rules["removables"]:
            date_clean = date_clean.replace(prefix, "").strip()

        components.append(date_clean)
    if time_raw:
        time_clean = str(time_raw).lower().strip()

        for expression, translation in translation_rules["idiomatic_times"].items():
            time_clean = time_clean.replace(expression, translation)

        components.append(time_clean)

    temp_text = " ".join(components).strip()

    settings = {
        'PREFER_DATES_FROM': 'future',
        'RETURN_AS_TIMEZONE_AWARE': False,
        'RELATIVE_BASE': datetime.now(),
    }

    parsed = None
    if temp_text:
        parsed = dateparser.parse(
            temp_text, 
            languages=[config.LANG], 
            settings=settings
        )

        if parsed:
            memo_date = parsed

            if time_raw:
                memo_hour = parsed.strftime("%H")
                memo_minutes = parsed.strftime("%M")

    memo_time = f"{memo_hour}:{memo_minutes}"
    memo_date = memo_date.strftime("%d/%m/%Y")

    return memo_time, memo_date

def write_memo(chat_id, title, time_raw, date_raw):
    if not title.strip():
        return config.RESPONSES['missing_memo']
    
    time, date = extract_time_and_date(time_raw, date_raw)
    
    database.add_memo(chat_id, title, time, date)

    return config.TEMPLATES['memo_save'].format(title=title, time=time, date=date) 

def memo_alert(bot):
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_date = now.strftime("%d/%m/%Y")
    
        expired_memos = database.check_memo(current_time, current_date)
        
        if expired_memos:
            for memo in expired_memos:
                bot.send_message(memo[1], config.TEMPLATES['memo_alert'].format(memo=memo[2]), parse_mode="HTML")

        time.sleep(60)

def start_memo_alert(bot):
    memo_checking_thread = threading.Thread(target=memo_alert, args=(bot,), daemon=True)
    memo_checking_thread.start()

def read_memos(chat_id):
    memos = database.get_memo_list(chat_id)

    memo_reply = config.RESPONSES['empty_list']

    if memos:
        memo_reply = config.RESPONSES['reply_list']
        
        for memo in memos:
            memo_reply += f"* {memo[0]} - {memo[1]} {memo[2]}\n"

    return memo_reply

def clean_memos(chat_id):
    database.clean_memo_list(chat_id)

    return config.RESPONSES['clean_list']