import os.path
import random
import time

import endpoints
import json

from models import *

import typing

main_account_cookie = None


def get_accounts_cookies() -> list[typing.Optional[dict]]:
  """
  Returns the accounts stored in accounts.json and also the anonymous account (no cookies)
  """
  global main_account_cookie

  with open('../data/accounts.json', 'r', encoding='utf-8') as f:
    accounts = json.load(f)

  # 17.6.23 :: for could do ratio
  main_account_cookie = {'EurekaLogin%5FUser': accounts[0]['cookie']}

  return [None, *[{'EurekaLogin%5FUser': acc['cookie']} for acc in accounts]]


class Database:
  path = '../data/database.json'

  def __init__(self):
    self._db = {}

    if os.path.exists(self.path):
      with open(self.path, encoding='utf-8') as f:
        self._db = json.load(f)

    print(f'💽 Database loaded with {len(self._db)} solutions')

  def get_count(self):
    return len(self._db)

  def _save(self):
    """
    Save the database to the disk
    """
    with open(self.path, 'w', encoding='utf-8') as f:
      json.dump(self._db, f, ensure_ascii=False, indent=2)

  def _add(self, obj: dict):
    """
    Add a raw solution or challenge to the database
    """
    q = obj.pop('question')  # it will be the key

    new = q not in self._db
    # if the question is already in the database, possibly update new values
    if not new:
      print(f'🔃 Updating an existing question: {q=}')
      self._db[q].update(obj)
    else:
      print(f'📰 Adding a new question: {q=}')
      self._db[q] = obj

    self._save()

    return new

  def add_solution(self, solution: Solution):
    """
    Add a solution to the database
    """
    raw_solution: dict = dataclass_to_dict(solution)
    self._add(raw_solution)

  def add_challenge(self, challenge: Challenge):
    """
    Add a challenge to the database
    """
    raw_challenge: dict = dataclass_to_dict(challenge)
    return self._add(raw_challenge)


def routine_store_last_challenges():
  """
  Routine that will store the last challenges in the database
  """

  database = Database()

  count = database.get_count()

  cookies_batch = get_accounts_cookies()

  for cookies in cookies_batch:
    last_challenge = endpoints.last_challenge(cookies=cookies)

    # store the last challenge in the database
    database.add_solution(last_challenge)

    time.sleep(random.random() * 3)

  return database.get_count() - count


def route_store_daily_challenges():
  """
  Routine that will store the daily challenges in the database.
  It sounds pointless, but it doesn't look like they provide challenge_id
  in the last challenge, so we will have to save it today, and match it with
  the solution tomorrow.
  """

  database = Database()

  count = database.get_count()

  cookies_batch = get_accounts_cookies()

  for cookies in cookies_batch:
    daily_challenge = endpoints.daily_challenge(cookies=cookies)

    if not daily_challenge:  # already solved it
      continue

    # store the daily challenge in the database
    new = database.add_challenge(daily_challenge)

    # for could do ratio
    if cookies == main_account_cookie:
      # if its new, then could do, otherwise its new so couldnt.
      # get current
      do_ratio: list[bool] = []
      if os.path.exists('../data/could_do_ratio.json'):
        with open('../data/could_do_ratio.json') as f: do_ratio: list[bool] = json.load(f)
      do_ratio.append(not new)
      with open('../data/could_do_ratio.json', 'w') as f:
        json.dump(do_ratio, f, indent=2)

    time.sleep(random.random() * 3)

  return database.get_count() - count


if __name__ == '__main__':
  n_stored = routine_store_last_challenges()
  print(f'⭐ Stored {n_stored} previous challenges')

  n_stored = route_store_daily_challenges()
  print(f'⭐ Stored {n_stored} daily challenges')
