import sys
import speech_recognition as sr
import pyttsx3 as tts
import random
from neuralintents import GenericAssistant
import pyjokes
import json

speaker = tts.init()
# speaker.setProperty('rate', 130)
en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enGB_GeorgeM"
speaker.setProperty('voice', en_voice_id) # sets voice
recognizer = sr.Recognizer()

def listen():

    try:
        with sr.Microphone() as mic:
            recognizer = sr.Recognizer()
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            input_audio = recognizer.listen(mic)
            audio = ''
            audio = recognizer.recognize_google(input_audio)

    except sr.UnknownValueError:
        recognizer = sr.Recognizer()
    return audio.lower()

def speak(audio):
    speaker.say(audio)
    speaker.runAndWait()


def main():
    while True:
        global assistant
        WAKE = 'alexa'
        try:
             input = listen()
             if (input.count(WAKE) > 0) or (WAKE in input):
                 print('yh?')
                #  input = input.replace(' ','')
                 input = input.replace('alexa ', '')
                 input = input.replace('task', '')
                 input = input.replace('number', '')
                 print("-" + input + "-")
                 continue


        except sr.UnknownValueError:
            recognizer = sr.Recognizer()

speak("Hello")
main()


