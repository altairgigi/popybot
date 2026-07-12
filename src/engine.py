import gc
import torch
import spacy
import numpy
from spacy.matcher import Matcher
from src.nltk_utils import tokenise, stem, bag_of_words
from src.model import NeuralNet
import config

nlp = spacy.load('it_core_news_sm')

matcher = Matcher(nlp.vocab)

date_idioms_pattern = config.DATE_IDIOMS
day_of_week_pattern = config.DAY_OF_WEEK
time_of_day_pattern = config.TIME_IDIOMS

custom_date_pattern = [date_idioms_pattern, day_of_week_pattern] + config.DATE_DURATIONS

matcher.add("CUSTOM DATE", custom_date_pattern)
matcher.add("CUSTOM TIME", time_of_day_pattern)

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
    doc = nlp(message)
    entities = {"action": None, "date": None, "time": None}

    if intent == "weather":
        locations = [ent.text for ent in doc.ents if ent.label_ in ["LOC", "GPE"]]
        entities["location"] = locations[0] if locations else None

    elif intent == "memo":
        date_ent = []
        time_ent = []

        matches = matcher(doc)
        match_indexes = set()

        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]

            for index in range(start, end):
                match_indexes.add(index)

            if string_id == "CUSTOM DATE":
                date_ent.append(span.text)
            elif string_id == "CUSTOM TIME":
                time_ent.append(span.text)

        for ent in doc.ents:
            if(ent.label_ == "DATE"):
                date_ent.append(ent)
            elif(ent.label_ == "TIME"):
                time_ent.append(ent)

        entities["date"] = date_ent[0] if date_ent else None
        entities["time"] = time_ent[0] if time_ent else None
        
        action = message
        for t in time_ent:
            action = action.replace(t, "")
        for d in date_ent:
            action = action.replace(d, "")
        
        for trigger in config.MEMO_PREFIX_LIST:
            if action.lower().startswith(trigger):
                action = action[len(trigger):].strip()
                
        entities["action"] = action.strip(", ")

    return entities