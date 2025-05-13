import speech_recognition as sr
from difflib import SequenceMatcher

def evaluate_pronunciation(audio_path, target_word):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    
    try:
        spoken_text = recognizer.recognize_google(audio).lower()
        similarity = SequenceMatcher(None, spoken_text, target_word).ratio()
        return {
            'status': 'success',
            'spoken': spoken_text,
            'target': target_word,
            'accuracy': round(similarity * 100, 2)
        }
    except sr.UnknownValueError:
        return {'status': 'error', 'message': 'Could not understand audio'}
    except sr.RequestError:
        return {'status': 'error', 'message': 'API unavailable'}