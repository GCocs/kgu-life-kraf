import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# .env파일 로드
load_dotenv()

# DB
db_uri = os.getenv('DB_URI')
client = MongoClient(db_uri)
db = client.kraf
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

# 학과 공지사항 스크래핑 -> DB 저장
def insert_department_notice():
    data = requests.get('https://www.kyonggi.ac.kr/u_computer/selectBbsNttList.do?key=2161&bbsNo=565', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    notices = soup.select('tbody tr')

    for notice in notices:
        title = notice.select_one('td.p-subject a').get_text(strip=True)
        href = notice.select_one('td.p-subject a')['href'].lstrip('.')
        full_link = f"https://www.kyonggi.ac.kr/u_computer{href}"
        department = notice.select_one('td:nth-of-type(3)').get_text(strip=True)
        date = notice.select_one('td time').get_text(strip=True)
        doc = {
            'title' : title,
            'link' : full_link,
            'department' : department,
            'date' : date,
        }
        db.department_notice.insert_one(doc)

# 학사일정 스크래핑 -> DB 저장
def insert_academic_calendar() :
    data = requests.get('https://www.kyonggi.ac.kr/www/selectTnSchafsSchdulListUS.do?key=5695&sc1=10', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    #calendars = soup.select('#sc_con_202503 ul.info_box__list li.info_box__item')
    calendars = soup.select('.schedule_content__group .academic_info_box ul.info_box__list li.info_box__item')

    for calendar in calendars:
        date = calendar.select_one('div.info_box__date').get_text(strip=True)
        event = calendar.select_one('div.info_box__text p').get_text(strip=True)
        # 이미 동일한 데이터가 있는지 확인
        existing_event = db.academic_calendar.find_one({'date': date, 'event': event})

        # 데이터가 존재하지 않으면 삽입
        if not existing_event:
            doc = {'date': date, 'event': event}
            db.academic_calendar.insert_one(doc)


if __name__ == '__main__':
    db.department_notice.drop()
    insert_department_notice()
    db.academic_calendar.drop()
    insert_academic_calendar()