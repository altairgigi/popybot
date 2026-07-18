import gc
import os
from bot import bot
from src import database, memo

if __name__ == "__main__":
    print(f"Bot started. PID: {os.getpid()}")
    print("Starting database...")
    database.initialise()
    
    print("Starting alert system...")
    memo.start_memo_alert(bot)

    gc.collect()

    print("Bot is listening...")
    bot.infinity_polling()