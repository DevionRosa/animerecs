import requests
import json
import os
import sqlalchemy as db
import pandas as pd
from pandas import json_normalize

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

anime_table = r.json()
if 'data' in anime_table:
  anime_attributes = anime_table['data'].get('attributes', {})
  anime_id_val = anime_table['data'].get('id')
  anime_df = json_normalize(anime_attributes)
  anime_df['id'] = anime_id_val
  for column in anime_df.columns:
    if anime_df[column].apply(lambda x: isinstance(x, (dict, list))).any():
      anime_df[column] = anime_df[column].astype(str)

engine = db.create_engine('sqlite:///data_base_name.db')
anime_df.to_sql('anime_df', con=engine, if_exists='replace', index=False)
with engine.connect() as connection:
  query_result = connection.execute(db.text("SELECT * FROM anime_df;")).fetchall()
  print(pd.DataFrame(query_result, columns=anime_df.columns))
