import time
import threading
from datetime import datetime
from src import database, greet, news, weather
import config

def set_digest(message):
    args = message.text.split()

    if len(args) >= 3:
        try:
            datetime.strptime(args[1], "%H:%M")
        except ValueError:
            return config.RESPONSES['digest_error']

        location = " ".join(args[2:])

        database.set_user_settings(message.chat.id, args[1], location)
        return config.RESPONSES['digest_set']
    else:
        return config.RESPONSES['digest_error']

def daily_digest(bot):
    while True:
        wait_time = 60 - datetime.now().second
        time.sleep(wait_time)

        time_now = datetime.now().strftime("%H:%M")
        date_today = datetime.now().strftime("%d/%m/%Y")

        digest_list = database.get_digest_list(time_now)

        if len(digest_list) >= 1:
            for chat_id, location in digest_list:
                digest_intro = greet.greet_user()
                digest_weather = weather.get_weather(location)
                daily_memo_list = database.get_daily_memo_list(chat_id, date_today)
                digest_news = news.get_news(config.DIGEST_NEWS)

                if len(daily_memo_list) >= 1:
                    digest_memo = config.TEMPLATES['digest_memo_intro']

                    for memo in daily_memo_list:
                        digest_memo += f"* {memo[0]} - {memo[1]}\n"
                else:
                    digest_memo = config.TEMPLATES['digest_memo_none']

                digest = config.TEMPLATES['digest_report'].format(
                    intro= digest_intro,
                    weather= digest_weather,
                    memo= digest_memo,
                    news= digest_news
                )

                bot.send_message(chat_id, digest, parse_mode="HTML", disable_web_page_preview=True)
                time.sleep(0.05)

def start_daily_digest(bot):
    digest_checking_thread = threading.Thread(target=daily_digest, args=(bot,), daemon=True)
    digest_checking_thread.start()