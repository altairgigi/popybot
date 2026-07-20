import re
import json
import numpy
import ai_edge_litert.interpreter as litert
import dateparser.search
from datetime import datetime
from src.nltk_utils import tokenise, bag_of_words
import config

with open(config.META_DATA, "r", encoding="utf-8") as data:
    metadata = json.load(data)

all_words = metadata["all_words"]
tags = metadata["tags"]

del metadata

interpreter = litert.Interpreter(model_path=config.MODEL_DATA)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def decode_intent(message):
    tokenised = tokenise(message)
    X = bag_of_words(tokenised, all_words)

    if numpy.sum(X) == 0:
        return None
    
    X = X.reshape(1, X.shape[0]).astype(numpy.float32)

    interpreter.set_tensor(input_details[0]['index'], X)
    interpreter.invoke()
    outputs = interpreter.get_tensor(output_details[0]['index'])

    predicted_idx = numpy.argmax(outputs, axis=1)[0]
    intent = tags[predicted_idx]

    exp_outputs = numpy.exp(outputs - numpy.max(outputs))
    probs = exp_outputs / numpy.sum(exp_outputs, axis=1, keepdims=True)
    prob = probs[0][predicted_idx]

    if prob >= 0.80:
        return intent
    return None

def extract_entities(message, intent):
    entities = {"action": None, "date": None, "time": None, "location": None}
    clean_text = message.replace("?", "").replace(".", "").strip()

    translation_rules_for_time = config.TRANSLATIONS.get(config.LANG, {"idiomatic_times": {}})
    translation_rules_for_date = config.TRANSLATIONS.get(config.LANG, {"idiomatic_dates": {}})
    removables_list = config.TRANSLATIONS.get(config.LANG, {"removables": []})
    removables = r"(?:\b(?:" + "|".join(removables_list) + r")\b['\s]*)*"
    
    for word, value in translation_rules_for_time['idiomatic_times'].items():
        pattern = r"\b" + re.escape(word) + r"\b"
        if re.search(pattern, clean_text, re.IGNORECASE):
            clean_text = re.sub(removables + pattern, value, clean_text, flags=re.IGNORECASE)
            break
    
    for word, value in translation_rules_for_date['idiomatic_dates'].items():
        pattern = r"\b" + re.escape(word) + r"\b"
        if re.search(pattern, clean_text, re.IGNORECASE):
            clean_text = re.sub(removables + pattern, value, clean_text, flags=re.IGNORECASE)
            break

    matches = dateparser.search.search_dates(
        clean_text,
        languages=[config.LANG],
        settings={
            'PREFER_DATES_FROM': 'future',
            'RETURN_AS_TIMEZONE_AWARE': False,
            'RELATIVE_BASE': datetime.now()
        }
    )

    memo_date = datetime.now().date().strftime("%d/%m/%Y")
    memo_hour = config.DEFAULT_HOUR
    memo_minutes = config.DEFAULT_MINUTES

    if matches:
        text, temporal_data = matches[0]
        
        memo_date = temporal_data.strftime("%d/%m/%Y")

        time_match = re.search(config.TIME_PATTERN, clean_text, re.IGNORECASE)

        if time_match:
            memo_hour = time_match.group(1).zfill(2)
            if time_match.group(2):
                memo_minutes = time_match.group(2)
            
            clean_text = re.sub(config.TIME_PATTERN, "", clean_text).strip()

        clean_text = re.sub(config.PREFIX_PATTERN + re.escape(text), "", clean_text, flags=re.IGNORECASE)
    
    entities['date'] = memo_date
    entities['time'] = f"{memo_hour}:{memo_minutes}"

    if intent == "weather":
        for prefix in config.WEATHER_PREFIX_LIST:
            if clean_text.lower().startswith(prefix):
                clean_text = clean_text[len(prefix):].strip()
        
        city_match = re.search(config.WEATHER_PATTERN, clean_text, re.IGNORECASE)

        if city_match:
            entities['location'] = city_match.group(2).strip()
        else:
            entities['location'] = clean_text

    if intent == 'memo':
        clean_text = re.sub(config.MEMO_PATTERN, "", clean_text).strip()

        entities["action"] = clean_text.strip(", ")

    return entities