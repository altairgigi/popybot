# PoPyBot
A modular personal assistant written in Python. The bot is optimised to run even on limited hardware (like a Raspberry Pi Zero), is capable of managing memos, telling the weather and alerting when a memo expires, and offers unlimited feature possibilities thanks to its modular design.

## Installation
1) Clone the repository
```bash
git clone https://github.com/altairgigi/popybot.git
```

2) Install the dependencies
```bash
pip install -r requirements.txt
```

3) Make a .env file and paste your Telegram token and WeatherAPI key:
```
TELEGRAM_TOKEN="INSERT-YOUR-TOKEN"
WEATHER_API_KEY="INSERT-YOUR-API-KEY"
```
You can also add IP and port settings for your local model with:
```
FALLBACK_DEVICE_IP="INSERT-IP-HERE"
FALLBACK_DEVICE_PORT="INSERT-PORT-NUMBER-HERE"
FALLBACK_MODEL="INSERT-NAME-OF-THE-LOCAL-MODEL"
```

4) Train the bot with the `train.py` script and convert it to .ftlite with the `convert_to_litert.py` script you can find in the `nlp_training\` folder (more down below). 

5) Edit the `config.py` to your liking. The file contains all the templates for the bot's replies and regex functions. Those are set in Italian but you can change or translate them with a simple text editor, just keep the .py extension.

6) Start the bot with
```bash
#windows
pithon main.py
```
or
```bash
#linux/macos
pithon3 main.py
```
### How to train the model
Before using the bot and after every function you might add you need to train the bot. To do so you can use the `train.py` script. The file that will be used for training is the `intents.json` file: it's in Italian so you might need to translate it to your native language. You can either edit that one file or one of the intents .json, which are all kept int `intents_data\` folder. If you edit on the intent .json or add one you will need to recompile the main `intents.json` file with the `compile_dataset.json` script. It will automatically load and compile any .json in the folder so beware.

Once done so you can use the `train.py` script and train the bot, it will take around 5 minutes depending on your system power. After that you have to convert it to .tflite with the `convert_to_litert.py` script. You can also use the unconverted .pth model or convert it to .onnx with the `convert_to_onnx.py` script but in those cases you'll need to edit the code in `engine.py` too to make it work.

### How to add a function
Adding a function is pretty straight forward if you have everything set up properly: in order, you'll need to write the new function, link it to the `bot.py` file (to a command to a specific intent), and (if the function is to be linked to an intent) train the model.
```python
#example of function linked to command (@bot.message_handler())
@bot.message_handler(commands = ['new_command'])
def help(message):
    bot.send_message(message.chat.id, new_file.new_function())
```
```python
#example of function linked to intent recognition (process_message())
def process_message(message, user_text):
    user_intent = engine.decode_intent(user_text)

    if user_intent is not None and user_intent != config.INTENTS['?']:
    entities = engine.extract_entities(user_text, user_intent)

        if user_intent == config.INTENTS['greet']:
            bot.send_message(message.chat.id, greet.greet_user())

        #insert your new function here
        elif user_intent == config.INTENTS['new_intent']:
            bot.send_message(message.chat.id, new_file.new_function())
    
    #rest of the code, don't touch if you are not sure how it works
```

In order to train the bot for a new function you simply need to add a .json for the intent related to your function, compile the dataset and train the model, then convert it to .tflite (more on this up above).


## Requirements
You need `Python`, `pip`, `ffMpeg` and `FLAC` to be installed on your system.
It's advised to configure a virtual environment to better manage the project and the configuration.
All the main requirements are listed in the `requirements.txt` and can be installed all at once with:
```bash
pip install -r requirements.txt
```
Additional requirements are needed to train and convert the model needed by the bot:
* pytorch (2.12) to train and convert;
* onnxruntime (and onnxscripts) if you need to convert for ONNX;
* litert-torch and torchvision (0.27) to convert for LiteRT.

You can find the training and conversion scripts in the `/nlp_training` folder.
Pay attention to compatibility between dependencies as there might be conflicts.

## Features
* **Speech-to-Text (STT):** Accepts Telegram voice messages, converts them, and automatically transcribes them to text.
* **Smart Notifications:** Reminder management system with an asynchronous background alert system.
* **Live Weather:** Provides current weather conditions and temperatures for any city.
* **Modular Design:** Modular architecture with complete separation between modules logic, centralized configurations and databases.
* **NLP Intent Recognition:** Understands what you need thanks to a small-sized model tuned specifically for the bot's functions.
* **Local Fallback System:** When the bot is not enough it can forward your query to a local model through Ollama (provided you set it up).
* **Handy Commands:** You can easily show all the memo, clean the memo list, find help and show system status monitor.

## Tech-Stack
* **Language:** Python (tested on 3.11-3.12-3.13)
* **Package Manager:** pip (25.0,1)
* **Bot Framework:** `pyTelegramBotAPI`
* **NLP:** `PyTorch` (training) and `LiteRT` (execution)
* **Database:** SQLite3
* **Audio Processing:** `pydub` (with FFmpeg/FLAC)
* **Speech Recognition:** `SpeechRecognition`
* **System Monitor:** `psutil`
* **Environment Tools:** `python-dotenv`

## Credits
This project was made possible thanks to the following open-source technologies and services:

* **[LiteRT](https://github.com/google-ai-edge/litert)**
* **[NumPy](https://numpy.org/)**
* **[psutil](https://github.com/giampaolo/psutil)**
* **[Pydub](https://github.com/jiaaro/pydub)**
* **[pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)**
* **[PyTorch](https://pytorch.org/)**
* **[SpeechRecognition](https://github.com/Uberi/speech_recognition)**
* **[WeatherAPI](https://www.weatherapi.com/)**

## License
[GPL3.0](https://choosealicense.com/licenses/gpl-3.0/)