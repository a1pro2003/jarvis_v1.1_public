from logging import fatal
import pandas as pd
from speech_recognition import Microphone, Recognizer, UnknownValueError
import speech_recognition
import spotipy as sp
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os
from time import sleep
import subprocess
import psutil
from os.path import expanduser

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
home = expanduser("~")

# Connecting to the Spotify account
auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    username=username)
spotify = sp.Spotify(auth_manager=auth_manager)


def check_running_program(program):
    return str(program) in (p.name() for p in psutil.process_iter())

def start_spotify():
    #subprocess.run([home + '\\AppData\\Roaming\\Spotify\\Spotify.exe'])
    #subprocess.call(home + '\\AppData\\Roaming\\Spotify\\Spotify.exe') #for windows #C:\Users\Adrian\AppData\Roaming\Spotify
    subprocess.Popen(home + '\\AppData\\Roaming\\Spotify\\Spotify.exe')

if check_running_program('Spotify.exe') == False:
    start_spotify()
    sleep(8)

# Selecting device to play from
devices = spotify.devices()
for device in devices['devices']:
    print("Device: " + device['name'])
    print("ID: " + device['id'])

#change volume
spotify.volume(75)

class InvalidSearchError(Exception):
    pass

def get_album_uri(spotify: Spotify, name: str) -> str:
    """
    :param spotify: Spotify object to make the search from
    :param name: album name
    :return: Spotify uri of the desired album
    """

    # Replace all spaces in name with '+'
    original = name
    name = name.replace(' ', '+')

    results = spotify.search(q=name, limit=1, type='album')
    if not results['albums']['items']:
        raise InvalidSearchError(f'No album named "{original}"')
    album_uri = results['albums']['items'][0]['uri']
    return album_uri


def get_artist_uri(spotify: Spotify, name: str) -> str:
    """
    :param spotify: Spotify object to make the search from
    :param name: album name
    :return: Spotify uri of the desired artist
    """

    # Replace all spaces in name with '+'
    original = name
    name = name.replace(' ', '+')

    results = spotify.search(q=name, limit=1, type='artist')
    if not results['artists']['items']:
        raise InvalidSearchError(f'No artist named "{original}"')
    artist_uri = results['artists']['items'][0]['uri']
    print(results['artists']['items'][0]['name'])
    return artist_uri


def get_track_uri(spotify: Spotify, name: str) -> str:
    """
    :param spotify: Spotify object to make the search from
    :param name: track name
    :return: Spotify uri of the desired track
    """

    # Replace all spaces in name with '+'
    original = name
    name = name.replace(' ', '+')

    results = spotify.search(q=name, limit=1, type='track')
    if not results['tracks']['items']:
        raise InvalidSearchError(f'No track named "{original}"')
    track_uri = results['tracks']['items'][0]['uri']
    return track_uri


def play_album(spotify=None, device_id=None, uri=None):
    spotify.start_playback(device_id=device_id, context_uri=uri)


def play_artist(spotify=None, device_id=None, uri=None):
    spotify.start_playback(device_id=device_id, context_uri=uri)


def play_track(spotify=None, device_id=None, uri=None):
    spotify.start_playback(device_id=device_id, uris=[uri])


#lists all the users playlists
results = spotify.current_user_playlists(limit=50)
for i, item in enumerate(results['items']):
    print("%d %s" % (i, item['name']))
    print("%d %s" % (i, item['uri']))



saved_music = spotify.current_user_saved_tracks(limit = 50)

for item in saved_music['items']:
    track = item['track']
    print("%32.32s %s" % (track['artists'][0]['name'], track['name']))


#spotify.pause_playback(device_id = 'b806a37ebf5690d31761b7e3a3c3f5ad51c9c03c')

#sleep(3)

#spotify.start_playback(device_id = 'b806a37ebf5690d31761b7e3a3c3f5ad51c9c03c')



def main():
    done = False
    while not done:
        request = input("Request: ")
        request_split = request.split()

        try:
            information = spotify.current_playback()
            device_id = information['device']['id']
            volume = information['device']['volume_percent']
            shuffle_state = information['shuffle_state']
            playing_state = information['is_playing']
        except:
            pass


        #print(volume, device_id, shuffle_state, playing_state)

        print(request)
        if request[0] == 'start':
            spotify.start_playback(device_id = 'b806a37ebf5690d31761b7e3a3c3f5ad51c9c03c')
            done = True
        elif request[0] == 'stop':
            spotify.pause_playback(device_id = 'b806a37ebf5690d31761b7e3a3c3f5ad51c9c03c')
            done = True
        elif request[0] == 'volume':
            spotify.volume(int(request[1]))
        elif request[0] == 'next':
            spotify.next_track(device_id = 'b806a37ebf5690d31761b7e3a3c3f5ad51c9c03c')
            done = True
        elif request[0] == 'shuffle':
            spotify.shuffle(False, device_id = 'b806a37ebf5690d31761b7e3a3c3f5ad51c9c03c')
        # elif request[0] == 'trans':
        #     spotify.transfer_playback()
        elif request[0] == 'tracks':
            print(spotify.current_playback())
        elif request[0] == 'search':
            uris = spotify.search(request[1:], limit=1, type='track')
            print(uris)
            track = []
            num = 0
            #uri
            for uri in uris['tracks']['items']:
                track.append(uris['tracks']['items'][num]['uri'])
                print([uris['tracks']['items'][num]['uri']])
                num += 1
            
            num = 0
            contex = []
            #spotify contex_uri
            for uri in uris['tracks']['items']:
                contex.append(uris['tracks']['items'][num]['href'])
                print([uris['tracks']['items'][num]['href']])
                num += 1
            spotify.start_playback(device_id = 'b806a37ebf5690d31761b7e3a3c3f5ad51c9c03c', context_uri=contex)

        elif request[0] == 'current':
            print(spotify.current_playback())
        
        elif request[0:3] == 'change device to':
            print(spotify.devices())

main()