from bot import bot
from src import database, memo

if __name__ == "__main__":
    print("Starting database...")
    database.initialise()
    
    print("Starting alert system...")
    memo.start_memo_alert(bot)

    print("Bot listening...")
    bot.infinity_polling()