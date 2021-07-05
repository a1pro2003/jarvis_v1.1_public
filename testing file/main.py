import speech_recognition as sr
import pyttsx3
import datetime
import random
import sys


listener = sr.Recognizer()
engine = pyttsx3.init()

#gets properties
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')

for voice in voices:
    print("Voice:")
    print(" - ID: %s" % voice.id)
    print(" - Name: %s" % voice.name)
    print(" - Languages: %s" % voice.languages)
    print(" - Gender: %s" % voice.gender)
    print(" - Age: %s" % voice.age)

#List of voices
en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enGB_GeorgeM"
en_voice_id2 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
en_voice_id3 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
en_voice_id4 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0"
engine.setProperty('voice', en_voice_id) # sets voice
engine.setProperty('rate', 150) # sets speech rate
engine.setProperty('volume', 1) # sets volume
engine.say("Goodmorning sir jarvis")
engine.runAndWait()


answers = ['Sir, i did no quite catch that', 'I didn\'t catch that' ]
q_time = ['what is the time', 'can i have the time', 'can you please tell me the time', 'what\'s the time']


def talk(text):
    engine.say(text)
    engine.runAndWait()


def run_alexa():
    command = take_command()
    print(command)

def get_audio():
    with sr.Microphone() as source:
        #listener.adjust_for_ambient_noise(source, duration=0.1)
        print('getting audio...')
        voice = listener.listen(source)
        command = ''
        try:
            command = listener.recognize_google(voice)
        except:
            pass
    
    return command.lower()
        
def listen():
    global listener
    WAKE = 'alexa'
    
    while True:
        #sets up listener
        text = get_audio()

        if text.count(WAKE) > 0:
            print(text.count(WAKE))
            talk("ready")
            text = get_audio()
            try:
                command = get_audio()


                if 'good morning' in command:
                    talk('good morning sir')


                if 'thank you' in command:
                    talk('you\'r welcome sir')


                if 'alexa' in command:
                    print('Alexa: ' + command)
                    take_command(command)
                    continue

                else:

                    print(answers[random.randint(0,1)])
                    pass


            except sr.UnknownValueError as e:
                listener = sr.Recognizer()
                print(e)
                continue
            

def take_command(command):
    for time in q_time:
        if time in command:
            time = datetime.datetime.now().strftime('%H:%M')
            talk('the time is ' + time)
            print('the time is ' + time)

    

listen()










