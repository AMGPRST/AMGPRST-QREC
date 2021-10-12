from time import sleep

from spotify import secrets
import requests


class Requester(object):
    def __init__(self):
        self.CLIENT_ID = secrets.CLIENT_ID
        self.CLIENT_SECRET = secrets.CLIENT_SECRET
        self.AUTH_URL = 'https://accounts.spotify.com/api/token'
        self.DELAY = 0.1

        auth_response = requests.post(self.AUTH_URL, {
            'grant_type': 'client_credentials',
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
        })

        self.headers = {'Authorization': 'Bearer {token}'.format(token=auth_response.json()['access_token'])}
        self.BASE_URL = 'https://api.spotify.com/v1/'

    def track_by_id(self, track_id):
        sleep(self.DELAY)
        req = requests.get(self.BASE_URL + 'tracks/' + track_id, headers=self.headers).json()
        title = track_id + ":::NOT FOUND"
        artist = track_id + ":::NOT FOUND"
        try:
            title = req['name']
            artist = req['artists'][0]['name']
        except KeyError:
            print("ERROR with API call:", req)

        return title, artist

    def id_by_track(self, title, artist):
        sleep(self.DELAY)
        req = requests.get(self.BASE_URL + 'search?query=track:'
                           + title.replace(" ", "+") + '+artist:'
                           + artist.replace(" ", "+") + '&type=track', headers=self.headers).json()
        return req['tracks']['items'][0]['id']
