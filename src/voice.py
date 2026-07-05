import speech_recognition
from pydub import AudioSegment
import config

def transcribe_audio(ogg_file_path):
    wav_file_path = ogg_file_path.replace(".ogg", ".wav")

    audio = AudioSegment.from_file(ogg_file_path, format="ogg")
    audio.export(wav_file_path, format="wav")

    recon = speech_recognition.Recognizer()

    with speech_recognition.AudioFile(wav_file_path) as source:
        audio_data = recon.record(source)

    try:
        text = recon.recognize_google(audio_data, language=config.LANGUAGE)
        return text
    
    except speech_recognition.UnknownValueError:
        raise speech_recognition.UnknownValueError
    
    except speech_recognition.RequestError:
        raise speech_recognition.RequestError
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return
