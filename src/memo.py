import time
import threading
from datetime import datetime
from src import database
import config

def write_memo(chat_id, title, time, date):
    if not title.strip():
        return config.RESPONSES['missing_memo']
    
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