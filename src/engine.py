import gc
import re
import torch
import numpy
import dateparser.search
from datetime import datetime
from src.nltk_utils import tokenise, bag_of_words
from src.model import NeuralNet
import config

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

FILE = config.MODEL_DATA
data = torch.load(FILE, map_location=device)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

torch.set_grad_enabled(False)

del data
gc.collect()

def decode_intent(message):
    tokenised = tokenise(message)
    X = bag_of_words(tokenised, all_words)

    if numpy.sum(X) == 0:
        return None
    
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device, dtype=torch.float32)

    outputs = model(X)
    _, predicted = torch.max(outputs, dim=1)
    intent = tags[predicted.item()]

    probs = torch.softmax(outputs, dim=1)
    prob = probs[0][predicted.item()].item()

    if prob > 0.75:
        return intent
    return None

def extract_entities(message, intent):
    entities = {"action": None, "date": None, "time": None, "location": None}
    clean_text = message.replace("?", "").replace(".", "").strip()

    matches = dateparser.search.search_dates(
        clean_text,
        languages=[config.LANG],
        settings={
            'PREFER_DATES_FROM': 'future',
            'RELATIVE_BASE': datetime.now()
        }
    )

    print("Tutti i match trovati:", matches)

    if matches:
        text, temporal_data = matches[0]
        
        entities['date'] = temporal_data.strftime("%d/%m/%Y")

        clean_text = clean_text.replace(text, "").strip()

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
        for prefix in config.MEMO_PREFIX_LIST:
            if clean_text.lower().startswith(prefix):
                clean_text = clean_text[len(prefix):].strip()

        time_match = re.search(config.TIME_PATTERN, clean_text, re.IGNORECASE)

        memo_hour = config.DEFAULT_HOUR
        memo_minutes = config.DEFAULT_MINUTES

        if time_match:
            memo_hour = time_match.group(1).zfill(2)
            if time_match.group(2):
                memo_minutes = time_match.group(2)
            
            clean_text = re.sub(config.TIME_PATTERN, "", clean_text).strip()

            entities['time'] = f"{memo_hour}:{memo_minutes}"

    entities["action"] = clean_text.strip(", ")

    print(entities)

    return entities