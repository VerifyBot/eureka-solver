"""
A utility to generate Eureka accounts.
More accounts means more unique daily challenges which results in more solutions the next day.
"""

import json
import random
import string
import sys
import time

import requests

headers = {
  'authority': 'eureka.org.il',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'accept': '*/*',
  'Referer': 'https://eureka.org.il/register',
}


def generate_usernames(n: int) -> list[str]:
  """Generates n usernames"""
  with open('hebrew_first_names.txt', encoding='utf-8') as f:
    first_names = f.read().splitlines()

  with open('hebrew_last_names.txt', encoding='utf-8') as f:
    last_names = f.read().splitlines()

  return [f'{random.choice(first_names)} {random.choice(last_names)} {random.randint(1000, 9999)}'
          for _ in range(n)]


def generate_passwords(n: int) -> list[str]:
  """Generates n passwords, this will also be used for the email password@gmail.com"""
  return [
    ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    for _ in range(n)
  ]


def generate_accounts(n: int):
  """"Generates n accounts"""
  print(f'👤 Attempting to generate {n} accounts')

  url = 'https://eureka.org.il/scripts/register_user.asp'

  usernames = generate_usernames(n)
  passwords = generate_passwords(n)

  accounts = []
  for username, password in zip(usernames, passwords):
    print(f'📬 Creating account: {username=} {password=}')

    resp = requests.post('https://eureka.org.il/scripts/register_user.asp', data={
      'nickname': username,
      'email': f'{password}@gmail.com',
      'password': password,
    }, headers=headers)

    if resp.status_code == 200:
      accounts.append({
        'nickname': username,
        'email': f'{password}@gmail.com',
        'password': password,
        'cookie': resp.cookies['EurekaLogin%5FUser']
      })
    else:
      print(f'⚠️ ({resp.status_code}) Failed to generate account for {username=}')
      print(resp.text)

    time.sleep(random.random() * 3)

  print(f'✅ Generated {len(accounts)} accounts')
  return accounts


if __name__ == '__main__':
  if len(sys.argv) > 1:
    accounts_to_generate = int(sys.argv[1])
  else:
    accounts_to_generate = int(input('How many accounts to generate? '))

  with open('../data/accounts.json', encoding='utf-8') as f:
    existing_acounts = json.load(f)

  new_accounts = generate_accounts(accounts_to_generate)

  accounts = [*existing_acounts, *new_accounts]

  with open('../data/accounts.json', 'w', encoding='utf-8') as f:
    json.dump(accounts, f, indent=2, ensure_ascii=False)

  print(f'💽 New accounts added to accounts.json (total {len(accounts)})')
  print('\n'.join(map(str, new_accounts)))
