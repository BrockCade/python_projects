#! /usr/bin/env python
import os
import requests
import hashlib
import base64
from urllib.parse import urlencode

#spotify api info
client_id = ('684e8eb73c5943aa8e1915a8ab5539ee')
client_secret = ('c0e85f33ee4640bc9b3c6da53d9e288f')
redirect_uri = 'http://localhost:3000'
#access_token = 'BQD5zhl7PXi8CTdB5yw07l_2A3Zmm9rnFe2E1mBeeH-EKb_rAgykp228o73BVnPLfy87loHX-OW1MAj9Bgb0xI9NzZ3X_DwApSBVRntlso2RumL0NIoPdFZkW6DRaMI5Tpwkm4te7CZlwVl0NrSjFVO3RVSW2sGdhy7d7NstQtdTmQug_qNxKewnyJ6YbmXJKtQ5pv25L_so_8A8hUDC60Y'
app_name = ('headunit')
user_name = ('cade')


class spotifyapi():
    def __init__(self):
        self.access_token = self.read('access_token:')
        #print('read access token ')
        pass
    def get_access_token(self,CLIENT_ID,REDIRECT_URI):
        # Specify required scopes
        SCOPE = 'user-modify-playback-state%20user-read-currently-playing%20playlist-read-private'  
        # Generate a random code verifie
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
            self.wright('access_token:',access_token)
            self.wright('refresh_token:',refresh_token)


        #refreash token
    def refresh(self):
        client_id = self.read('client_id:')
        client_secret = self.read('client_secret:')
        refresh_token = self.read('refresh_token:')
        # Base64 encode the client ID and client secret
        client_credentials = f"{client_id}:{client_secret}"
        client_credentials_b64 = base64.b64encode(client_credentials.encode()).decode()

        # Make a POST request to refresh the access token
        response = requests.post('https://accounts.spotify.com/api/token',
                                data = {"grant_type": "refresh_token","refresh_token": refresh_token,},
                                headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": f"Basic {client_credentials_b64}",})

        # Check if the request was successful
        if response.status_code == 200:
            # Extract the new access token from the response
            access_token = response.json()["access_token"]
            refresh_token = response.json()["refresh_token"]
            self.wright('access_token:',access_token)
            self.wright('refresh_token:',refresh_token)
            print('access token refreshed')
        else:
            print(response.json())
            print(f"Token refresh failed: {response.status_code}")

    def wright(self,name,value):
        filedata = open(r'/home/brockc09/headunit/python/spotify_api/credz.txt', 'r')
        data  = filedata.readlines()
        print(data)
        filedata.close()
        with open (r'/home/brockc09/headunit/python/spotify_api/credz.txt', 'w+') as myfile:
            if data != []:
                for line in data:
                    if name in line:
                        data.remove(line)
                        data.insert(0,name + "'" +value + "'" + '\n')
                myfile.writelines(data)
                        
                    
            else:
                print('empty')
                data.insert(0,name + "'" +value + "'" + '\n')
                myfile.writelines(data)
            
        print(data)
        myfile.close()
    def read(self,name):
        with open (r'/home/brockc09/headunit/python/spotify_api/credz.txt', 'rt') as myfile:
            for line in myfile:
                if name in line:
                    #print(line.split(':')[1].strip().replace("'", ""))
                    return line.split(':')[1].strip().replace("'", "")


    def get_playlists(self):
        response = requests.get('https://api.spotify.com/v1/me/playlists',
                    headers = {'Authorization': f'Bearer {self.access_token}'})
        lists = []
        for playlist in response.json()['items']:
            lists.append(playlist['name'])
        print(lists)
        return lists

    def pause(self):
        response = requests.put('https://api.spotify.com/v1/me/player/pause',
                    headers = {'Authorization': f'Bearer {self.access_token}'})
        
    def skip(self):
        response = requests.post('https://api.spotify.com/v1/me/player/next',
                    headers = {'Authorization': f'Bearer {self.access_token}'})
        
    def previous(self):
        response = requests.post('https://api.spotify.com/v1/me/player/previous',
                    headers = {'Authorization': f'Bearer {self.access_token}'})
        
    def play(self):
        response = requests.put('https://api.spotify.com/v1/me/player/play',
                    headers = {'Authorization': f'Bearer {self.access_token}'})

    def get_currently_playing(self):
        response = requests.get('https://api.spotify.com/v1/me/player/currently-playing',
                    headers = {'Authorization': f'Bearer {self.access_token}'})
        #print('acces token'+self.access_token)
        #print('respinse   ', response.json())
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
        
    def change_volume(new_volume):
        response = requests.put('https://api.spotify.com/v1/me/player/volume?volume_percent='+str(new_volume),
            headers = {'Authorization': f'Bearer {spotifyapi().access_token}'})

       

    def pick(self,name,args = None,args2 = None):
        try:
            method = getattr(spotifyapi(),name)
            method(args,args2)
        except:
            print('not 2')
        try:
            method = getattr(spotifyapi(),name)
            method(args)
        except:
            print('not 1')
        try:
            method = getattr(spotifyapi(),name)
            method()
        except:
            print('not 0')



#spotifyapi().pick('change_volume',80)

