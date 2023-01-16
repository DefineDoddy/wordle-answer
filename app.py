from flask import Flask, render_template
from requests_html import HTMLSession
from datetime import datetime
import os
import json


app = Flask(__name__)
FILE_PATH = '/tmp/data/'


def get_word():
    print("Finding wordle...")
    try:
        f = open(f"{FILE_PATH}word.txt", "r")
        text = f.read()
        f.close()
        date = datetime.strptime(text.split("=")[0], "%d/%m/%Y").date()
        if date >= datetime.now().date():
            word = text.split("=")[1]
            print("Stored wordle still valid")
            print("Found wordle from file: " + word)
            return text.split("=")[1]
    except:
        pass

    print("Requesting wordle...")

    try:
        session = HTMLSession(browser_args=["--no-sandbox"])
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1', 
        'referer': 'https://www.nytimes.com/', 'authority': 'pnytimes.chartbeat.net', 'Content-Type': 'application/json', 
        'accept': 'application/json', 'origin': 'https://www.nytimes.com'}
        r = session.get("https://www.nytimes.com/games/wordle/index.html", headers=headers)
        state = json.loads(r.html.render(script="localStorage.getItem('nyt-wordle-state')"))
        word = str.upper(state["solution"])

        print("Found wordle from request: " + word)

        if not os.path.exists(FILE_PATH):
            os.makedirs(FILE_PATH)

        f = open(f"{FILE_PATH}/word.txt", "w+")
        f.write(datetime.today().strftime("%d/%m/%Y") + "=" + word)
        f.close()

        print("Saved wordle to storage")
        return word
    except Exception as e:
        return '[ERROR] ' + str(e)
    return word

word = get_word()

@app.route('/')
def display_word():
    return render_template("index.html", word=word)


if __name__ == '__main__':
    app.run(debug=True)