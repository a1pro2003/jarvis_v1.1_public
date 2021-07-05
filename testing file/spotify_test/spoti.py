import pandas as pd
from speech_recognition import Microphone, Recognizer, UnknownValueError
import speech_recognition
import spotipy as sp
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os

from pepper import stop_device, InvalidSearchError, get_album_uri, get_artist_uri, play_album, play_artist, get_track_uri, play_track

"""
To run this script, you must have a file in this directory called 'setup.txt'
In this file, enter all of the values of the required variables in the following format:
client_id=XXXXXXXX
client_secret=XXXXXXX
device_name=Jake's iMac
redirect_uri=https://example.com/callback/
username=jakeg135
scope=user-read-private user-read-playback-state user-modify-playback-state
"""

# Set variables from setup.txt
dir_path = os.path.dirname(os.path.realpath(__file__))
setup = pd.read_csv(dir_path + '/setup.txt', sep='=', index_col=0, squeeze=True, header=None)
client_id = setup['client_id']
client_secret = setup['client_secret']
device_name = setup['device_name']
redirect_uri = setup['redirect_uri']
scope = setup['scope']
username = setup['username']

# Connecting to the Spotify account
auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    username=username)
spotify = sp.Spotify(auth_manager=auth_manager)

# Selecting device to play from
devices = spotify.devices()
deviceID = None
for d in devices['devices']:
    d['name'] = d['name'].replace('’', '\'')
    if d['name'] == device_name:
        deviceID = d['id']
        break

# Setup microphone and speech recognizer
r = Recognizer()
# m = None
# input_mic = 'Scarlett 2i4 USB'  # Use whatever is your desired input
# for i, microphone_name in enumerate(Microphone.list_microphone_names()):
#     if microphone_name == input_mic:
#         m = Microphone(device_index=i)



while True:
    """
    Commands will be entered in the specific format explained here:
     - the first word will be one of: 'album', 'artist', 'play'
     - then the name of whatever item is wanted
    """


    command = input("Command: ")
    # try:
    #     with speech_recognition.Microphone() as source:
    #         r = Recognizer()
    #         r.adjust_for_ambient_noise(source, duration=1)
    #         r.dynamic_energy_threshold = True
    #         r.energy_threshold = 4600
    #         #r.pause_threshold = 0.8
    #         record = r.record(source, duration = 5) #works nice
    #         #audio = r.listen(source)
    #         command = r.recognize_google(record).lower()
    # except UnknownValueError:
    #     continue

    print(command)
    words = command.split()
    if len(words) <= 1 and words[0] != 'stop':
        print('Could not understand. Try again')
        continue

    name = ' '.join(words[1:])
    try:
        if words[0] == 'album':
            uri = get_album_uri(spotify=spotify, name=name)
            play_album(spotify=spotify, device_id=deviceID, uri=uri)
        elif words[0] == 'artist':
            uri = get_artist_uri(spotify=spotify, name=name)
            play_artist(spotify=spotify, device_id=deviceID, uri=uri)
        elif words[0] == 'play':
            uri = get_track_uri(spotify=spotify, name=name)
            play_track(spotify=spotify, device_id=deviceID, uri=uri)
        elif words[0] == 'stop':
            uri = get_track_uri(spotify=spotify, name=name)
            stop_device(spotify=spotify, device_id=deviceID, uri=uri)
        else:
            print('Specify either "album", "artist" or "play". Try Again')
    except InvalidSearchError:
        print('InvalidSearchError. Try Again')