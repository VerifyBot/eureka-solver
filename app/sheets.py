"""
This is used for logging scraping stats to a Google Sheet.
It is optional. To use it provide a creds.json file from Google Cloud Platform.
"""

import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials

with open('../data/stats.json', encoding='utf-8') as f:
  stats_js: list[dict] = json.load(f)

with open('../data/database.json', encoding='utf-8') as f:
  db_js: dict[str, dict] = json.load(f)

with open('../data/could_do_ratio.json') as f:
  could_do_ratio_js: list[bool] = json.load(f)


def do_auth(title):
  scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
           "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
  creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
  client = gspread.authorize(creds)

  sheet = client.open(title).sheet1
  return client, sheet


sauth = do_auth("Eureka")
ws = sauth[1]


### stats data: date, questions, answers, accounts ###
def get_data():
  # need to turn the list that contains dicts to a 2D list for gspread
  return [[*d.values()] for d in stats_js]


data = get_data()
ws.update(f'A2:D{1 + len(get_data())}', data)


### misc: max id, could solve ratio ###
def get_misc():
  return dict(
    max_id=max(db_js.values(), key=lambda d: d.get('challenge_id', -1))['challenge_id'],
    could_solve_ratio=round(sum(could_do_ratio_js) / len(could_do_ratio_js), 2)
  )


misc = get_misc()
ws.update_acell('G3', misc['max_id'])
ws.update_acell('G6', misc['could_solve_ratio'])
