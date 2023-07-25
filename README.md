# 🐲 Eureka Bumper

> Automatically get points for solveing all Eureka questions.
> This will reward you with ~5120 points (336 questions solved).

*This is possible since you can answer all questions at once via API 
requests, and all of them were collected in this repo ([read more](#-how-is-it-possible)).*

<hr>

![https://i.imgur.com/fiQBK2a.png](https://i.imgur.com/fiQBK2a.png)

![https://i.imgur.com/tGsraKf.png](https://i.imgur.com/tGsraKf.png)

## 🛖 Background

**Eureka** ([eureka.org.il](https://eureka.org.il)) provides daily questions
that people can answer, based on their knowledge that can be expanded by
reading articles on their website.
<br><br>
Each daily question you answer provides you with points,
and when you reach a certain amount you climb to a new level:

![https://i.imgur.com/viUggem.png](https://i.imgur.com/ydJ7jMw.png)

The number of questions is limited (336), and therefore you can climb
just so much before reaching the barrier (5120 points for me), but that's
still good!

- **Note:** To get to `בוגר תואר שני`, you have to [add articles to the website](https://eureka.org.il/academy/).


## 🤔 How is it possible?

<p>There are <strong>3</strong> things that allow this to be possible:</p>

1. **The solution for yesterday's question is available the next day**, this allows the bot to collect all questions and
   their answers.
2. **Every account gets a different question**, so if you have multiple accounts, you can collect questions fast.
3. **There are only a few hundred questions**, so it's not a problem to collect all of them.

## 🎸 Usage

There is another *loophole* in the website, and it is that when
you solve a question, you provide the `challenge_id` and the `answer`,
so you can basically just send multiple requests for all the different
challenges (questions) and get all the possible points at once!

<p>Here is how to do it:</p>

```bash
pip install -r requirements.txt
cd app
python answer.py <email> <password> 
```

<hr>

<p>This repo contains all website questions, so no need to collect them.
If desired, cronjobs can be set up to automate daily script runs:</p>

```bash
# (Assuming the repository is in ~/dev/eureka)

# Daily :: Fetch today's and yesterday's challenge and save
10 8 * * * cd ~/dev/eureka/app && python store.py

# Daily :: Generate a new account
0 8 * * * cd ~/dev/eureka/tools && python generate_accounts.py 1

# Daily :: Update stats file
30 8 * * * cd ~/dev/eureka/data && python stats.py

# Daily :: Update stats sheets
35 8 * * * cd ~/dev/eureka/app && python sheets.py
```

## 📂 Scripts

### Getting points

#### 🎁 answer.py

Probably the highlight of this repository. Takes all questions and
answers from `database.json` and answers them on your main account.

```bash
python answer.py <email> <password>
```

<br/>
<hr/>

### Scraping related scripts

#### 🐍 generate_accounts.py

Generates random accounts and adds them to `data/accounts.json`.

```bash
python generate_accounts.py <amount>
```

#### 🐍 store.py

Stores today's question, and yesterday's answer from all accounts
in `data/database.json`.

```bash
python store.py
```

#### 🐍 stats.py

Stores how many questions, answers and accounts are in the database,
this is used for logging in a spreadsheet (see `sheets.py`).

```bash
python stats.py
```

#### 🐍 sheets.py

Logs stats about the collection process to a spreadsheet. This includes
info from `stats.json`, `database.json` and `could_do_ration.json`.

```bash
python sheets.py
```

