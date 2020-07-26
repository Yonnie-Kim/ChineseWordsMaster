from pymongo import MongoClient
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbcwm


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/wordlist', methods=['GET'])
def listing():
    # 모든 document 찾기 & _id 값은 출력에서 제외하기
    result = list(db.wordlist.find({}, {'_id': 0}))
    # wordlist라는 키 값으로 영화정보 내려주기
    return jsonify({'result': 'success', 'wordlist': result})
# API 역할을 하는 부분


@app.route('/wordlist', methods=['POST'])
def save_word():
    # 1. 클라이언트로부터 데이터 입력받기
    word_receive = request.form['word_give']

    # 2. 받아온 단어로 나머지 정보 스크래핑 하기
    url = "https://dict.naver.com/search.nhn?dicQuery=" + word_receive
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")

    entry_url = soup.find('div', {'class': 'cn_dic_section search_result dic_cn_entry'}).find(
        'dl', {'class': 'dic_search_result'}).find('dt').find('a')['href']

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')

    driver = webdriver.Chrome(
        '/Users/YonnieK/Desktop/chromedriver', options=options)
    driver.get(entry_url)

    pinyin = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.pronounce"))).text
    level = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.btn_toggle_square"))).text
    meanings = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.entry_mean_list"))).text

    driver.quit()

    # 딕셔너리 구성
    word = {'hanzi': word_receive, 'url': entry_url,
            'pinyin': pinyin, 'level': level, 'meanings': meanings}
    print(word)
    # 3. mongoDB에 데이터를 넣기
    db.wordlist.insert_one(word)

    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
