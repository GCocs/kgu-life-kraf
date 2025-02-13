from datetime import datetime
from flask import Blueprint, request, session, jsonify
from datetime import timedelta
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import account

# Blueprint
bp = Blueprint('calendar', __name__)

# .env파일 로드
load_dotenv()

# DB
db_uri = os.getenv('DB_URI')
client = MongoClient(db_uri)
db = client.kraf
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

# 날짜 포맷 변환 함수
def convert_date_format(date_str):
    # 날짜 앞부분에 불필요한 문자가 있을 수 있음, 제거
    date_str = date_str.split('(')[0].strip()  # 괄호 제거
    try:
        return datetime.strptime(date_str, "%Y.%m.%d").strftime("%Y-%m-%d")
    except ValueError:
        return date_str  # 형식이 맞지 않으면 원래의 날짜를 그대로 반환   
    

# 형식 변환 함수
def convert_event_format(date_range, event_name):
    if '~' in date_range:
        start_date, end_date = date_range.split('~')
        start_date = convert_date_format(start_date.strip())
        end_date = convert_date_format(end_date.strip())
    else:
        start_date = convert_date_format(date_range.strip())
        end_date = start_date  # 시작일과 종료일이 같은 경우

    return {
        "title": event_name,
        "start": start_date,
        "end": end_date
    }


# 로그인 인증
@bp.route('/check-session', methods=['GET'])
def check_session():
    id = session.get('logined_email')
    if id == None :
        return jsonify({'success': False}), 200
    return jsonify({'success': True}), 200

# 캘린더 가져오기
@bp.route('/calendar', methods=['GET'])
def get_calendar():
    # 학사일정과 사용자 일정 데이터 가져오기
    calendar_data = list(db.academic_calendar.find({}, {'_id': 0}))

    user = session.get('logined_email')
    academic_events = []
    user_events = list(db.user_calendar.find({"user" : user}, {'_id': 0, 'user': 0})) 

    # 학사일정 처리
    for item in calendar_data:
        date_range = item["date"]
        event_name = item["event"]
        academic_events.append(convert_event_format(date_range, event_name))

    # 결과를 각 변수에 담아서 리턴
    return jsonify({
        'result': 'success', 
        'academic_calendar': academic_events,
        'user_calendar': user_events
    })

# 사용자 일정 입력 > db 삽입
@bp.route('/calendar', methods=['POST'])
def add_event():
    title_receive = request.form['title_give']
    start_receive = request.form['start_give']
    end_receive = request.form['end_give']

    if not title_receive or not start_receive or not end_receive:
        return jsonify({'error': '모든 필드를 입력하세요'}), 400


    existing_event = db.user_calendar.find_one({'title': title_receive, 'start': start_receive, 'end': end_receive})

        # 데이터가 존재하지 않으면 삽입
    user = session.get('logined_email')

    if not existing_event:
        doc = {'title': title_receive, 'start': start_receive, 'end': end_receive, 'user': user}
        db.user_calendar.insert_one(doc)
        
    return jsonify({'result':'success','message': '일정이 추가되었습니다'}), 201