import os
import json

stats = []
if os.path.exists('stats.json'):
    with open('stats.json') as f:
        stats = json.load(f)

from datetime import datetime

with open('database.json', encoding='utf-8') as f:
    db = json.load(f)

with open('accounts.json', encoding='utf-8') as f:
    accs = json.load(f)

stat = {}

stat['date'] = str(datetime.now().date())

for i, s in enumerate(stats):
    if s['date'] == stat['date']:
        stats.pop(i)

stat['questions'] = len(db)
stat['answers'] = len(list(filter(lambda it: it.get('answer'), db.values())))
stat['accounts'] = len(accs)

stats.append(stat)

with open('stats.json', 'w') as f:
    json.dump(stats, f, indent=2)

print(f'📝 Stats written for {stat["date"]}:\n', stat)