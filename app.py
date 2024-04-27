from flask import Flask, make_response, request, jsonify, send_from_directory, render_template
from bs4 import BeautifulSoup
from translate import translate
import requests
import sqlite3
import re

connection = sqlite3.connect('wordbank.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS words (
id INTEGER PRIMARY KEY,
word TEXT NOT NULL,
transcription TEXT NOT NULL)''')

connection.commit()


app = Flask(__name__, static_folder='static')


def addLocal(word, phonetic):
    global cursor, connection

    cursor.execute('INSERT INTO words (word, transcription) VALUES (?, ?)', (word, phonetic))
    connection.commit()


def searchLocal(word):
    cursor.execute('SELECT transcription FROM words WHERE word = ? LIMIT 1', (word,))
    result = cursor.fetchall()

    if len(result) == 0:
        return None
    
    return word, result[0][0]

def searchDict(word):
    headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    }

    url = f'https://www.oxfordlearnersdictionaries.com/search/english/direct/?q={word}'
    resp = requests.get(url, headers=headers)

    if '.com/spellcheck' in resp.url:
        return None
    
    soup = BeautifulSoup(resp.text, "html.parser")
    soup = soup.find('div', class_='webtop')
    word = soup.find('h1', class_='headword').text
    phonetic = soup.find('div', class_='phons_br').find('span', class_="phon").text
    phonetic = re.sub('[(].[)]', '', phonetic[1:-1])
    print(f'RP trscr {phonetic}')
    phonetic = translate(phonetic)

    return word, phonetic

    

@app.route("/manifest.json")
def manifest():
    return send_from_directory('static', 'manifest.json')

@app.route("/logo.svg")
def logo():
    return send_from_directory('static', 'logo.svg')


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/search/<word>')
def search(word):
    word = word.lower()

    result = searchLocal(word)
    if result is not None:
        print(result)
        return jsonify(word=result[0], phonetic=result[1]), 200, {'content-type': 'application/json'}
    
    result = searchDict(word)
    if result is not None:
        addLocal(result[0], result[1])
        return jsonify(word=result[0], phonetic=result[1]), 200, {'content-type': 'application/json'}

    return '"resp":"None"', 404
    

app.run('localhost', 8080)

search('hummingbird')
connection.close()