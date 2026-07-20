import json
import torch
import torchvision
import litert_torch
from src.model import NeuralNet

def convert_model():
    INPUT_FILE = "data.pth"
    OUTPUT_MODEL = "model.tflite"
    OUTPUT_METADATA = "metadata.json"

    device = torch.device('cpu')

    try:
        data = torch.load(INPUT_FILE, map_location=device)
    except FileNotFoundError:
        print("Model data not found! Train the model first!")

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data["all_words"]
    tags = data["tags"]
    model_state = data["model_state"]

    print("Data loaded with success!")

    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()

    sample_inputs = (torch.randn(1, input_size),)

    try:
        edge_model = litert_torch.convert(model, sample_inputs)
        edge_model.export(OUTPUT_MODEL)

        print("Conversion to tflite completed!")
    except Exception as e:
        print(f"Error during conversion: {e}!")

    metadata = {
        "all_words": all_words,
        "tags": tags
    }

    with open(OUTPUT_METADATA, "w", encoding="utf-8") as file:
        json.dump(metadata, file, ensure_ascii=False, indent=4)
    
    print("Export to json completed!")
    print("Conversion was successfull!")

if __name__ == "__main__":
    convert_model()
