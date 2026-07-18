#intents linked to functions
INTENTS = {
    "memo": "memo",
    "weather": "weather",
    "greet": "greeting",
    "?": "unknown"
}

#default responses
RESPONSES = {
    "start": "PRONTI!",
    "help": "Per adesso non so fare molto. Posso salutare, dirti il meteo o ricordarti le cose.",
    "unknown_replies": [
        "6 7",
        "C'hai detto?",
        "'Nche senso, scusa?"
    ],
    "greeting": ", come posso aiutarti?",
    "reply_list": "Ecco i tuoi promemoria:\n",
    "empty_list": "La lista dei promemoria è vuota!",
    "clean_list": "La lista dei promemoria è stata svuotata!",
    "missing_memo": "Non mi ha detto cosa devo ricordarti.",
    "missing_city": "Non sono riuscito a controllare il meteo! Controlla di aver scritto bene il nome della città.",
    "voice_issue": "Non ho capito cosa hai detto, puoi ripetere?",
    "voice_connection_issue": "In questo momento ho problemi a connettermi al servizio di trascrizione."
}

#templates for replies
TEMPLATES = {
    "weather_report": "Questo è il tempo a <b>{location}</b>:\n{condition}\n<b>{temperature}°C</b>",
    "forecast_header": "Questo è il tempo a <b>{location}</b> nei prossimi giorni:",
    "forecast_report": "<b>{date}</b>:\n{condition}\nMassima: <b>{temp_max}°C</b>\nMinima: <b>{temp_min}°C</b>",
    "memo_save": "Fatto! Ho annotato '{title}' alle {time} il {date}.",
    "memo_alert": "<b>PROMEMORIA!</b>\n\nNon scordarti di <b><i>{memo}</i></b>!"
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
            "all'una": "13:00",
            "l'una": "13:00",
            "mezzogiorno": "12:00",
            "mezzanotte": "00:00"
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

WEATHER_PREFIX_LIST = [
    "di", 
    "a", 
    "per", 
    "su", 
    "meteo"
]

GENERIC_PREFIX_LIST = [
    "il",
    "tra",
    "fra",
    "verso",
    "le",
    "per"
]

#regex patterns
ARTICLES = r"\b(un|una|uno)"
PREPOSITIONS = r"\b(il|tra|fra|per)"
PREFIX_PATTERN = r"(?:\b(?:" + "|".join(GENERIC_PREFIX_LIST) + r")\b\s*)*"
TIME_PATTERN = PREFIX_PATTERN + r"(?:a|alle|le)?\s(\d{1,2})(?::(\d{2}))?"
WEATHER_PATTERN = r"\b(" + "|".join(WEATHER_PREFIX_LIST) + r")\s+([a-z\s]+)"

#default values
DATABASE_NAME = "memo_data.db"
MODEL_DATA = "src/model.tflite"
META_DATA = "src/metadata.json"
DEFAULT_MINUTES = "00"
DEFAULT_HOUR = "09"
LANG = "it"
LANGUAGE = "it_IT"
WEATHER_SERVICE_URL = "https://api.weatherapi.com/v1/current.json"
FORECAST_SERVICE_URL = "https://api.weatherapi.com/v1/forecast.json"