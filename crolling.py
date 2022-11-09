from selenium import webdriver
import time
from openpyxl import Workbook
import pandas as pd
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

import warnings
warnings.filterwarnings('ignore')

wb = Workbook(write_only=True)
ws = wb.create_sheet()

options=webdriver.ChromeOptions()
driver = webdriver.Chrome('chromedriver', options=options)
driver.get("https://www.youtube.com/watch?v=abVcyLF3yjE")
driver.implicitly_wait(3)

time.sleep(1.5)

driver.execute_script("window.scrollTo(0,800)")
time.sleep(3)

#webpage 끝까지 스크롤
last_height = driver.execute_script("return document.documentElement.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(1.5)

    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(10)
#유튜브 팝업 닫기
try:
    driver.find_element(By.CSS_SELECTOR,"#main > div > ytd-button-renderer").click()
except:
    pass

#대댓글 버튼 누르기

try:
    buttons = driver.find_element(By.CSS_SELECTOR, "#more-replies > a")

    for button in buttons:
        button.send_keys(Keys.ENTER)
        time.sleep(1.5)
        button.click()
    time.sleep(1)
except:
    print("More replies are don't exist")


#댓글 가져오기
html_source = driver.page_source
soup = BeautifulSoup(html_source, 'html.parser')

id_list = soup.select("div#header-author > h3 > #author-text > span")
comment_list = soup.select("yt-formatted-string#content-text")

id_final = []
comment_final = []

for i in range(len(comment_list)):
    temp_id = id_list[i].text
    temp_id = temp_id.replace('\n', '')
    temp_id = temp_id.replace('\t', '')
    temp_id = temp_id.replace('    ', '')
    id_final.append(temp_id) # 댓글 작성자

    temp_comment = comment_list[i].text
    temp_comment = temp_comment.replace('\n', '')
    temp_comment = temp_comment.replace('\t', '')
    temp_comment = temp_comment.replace('    ', '')
    comment_final.append(temp_comment) # 댓글 내용
    
#댓글 저장하기
pd_data = {"댓글 내용" : comment_final}
youtube_pd = pd.DataFrame(pd_data)

youtube_pd.to_excel('result.xlsx')

