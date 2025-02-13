from flask import Flask, render_template, request, session
from datetime import timedelta
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import account
import user_calendar

# .env파일 로드
load_dotenv()
sessionKey = os.getenv('SESSION_SECRET_KEY')

# app 설정
app = Flask(__name__, template_folder='../../templates', static_folder='../../static')
app.secret_key = sessionKey
app.permanent_session_lifetime = timedelta(minutes=10)
app.register_blueprint(account.bp)
app.register_blueprint(user_calendar.bp)

# db 설정
db_uri = os.getenv('DB_URI')
client = MongoClient(db_uri)
db = client.kraf
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

# TMAP API Key 가져오기
TMAP_API_key = os.getenv('TMAP_API_KEY')

# 로그인시 세션 HTML 전달
@app.context_processor
def inject_logined_email():
    return {'logined_email': session.get('logined_email')}

# 기존 라우트
# 홈 페이지 라우트
@app.route('/')
def home():
    noticeList = db.department_notice.find({}, {'_id': 0})
    return render_template('index.html', current_path=request.path, noticeList = noticeList)

# 지도 페이지 라우트
@app.route('/map')
def map_page():
    return render_template('map.html', current_path=request.path, TMAP_API_key = TMAP_API_key)

# 학교생활 페이지 라우트
@app.route('/school')
def school_page():
    return render_template('school.html', current_path=request.path)

# 로그인 페이지 라우트
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', current_path=request.path)

# 회원가입 페이지 라우트
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html', current_path=request.path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
