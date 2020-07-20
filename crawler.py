import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# >>> 클라이언트에서 단어 input 연결 필요
word = ""
word = "生活"

# 통합사전에서 찾은 결과를 바탕으로 의미 수집
url = "https://dict.naver.com/search.nhn?dicQuery=" + word
data = requests.get(url)
soup = BeautifulSoup(data.text, "html.parser")

meaning = ""
try:
    meaning += soup.find('div', {'class': 'cn_dic_section search_result dic_cn_entry'}).find(
        'dl', {'class': 'dic_search_result'}).find('dd').find('em').next_sibling.strip()
    print(meaning)
except:
    print('중국어 단어를 찾지 못했습니다.')


# 중국어사전 상세 url 수집
entry_url = ""
try:
    entry_url += soup.find('div', {'class': 'cn_dic_section search_result dic_cn_entry'}).find(
        'dl', {'class': 'dic_search_result'}).find('dt').find('a')['href']
    print(entry_url)
except:
    print('결과를 찾을 수 없습니다.')


# 상세페이지에 있는 디테일 수집 - Selenium 활용
# HeadLess: 크롬 창이 뜨지 않고 동작하도록 명령
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')

driver = webdriver.Chrome(
    '/Users/YonnieK/Desktop/chromedriver', options=options)
driver.get(entry_url)

# >>> 여러가지 요소 한번에 불러올 수 있도록 수정 - 대기 명령은 한번만 하도록 바꿔야 하나?
try:
    pinyin = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.pronounce")))
    level = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.btn_toggle_square")))
    meanings = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.entry_mean_list")))
    print('병음: ' + pinyin.text + ', 레벨: ' +
          level.text + ', 뜻: ' + meanings.text)
finally:
    driver.quit()
