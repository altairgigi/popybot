from datetime import datetime
import config

def greet_user():
    time = datetime.now().hour

    if 5 < time <= 12:
        reply_greet = config.GREETINGS['morning']
    elif 12 < time <= 18:
        reply_greet = config.GREETINGS['afternoon']
    elif 18 < time <= 23:
        reply_greet = config.GREETINGS['evening']
    else:
        reply_greet = config.GREETINGS['generic']

    return reply_greet + config.RESPONSES['greeting']
