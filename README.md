# PoPyBot
A modular personal assistant written in Python. The bot is designed to run even on limited hardware, like a Raspberry Pi Zero, and is capable of managing memos, telling the weather and alerting when a memo expires.

## Installation
1) Clone the repository
2) Install the dependencies
```bash
pip install -r requirements.txt
```
3) Make a .env file and paste your Telegram token and WeatherAPI key:
```
TELEGRAM_TOKEN="INSERT-YOUR-TOKEN"
WEATHER_API_KEY="INSERT-YOUR-API-KEY"
```
4) Start the bot
```bash
pithon main.py
```

## Requirements
You need `Python`, `PIP`, `ffMpeg` and `FLAC` to be installed on your system.
It's advised to configure a virtual environment to better manage the project and the configuration.

## Features
* **Speech-to-Text (STT):** Accepts Telegram voice messages, converts them, and automatically transcribes them to text.
* **Smart Notifications:** Reminder management system with an asynchronous background alert system.
* **Live Weather:** Provides current weather conditions and temperatures for any city.
* **Modular Clean Code:** Modular architecture with complete separation between modules logic, centralized configurations and databases.

## Tech-Stack
* **Language:** Python (3.12)
* **Framework:** `pyTelegramBotAPI`
* **Database:** SQLite3
* **Audio Processing:** `pydub` & FFmpeg/FLAC
* **Speech Recognition:** `SpeechRecognition`
* **Environment Tools:** `python-dotenv`

## Credits
This project was made possible thanks to the following open-source technologies and services:

* **[pyTelegramBotAPI (Telebot)](https://github.com/eternnoir/pyTelegramBotAPI)**
* **[SpeechRecognition](https://github.com/Uberi/speech_recognition)**
* **[Pydub](https://github.com/jiaaro/pydub)**
* **[WeatherAPI](https://www.weatherapi.com/)**

## License
[GPL3.0](https://choosealicense.com/licenses/gpl-3.0/)