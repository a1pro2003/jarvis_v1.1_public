import speech_recognition as sr
import pyttsx3 as tts

speaker = tts.init()
# speaker.setProperty('rate', 130)
en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enGB_GeorgeM"
speaker.setProperty('voice', en_voice_id) # sets voice
recognizer = sr.Recognizer()

def speak(audio): #DONE
    speaker.say(audio)
    speaker.runAndWait()