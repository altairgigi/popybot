import json
import torch
from src.model import NeuralNet

def convert_model():
    INPUT_FILE = "data.pth"
    OUTPUT_MODEL = "model.onnx"
    OUTPUT_METADATA = "metadata.json"

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

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

    dummy = torch.randn(1, input_size).to(device)

    print("Starting conversion to ONNX...")
    
    torch.onnx.export(
        model,
        dummy,
        OUTPUT_MODEL,
        export_params=True,
        opset_version=18,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output']
    )

    print("Success!")
    print("Starting metadata export...")

    metadata = {
        "all_words": all_words,
        "tags": tags
    }

    with open(OUTPUT_METADATA, "w", encoding="utf-8") as file:
        json.dump(metadata, file, ensure_ascii=False, indent=4)
    
    print("Success!")
    print("Conversion completed!")

if __name__ == "__main__":
    convert_model()
