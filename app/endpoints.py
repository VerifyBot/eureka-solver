import re

import requests
from lxml import html

from models import Solution, Challenge

headers = {
  'authority': 'eureka.org.il',
  'Pragma': 'no-cache',
  'Referer': 'https://eureka.org.il/challenge/research/',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
  'X-requested-With': 'XMLHttpRequest',
}


### HTTP ENDPOINTS & PARSING ###
def login(email: str, password: str) -> dict:
  """
  Login to eureka.org.il and return the cookies
  :param email: Account email
  :param password: Account password
  :return: Identifying cookies
  """
  url = 'https://eureka.org.il/scripts/login_user.asp'
  params = {'email': email, 'password': password}

  resp = requests.get(url, params=params, headers=headers)

  return {'EurekaLogin%5FUser': resp.cookies.get_dict()['EurekaLogin%5FUser']}


def get_points(cookies) -> int:
  """
  Returns the user's points
  :param cookies: Account cookies
  :return: User's points
  """

  url = 'https://eureka.org.il/challenge'
  resp = requests.get(url, cookies=cookies, headers=headers)

  tree: html.HtmlElement = html.fromstring(resp.text)

  return int(tree.cssselect('.details div')[1].text_content().strip().split(' ')[1])


def last_challenge(cookies=None) -> Solution:
  """
  Returns the questions and the answer of the last challenge

  :param cookies: There is a unique challenge for each registered and a global one for anonymous.
  """
  url = 'https://eureka.org.il/scripts/print_ajax_area.asp?area=lastChallengeSlide'

  resp = requests.get(url, cookies=cookies, headers=headers)

  tree: html.HtmlElement = html.fromstring(resp.text)

  question = tree.cssselect('.TodayChallengeForm h1')[0].text_content().strip()
  points = re.search(r'(\d+)', tree.cssselect('.TodayChallengeForm h3')[0].text_content()).groups()[0]
  answer = tree.cssselect('.answerBox .finalAnswer')[0].text_content().strip()
  related_item = re.search(r'/(\d+)/', tree.cssselect('.itemBox a')[0].attrib['href']).groups()[0]

  return Solution(question=question, answer=answer,
                  points=int(points), related_item=int(related_item))


def daily_challenge(cookies=None) -> Challenge:
  """
  Returns the daily challenge (question, points and id)
  :param cookies: There is a unique challenge for each registered and a global one for anonymous.
  """
  url = 'https://eureka.org.il/scripts/print_ajax_area.asp?area=challengeSlide'

  resp = requests.get(url, cookies=cookies, headers=headers)

  tree: html.HtmlElement = html.fromstring(resp.text)

  question = tree.cssselect('.TodayChallengeForm h1')[0].text_content().strip()
  points = re.search(r'(\d+)', tree.cssselect('.TodayChallengeForm h3')[0].text_content()).groups()[0]

  try:
    challenge_id = tree.cssselect('#form_challenge_id')[0].attrib['value']
  except IndexError:
    return None  # solved already, ignore.

  return Challenge(question=question, points=int(points), challenge_id=int(challenge_id))


def submit_solution(cookies, challenge_id, answer):
  """
  Submit a solution for today's challenge
  :param cookies: The cookies of the account to submit the solution for
  """
  url = 'https://eureka.org.il/scripts/send_challenge_answer.asp'

  params = {'challenge_id': challenge_id, 'answer': answer}

  resp = requests.get(url, params=params, cookies=cookies, headers=headers)

  return resp.text


if __name__ == '__main__':
  print(daily_challenge())
  print(last_challenge())