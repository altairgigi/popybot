#intents linked to functions
INTENTS = {
    "greet": "greeting",
    "memo": "memo",
    "news": "news",
    "weather": "weather",
    "?": "unknown"
}

#default responses
RESPONSES = {
    "start": "PRONTI!",
    "help": "Ciao! Io sono PoPyBot, il tuo assistente virtuale Telegram scritto interamente in Python!\n"
            "Attualmente, posso dirti il meteo (es. 'che tempo fa a Roma?'), darti le ultime notizie (es. 'quali sono le ultime notizie?') e ricordarti le cose (es. 'ricordami di fare la spesa domani alle 11') in maniera completamente autonoma.\n"
            "\nSe lo imposti con il comando '/set_digest orario luogo', farò un riepilogo giornaliero all'orario scelto con il meteo del luogo selezionato.\n"
            "Inoltre, con il comando '/set_routine \"titolo\" orario', puoi impostare promemoria quotidiani.\n"
            "Altri comandi che puoi usare sono '/memo' per vedere i tuoi promemoria e '/clean' per cancellarli tutti.\n"
            "\nInoltre, per richieste più complesse, posso chiedere aiuto al mio cervello di riserva ospitato su Ollama (se configurato).\n"
            "Dimmi pure cosa ti serve e cercherò di aiutarti come posso!",
    "unknown_replies": [
        "6 7",
        "C'hai detto?",
        "'Nche senso, scusa?"
    ],
    "greeting": ", come posso aiutarti?",
    "digest_error": "Errore! Assicurati di scrivere 'orario' e 'luogo' dopo il comando e che l'orario sia in formato 'HH:MM'!",
    "digest_set": "Riepilogo impostato!",
    "routine_error": "Errore! Assicurati di scrivere 'titolo' e 'orario' dopo il comando, che il titolo sia tra doppi apici e che l'orario sia in formato 'HH:MM'!",
    "routine_set": "Routine impostata!",
    "reply_list": "Ecco i tuoi promemoria:\n",
    "empty_list": "La lista dei promemoria è vuota!",
    "clean_list": "La lista dei promemoria è stata svuotata!",
    "missing_memo": "Non mi ha detto cosa devo ricordarti.",
    "missing_city": "Non sono riuscito a controllare il meteo! Controlla di aver scritto bene il nome della città.",
    "news_error": "Non sono riuscito a trovare notizie!", 
    "voice_issue": "Non ho capito cosa hai detto, puoi ripetere?",
    "voice_connection_issue": "In questo momento ho problemi a connettermi al servizio di trascrizione."
}

#templates for replies
TEMPLATES = {
    "weather_report": "Questo è il tempo a <b>{location}</b>:\n"
                      "{condition}\n"
                      "<b>{temperature}°C</b>",
    "forecast_header": "Questo è il tempo a <b>{location}</b> nei prossimi giorni:\n",
    "forecast_report": "<b>{date}</b>:\n"
                       "{condition}\n"
                       "Massima: <b>{temp_max}°C</b>\n"
                       "Minima: <b>{temp_min}°C</b>",
    "memo_save": "Fatto! Ho annotato '{title}' alle {time} il {date}.",
    "memo_alert": "<b>PROMEMORIA!</b>\n\n"
                  "Non scordarti di <b><i>{memo}</i></b>!",
    "digest_memo_none": "Non hai promemoria oggi!\n",
    "digest_memo_intro": "I tuoi promemoria di oggi:\n",
    "digest_report": "{intro}, ecco il tuo riepilogo giornaliero!\n\n{weather}\n\n{memo}\n{news}",
    "news_report": "Ecco le ultime notizie:\n{news}",
    "news_feed": "<b>{title}</b>\n<i>{description}</i>\nPubblicato il {date}\n<a href='{link}'><b>Link</b></a>\n",
    "stats_report": "<b>PoPyBot</b> V2.4.1\nRunning on <i>{os}</i>:\n"
                    "<b>CPU</b>: {cpu_load}%\t<b>RAM</b>: {ram_load}%\n"
                    "<b>Up</b>: {upload}Mb\t<b>Down</b>: {download}Mb\n"
                    "<b>Batt</b>: {battery}\t<b>Temp</b>: {temperature}\n"
                    "<b>Uptime</b>: {uptime}"
}

#default greetings
GREETINGS = {
    "generic": "Ciao",
    "morning": "Buongiorno",
    "afternoon": "Buon pomeriggio",
    "evening": "Buonasera"
}

#default temp audio files
AUDIO_PATH = {
    "ogg_path": "audio/voice.ogg",
    "wav_path": "audio/voice.wav"
}

#idiomatic translation for spacy
TRANSLATIONS = {
    "it": {
        "idiomatic_times": {
            "all'una": "alle 13:00",
            "l'una": "alle 13:00",
            "a mezzogiorno": "alle 12:00",
            "a mezzanotte": "alle 00:00"
        },
        "idiomatic_dates": {
            "dopodomani": "fra 2 giorni"
        },
        "removables": ["di", "a", "verso", "per"]
    }
}

#prefixes lists
MEMO_PREFIX_LIST = [
    "ricordami di ", 
    "ricordami che ", 
    "crea un promemoria ", 
    "crea una nota ", 
    "scrivi un promemoria ", 
    "scrivi una nota ", 
    "mi ricordi di ", 
    "mi ricodi che ",
    "annota di ",
    "annotami che "
]

NEWS_PREFIX_LIST = [ 
    "a", 
    "da",
]

WEATHER_PREFIX_LIST = [
    "di", 
    "a", 
    "per", 
    "su"
]

GENERIC_PREFIX_LIST = [
    "a",
    "al",
    "alle",
    "il",
    "tra",
    "fra",
    "verso",
    "le",
    "per",
    "di"
]

#regex patterns
ARTICLES = r"\b(un|una|uno)"
PREPOSITIONS = r"\b(il|tra|fra|per)"
PREFIX_PATTERN = r"(?:\b(?:" + "|".join(GENERIC_PREFIX_LIST) + r")\b\s*)*"
MEMO_PATTERN = r".*?\b(?:" + "|".join(MEMO_PREFIX_LIST) + r"\b)"
NEWS_PATTERN = r"\b(" + "|".join(NEWS_PREFIX_LIST) + r")\s+([a-z\s]+)"
TIME_PATTERN = PREFIX_PATTERN + r"(?:a|alle|le)?\s(\d{1,2})(?::(\d{2}))?"
WEATHER_PATTERN = r"\b(" + "|".join(WEATHER_PREFIX_LIST) + r")\s+([a-z\s]+)"

#default values
DATABASE_NAME = "memo_data.db"
MODEL_DATA = "src/model.tflite"
META_DATA = "src/metadata.json"
DEFAULT_HOUR = "09"
DEFAULT_MINUTES = "00"
DIGEST_NEWS = 3
REPORT_NEWS = 5
LANG = "it"
LANGUAGE = "it_IT"
WEATHER_SERVICE_URL = "https://api.weatherapi.com/v1/current.json"
FORECAST_SERVICE_URL = "https://api.weatherapi.com/v1/forecast.json"
NEWS_OUTLET_URL = "https://www.ansa.it/sito/ansait_rss.xml"