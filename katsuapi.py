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
print(auth_response_data)
access_token = auth_response_data['access_token']

headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}

print("Access Token:")
print(access_token)