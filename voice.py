import os
import speech_recognition
from pydub import AudioSegment

def transcribe_audio(ogg_file_path):
    wav_file_path = ogg_file_path.replace(".ogg", ".wav")

    audio = AudioSegment.from_file(ogg_file_path, format="ogg")
    audio.export(wav_file_path, format="wav")

    recon = speech_recognition.Recognizer()

    with speech_recognition.AudioFile(wav_file_path) as source:
        audio_data = recon.record(source)

    if os.path.exists(wav_file_path):
        os.remove(wav_file_path)

    try:
        text = recon.recognize_google(audio_data, language="it_IT")
        return text
    
    except speech_recognition.UnknownValueError:
        return "Non ho capito cosa hai detto, puoi ripetere?"
    
    except speech_recognition.RequestError:
        return "In questo momento ho problemi a connettermi al servizio trascrizione vocale."
    
    except Exception as e:
        return f"C'è stato un errore inaspettato: {e}"
