import json
import numpy
import torch
from torch.utils.data import Dataset, DataLoader
from src.nltk_utils import tokenise, stem, bag_of_words
from src.model import NeuralNet

INTENTS_FILE = 'intents.json'

def train():
    with open(INTENTS_FILE, "r", encoding="utf_8") as file:
        intents_data = json.load(file)

    all_words = []
    tags = []
    xy = []

    for intent in intents_data['intents']:
        tags.append(intent['tag'])
        for pattern in intent['patterns']:
            tokenised_sentence = tokenise(pattern)
            xy.append((tokenised_sentence, intent['tag']))
            all_words.extend(tokenised_sentence)

    ignore_list= ['?', '!', '.', ',', '', "'"]
    all_words = [stem(word) for word in all_words if word not in ignore_list]

    all_words = sorted(list(set(all_words)))
    tags = sorted(list(set(tags)))

    x_train = []
    y_train = []

    for (pattern_sentence, tag) in xy:
        x_train.append(bag_of_words(pattern_sentence, all_words))
        y_train.append(tags.index(tag))

    X_train = numpy.array(x_train)
    Y_train = numpy.array(y_train)

    batch_size = 8
    hidden_size = 8
    input_size = len(all_words)
    output_size = len(tags)
    learning_rate = 0.001
    num_epochs = 1000

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    dataset = BotDataSet(X_train, Y_train)
    train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)

    model = NeuralNet(input_size, hidden_size, output_size)

    criterion = torch.nn.CrossEntropyLoss()
    optimiser = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        for (words, labels) in train_loader:
            words = words.to(device, dtype=torch.float32)
            labels = labels.to(device, dtype=torch.long)

            outputs = model(words)
            loss = criterion(outputs, labels)

            optimiser.zero_grad()
            loss.backward()
            optimiser.step()

        if (epoch + 1) % 100 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')
    
    print(f'Training complete! Loss: {loss.item():.4f}')

    data = {
        "model_state": model.state_dict(),
        "input_size": input_size,
        "output_size": output_size,
        "hidden_size": hidden_size,
        "all_words": all_words,
        "tags": tags
    }

    FILE = 'data.pth'
    torch.save(data, FILE)
    print("Training file created with success!")

    #print("=== LOADING TEST ===")
    #print(f"Unique tags found ({len(tags)}): {tags}")
    #print(f"Number of unique words in the vocabulary: {len(all_words)}")
    #print(f"First 10 elements in the vocabulary: {all_words[:10]}")
    #print(f"Total number of pattern-tag pairs (xy): {len(xy)}")
    #print(f"Shape of X_train: {X_train.shape}")
    #print(f"Shape of y_train: {Y_train.shape}")

    #print("=== MODEL TEST ===")
    #print("Modello creato con successo e pronto per l'addestramento!")
    #print(f"Configurazione: Input={input_size}, Nascosti={hidden_size}, Output={output_size}")

class BotDataSet(Dataset):
    def __init__(self, X_data, Y_data):
        self.n_samples = len(X_data)
        self.x_data = X_data
        self.y_data = Y_data
    
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]
    
    def __len__(self):
        return self.n_samples

if __name__ == '__main__':
    train()