import requests
import json
import os

AUTH_URL = "https://kitsu.io/api/oauth/token"


auth_response = requests.post(AUTH_URL, {
  'grant_type': 'password',
  'username': os.environ.get('KITSU_EMAIL'),
  'password': os.environ.get('KITSU_PASSWORD'),
})

auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']

headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}

BASE_URL = "https://kitsu.io/api/edge/anime"
anime_id = input("Input an anime ID: ")
r = requests.get(BASE_URL + '/' + anime_id, headers = headers)

print(r.json())