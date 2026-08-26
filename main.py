import gc
import os
from bot import bot
from src import database, digest, memo, routine

if __name__ == "__main__":
    print(f"Bot started at PID: {os.getpid()}")
    
    print("Starting database...", end="")
    database.initialise()
    print(" OK")
    
    print("Starting memo alert system...", end="")
    memo.start_memo_alert(bot)
    print(" OK")

    print("Starting routine system...", end="")
    routine.start_routine(bot)
    print(" OK")

    print("Starting digest system...", end="")
    digest.start_daily_digest(bot)
    print(" OK")

    gc.collect()

    print("Bot is now polling...")
    bot.infinity_polling()