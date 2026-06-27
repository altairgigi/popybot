from datetime import datetime

def greet_user():
    time = datetime.now().hour

    if 5 < time <= 12:
        reply_greet = "Buongiorno"
    elif 12 < time <= 18:
        reply_greet = "Buon pomeriggio"
    elif 18 < time <= 23:
        reply_greet = "Buonasera"
    else:
        reply_greet = "Ciao"

    return reply_greet + ", come posso aiutarti?"
