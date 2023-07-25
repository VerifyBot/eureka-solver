import json
import random
import sys
import time

import endpoints

import curses

BEHAVE_NICELY = True  # whether to wait a some time between requests

def solve_all(cookies):
  stdscr = curses.initscr()
  stdscr.keypad(True)
  curses.noecho()
  curses.curs_set(0)
  stdscr.clear()

  if BEHAVE_NICELY:
    stdscr.addstr(0, 0, '⚠️ Note: You chose to behave nicely, so this might take a while.')
    stdscr.addstr(1, 0, f'\tPerhaps go grab a coffee? ☕️\n')
    stdscr.refresh()
    time.sleep(3)

  with open('../data/database.json', encoding='utf-8') as f:
    database = json.load(f)

  solved = 0



  for i, (q, it) in enumerate(database.items()):
    # some items in the database don't have solutions yet, or are missing a challenge_id (rare)
    if not it.get('challenge_id') or not it.get('answer'):
      continue

    # use curses to send this message in the same line
    msg = f'🎶 [{i / len(database):.2%}] Solving {q[::-1]} (+{it["points"]})'
    stdscr.addstr(2, 0, msg)
    stdscr.refresh()

    r = endpoints.submit_solution(cookies, it['challenge_id'], it['answer'])

    if BEHAVE_NICELY:
      time.sleep(1 + random.random())

    solved += 1

  curses.endwin()

  points = endpoints.get_points(cookies)
  print(f'🎸 Solved {solved} challenges, You now have {points} points!')


if __name__ == '__main__':
  # main account
  assert len(sys.argv) == 3, 'Usage: python answer.py <email> <password>'

  email = sys.argv[1]
  password = sys.argv[2]

  cookies = endpoints.login(email, password)

  solve_all(cookies)
