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

        wait_time = 60 - datetime.now().second
        time.sleep(wait_time)

def start_memo_alert(bot):
    memo_checking_thread = threading.Thread(target=memo_alert, args=(bot,), daemon=True)
    memo_checking_thread.start()

def read_memos(chat_id):
    memos = database.get_memo_list(chat_id)

    memo_reply = config.RESPONSES['empty_memos']

    if memos:
        memo_reply = config.RESPONSES['reply_memos']
        
        for memo in memos:
            memo_reply += f"* {memo[0]} - {memo[1]} {memo[2]}\n"

    return memo_reply

def clean_memos(chat_id):
    database.clean_memo_list(chat_id)

    return config.RESPONSES['clean_memos']

def delete_memo(message):
    chat_id = message.chat.id
    args = message.text.split()

    if len(args) > 1:
        number = int(args[1])

    database.delete_memo(chat_id, number)

    return config.RESPONSES['delete_memo']