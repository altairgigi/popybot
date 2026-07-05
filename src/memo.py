import re
import time
import threading
from datetime import datetime, timedelta
from src import database
import config

def extract_time_and_date(user_text):
    time_pattern = config.TIME_PATTERN
    date_pattern = config.DATE_PATTERN

    time_match = re.search(time_pattern, user_text)
    date_match = re.search(date_pattern, user_text)

    memo_hour = config.DEFAULT_HOUR
    memo_minutes = config.DEFAULT_MINUTES
    date_found = config.DEFAULT_DATE

    if time_match:
        memo_hour = time_match.group(1)
        if time_match.group(2):
            memo_minutes = time_match.group(2)

    if date_match:
        date_found = date_match.group(1)

    day_map = config.DAY_MAP

    today = datetime.now()
    
    if date_found is None or date_found == config.DAYS['today']:
        memo_date = today
    elif date_found == config.DAYS['tomorrow']:
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
    prefix_list = config.MEMO_PREFIX_LIST
    user_text = None

    for prefix in prefix_list:
        if user_message.startswith(prefix):
            user_text = user_message[len(prefix):]
            break

    if user_text == None:
        user_text = user_message

    if not user_text.strip():
        return config.RESPONSES['missing_memo']
    
    title, time, date = extract_time_and_date(user_text)
    
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