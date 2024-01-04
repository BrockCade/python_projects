#!/usr/bin/env python

# Import necessary libraries and modules
import os
import requests
import hashlib
import base64
from urllib.parse import urlencode
import subprocess

# Define an application name and user name
app_name = 'headunit'
user_name = 'cade'

# Define the Spotify API class
class spotifyapi:
    def __init__(self):
        self.access_token = self.read('access_token:')

    # Method to obtain the access token
    def get_access_token(self, CLIENT_ID, REDIRECT_URI):
        # Specify required scopes
        SCOPE = 'user-modify-playback-state%20user-read-currently-playing%20playlist-read-private'

        # Generate a random code verifier
        code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')

        # Hash the code verifier using SHA-256
        code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).rstrip(b'=').decode('utf-8')

        # Step 1: Build the authorization URL
        auth_params = {
            'client_id': CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'scope': SCOPE,
            'code_challenge_method': 'S256',
            'code_challenge': code_challenge,
        }
        auth_url = f'https://accounts.spotify.com/authorize?{urlencode(auth_params)}'

        print("Visit the following URL to authorize:")
        print(auth_url)

        # Step 2: User grants permission, and they are redirected back to your redirect URI with an authorization code
        authorization_code = input("Enter the authorization code: ")

        # Step 3: Exchange authorization code for tokens
        token_url = 'https://accounts.spotify.com/api/token'
        token_data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'code_verifier': code_verifier,  # Include the code verifier in the token request
        }
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()
        if token_response.status_code != 200:
            print(token_response)
            print(token_json)
        else:
            print(token_response)
            # Step 4: Get access token and refresh token
            access_token = token_json['access_token']
            refresh_token = token_json['refresh_token']
            print('access token ' + access_token)
            print('refresh token ' + refresh_token)
            self.wright('access_token:', access_token)
            self.wright('refresh_token:', refresh_token)

    # Method to refresh the access token
    def refresh(self):
        client_id = self.read('client_id:')
        client_secret = self.read('client_secret:')
        refresh_token = self.read('refresh_token:')
        
        # Base64 encode the client ID and client secret
        client_credentials = f"{client_id}:{client_secret}"
        client_credentials_b64 = base64.b64encode(client_credentials.encode()).decode()

        # Make a POST request to refresh the access token
        response = requests.post('https://accounts.spotify.com/api/token',
                                 data={"grant_type": "refresh_token", "refresh_token": refresh_token,},
                                 headers={"Content-Type": "application/x-www-form-urlencoded",
                                          "Authorization": f"Basic {client_credentials_b64}",})

        # Check if the request was successful
        if response.status_code == 200:
            # Extract the new access token from the response
            access_token = response.json()["access_token"]
            refresh_token = response.json()["refresh_token"]
            self.wright('access_token:', access_token)
            self.wright('refresh_token:', refresh_token)
            print('access token refreshed')
        else:
            print(response.json())
            print(f"Token refresh failed: {response.status_code}")

    # Method to write data to a file
    def wright(self, name, value):
        filedata = open(r'/home/brockc09/headunit/python/spotify_api/credz.txt', 'r')
        data = filedata.readlines()
        print(data)
        filedata.close()
        with open(r'/home/brockc09/headunit/python/spotify_api/credz.txt', 'w+') as myfile:
            if data != []:
                for line in data:
                    if name in line:
                        data.remove(line)
                        data.insert(0, name + "'" + value + "'" + '\n')
                myfile.writelines(data)
            else:
                print('empty')
                data.insert(0, name + "'" + value + "'" + '\n')
                myfile.writelines(data)
        print(data)
        myfile.close()

    # Method to read data from a file
    def read(self, name):
        with open(r'/home/brockc09/headunit/python/spotify_api/credz.txt', 'rt') as myfile:
            for line in myfile:
                if name in line:
                    return line.split(':')[1].strip().replace("'", "")

    # Method to get user's playlists
    def playlists(self):
        response = requests.get('https://api.spotify.com/v1/me/playlists',
                                headers={'Authorization': f'Bearer {self.access_token}'})
        
        playlist_items = {}
        #print(response.json())
        for playlist in response.json()['items']:
            playlist_items[playlist.get('name')] = playlist.get('id')
            
            
        #print(playlists)
        return playlist_items


    # Method to pause playback
    def pause(self):
        response = requests.put('https://api.spotify.com/v1/me/player/pause',
                                headers={'Authorization': f'Bearer {self.access_token}'})

    # Method to skip to the next track
    def skip(self):
        response = requests.post('https://api.spotify.com/v1/me/player/next',
                                 headers={'Authorization': f'Bearer {self.access_token}'})

    # Method to return to the previous track
    def previous(self):
        response = requests.post('https://api.spotify.com/v1/me/player/previous',
                                 headers={'Authorization': f'Bearer {self.access_token}'})

    # Method to start playback
    def play(self):
        response = requests.put('https://api.spotify.com/v1/me/player/play',
                                headers={'Authorization': f'Bearer {self.access_token}'})
        print(response)
        
    def shuffle(self,state):
        response = requests.put('https://api.spotify.com/v1/me/player/shuffle?state='+state,
                                headers={'Authorization': f'Bearer {self.access_token}'})
    
    def devices(self):
        response = requests.get('https://api.spotify.com/v1/me/player/devices',
                                headers={'Authorization': f'Bearer {self.access_token}'})
        devices = {}
        for device in response.json()['devices']:
            devices[device.get('name')] = device.get('id')
        print(devices)
        return devices

    # Method to get the currently playing song
    def get_currently_playing(self):
        response = requests.get('https://api.spotify.com/v1/me/player/currently-playing',
                                headers={'Authorization': f'Bearer {self.access_token}'})
        if response.status_code == 204:
            return 'nothing playing'
        elif response.status_code == 200:
            API_Data = response.json()
            return API_Data['item']['name']
        else:
            print('error')
            print(response.status_code)
            print(response.json())
            return 'error'
    def play_item(self,track,track_type):
        response = requests.put('https://api.spotify.com/v1/me/player/play',
                                headers={'Authorization': f'Bearer {self.access_token}'},
                                data = '{"context_uri": "spotify:' + track_type + ':' + track + '","offset": {"position": 0},"position_ms": 0}')
       
                                
        print(response)
    # Method to change the volume
    def change_volume(new_volume):
        response = requests.put('https://api.spotify.com/v1/me/player/volume?volume_percent=' + str(new_volume),
                                headers={'Authorization': f'Bearer {spotifyapi().access_token}'})
    def reset(self):
        subprocess.call('sudo /bin/python /home/brockc09/headunit/python/headunit_v2/input_controller.py', shell=True)
    # Method to call other Spotify API methods dynamically based on their name
