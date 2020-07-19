import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
except:
    meaning += '중국어 단어를 찾지 못했습니다.'

print(meaning)


# 중국어사전 상세 url 수집
entry_url = ""
try:
    entry_url += soup.find('div', {'class': 'cn_dic_section search_result dic_cn_entry'}).find(
        'dl', {'class': 'dic_search_result'}).find('dt').find('a')['href']
except:
    entry_url += '결과를 찾을 수 없습니다.'
print(entry_url)


# 상세페이지에 있는 디테일 수집 - Selenium 활용
driver = webdriver.Chrome('/Users/YonnieK/Desktop/chromedriver')
driver.get(entry_url)

try:
    pinyin = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.pronounce")))
    print('병음: ' + pinyin.text)
finally:
    driver.quit()
