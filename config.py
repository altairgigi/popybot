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
    "weather_report": "Questo è il tempo a <b>{city}</b>:\n{condition}\n<b>{temperature}°C</b>",
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
        "removables": ["fra ", "tra ", "in "]
    }
}

#custom patters for spacy
DATE_IDIOMS = [
    {"LOWER": {"IN": ["domani", "dopodomani", "stasera", "oggi", "ieri"]}}
]

DATE_DURATIONS = [
    [
        {"LOWER": {"IN": ["fra", "tra", "in"]}},
        {"LIKE_NUM": True},
        {"LOWER": {"IN": ["settimana", "settimane", "mese", "mesi", "anno", "anni", "giorno", "giorni"]}}
    ],
    [
        {"LOWER": {"IN": ["fra", "tra", "in"]}},
        {"LOWER": {"IN": ["un", "uno", "una"]}},
        {"LOWER": {"IN": ["settimana", "settimane", "mese", "mesi", "anno", "anni", "giorno", "giorni"]}}
    ]
]

DAY_OF_WEEK = [
    {"LOWER": {"IN": ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]}}
]

TIME_IDIOMS = [
    [
        {"LOWER": {"IN": ["l'", "all'"]}, "OP": "?"}, 
        {"LOWER": {"IN": ["mezzogiorno", "mezzanotte"]}}
    ],
    [
        {"LOWER": {"IN": ["l'", "all'"]}}, 
        {"LOWER": "una"}
    ],
    [
        {"LOWER": "una"},
        {"LOWER": {"IN": ["di", "del", "in"]}},
        {"LOWER": {"IN": ["notte", "pomeriggio", "mattina", "punto"]}}
    ]
]

#regex to substitute articles with quantity
ARTICLE_TO_QUANTITY = r"\b(un|uno|una)\b"

#days
DAYS = {
    "today": "oggi",
    "tomorrow": "domani",
    "dayafter": "dopodomani"
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

#default values
DATABASE_NAME = "memo_data.db"
MODEL_DATA = 'src/data.pth'
DEFAULT_MINUTES = "00"
DEFAULT_HOUR = "09"
LANG = "it"
LANGUAGE = "it_IT"
WEATHER_SERVICE_URL = "https://api.weatherapi.com/v1/current.json"