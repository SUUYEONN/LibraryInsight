# 2022년 10월 기준 실행 가능한 코드입니다. 
import selenium
from selenium import webdriver as wd
import time
import pandas as pd
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import openpyxl
from bs4 import BeautifulSoup

# 가상 브라우저 사용을 위한 설정
options = wd.ChromeOptions()
options.add_argument("no-sandbox")  # 보안 설정을 비활성화
options.add_argument("--disable-dev-shm-usage")  # 공유 메모리 사용 비활성화
options.add_argument("user-agent={Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36}")  # 사용자 에이전트 설정

# 크롬 드라이버 실행
driver = wd.Chrome(executable_path='chromedriver', options=options)
driver.maximize_window() 
driver.implicitly_wait(1) 

# 사용자 로그인 정보
id = '자신의 에브리타임 id 입력'
pw = '자신의 에브리타임 pw 입력'

# 에브리타임 로그인 페이지로 이동
URL = 'https://everytime.kr/login'
driver.get(URL)

# 아이디와 비밀번호 입력
driver.find_element(By.NAME, 'userid').send_keys(id)
driver.find_element(By.NAME, 'password').send_keys(pw)

# 2~6초 중 랜덤으로 선택하여 쉬기 (사람처럼 보이기 위해)
rand_value = random.uniform(2, 6)
time.sleep(rand_value)

# 로그인 버튼 클릭
driver.find_element(By.XPATH, '//*[@id="container"]/form/p[3]/input').click()
rand_value = random.uniform(2, 6)
time.sleep(rand_value)

# 검색할 텍스트 입력
query_txt = '검색할 텍스트 입력'

# 검색창 요소 선택 및 접근
rand_value = random.unㄴiform(2, 6)
time.sleep(rand_value)
element = driver.find_element(By.XPATH, '//*[@id="container"]/div[3]/form/input')
rand_value = random.uniform(2, 6)
time.sleep(rand_value)

# 검색어 입력
element.send_keys(query_txt)
rand_value = random.uniform(2, 6)
time.sleep(rand_value)

# 검색어 전송
element.send_keys(Keys.ENTER)
rand_value = random.uniform(2, 6)
time.sleep(rand_value)

###########
# 게시글 크롤링
# 데이터를 엑셀파일로 저장하기 위해 엑셀파일 생성
excel_file = openpyxl.Workbook()
excel_sheet = excel_file.active

# 다음 페이지로 이동하여 데이터를 수집하는 함수
def next_page():
    # 현재 페이지의 HTML 소스를 가져와서 BeautifulSoup로 파싱
    res = driver.page_source
    soup = BeautifulSoup(res, "html.parser")
    
    # 게시글의 날짜, 좋아요 수, 내용 가져오기
    data_date = soup.select('#container > div.wrap.articles > article > a > time')
    data_like = soup.select('.vote')
    data_text = soup.select('#container > div.wrap.articles > article > a > p')

    # 데이터를 엑셀 시트에 추가
    for date, like, text in zip(data_date, data_like, data_text):
        excel_sheet.append([date.get_text(), like.get_text(), text.get_text()])

    # 다음 페이지로 이동
    rand_value = random.uniform(2, 6)
    time.sleep(rand_value)
    driver.find_element(By.CLASS_NAME, 'next').click()
    rand_value = random.uniform(2, 6)
    time.sleep(rand_value)

# 첫 페이지 대기
rand_value = random.uniform(2, 6)
time.sleep(rand_value)

# 여러 페이지에 걸쳐 데이터를 수집
# next_page를 n번 반복
for page_roof in range(50):
    rand_value = random.uniform(2, 6)
    time.sleep(rand_value)
    next_page()

# 수집된 데이터를 엑셀 파일에 저장
file_name = f'everytime_crawling_{query_txt}.xlsx'
file_path = os.path.join('data', file_name)  # data 폴더에 저장
excel_file.save(file_path)
excel_file.close()

# 브라우저 종료
driver.quit()
