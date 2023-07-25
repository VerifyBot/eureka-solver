from dataclasses import dataclass

@dataclass
class Solution:
  """The last solution"""
  question: str
  answer: str
  points: int
  related_item: int

@dataclass
class Challenge:
  """The current challenge"""
  question: str
  points: int
  challenge_id: int

# a function that will take dataclass class as input a return a dict
def dataclass_to_dict(cls):
  return dict((field.name, getattr(cls, field.name)) for field in cls.__dataclass_fields__.values())

