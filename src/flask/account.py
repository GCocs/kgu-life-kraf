from flask import Blueprint, render_template, request, session, jsonify
import bcrypt
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import smtp

# Blueprint
bp = Blueprint('account', __name__)

# .env파일 로드
load_dotenv()

# DB
db_uri = os.getenv('DB_URI')
client = MongoClient(db_uri)
db = client.kraf
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


# 비밀번호 해시
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

# 비밀번호 확인
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# 라우트
# 로그인 프로세스
@bp.route('/login-process', methods=['POST'])
def login_process():
    json_data = request.get_json()
    email = json_data.get('email')
    id = email.split('@')[0]
    checkPW = db.user.find_one({'email': id}, {'PW': 1, '_id': 0})
    PW = json_data.get('PW')
    if checkPW and check_password(PW, checkPW['PW']) :
        session['logined_email'] = id
        return jsonify({'success': True}), 200
    return jsonify({'success': False}), 200

# 로그아웃 프로세스
@bp.route('/logout', methods=['POST'])
def logout():
    session.pop('logined_email', None)
    return jsonify({'success': True}), 200

# 회원가입 프로세스
@bp.route('/signup-process', methods=['POST'])
def signup_process():
    json_data = request.get_json()
    email = json_data.get('email')
    PW = json_data.get('PW')
    hashed_PW = hash_password(PW)
    doc = {
        'email' : email,
        'PW' : hashed_PW
    }
    db.user.insert_one(doc)

    session['logined_email'] = email

    return jsonify({'success': True}), 200

# 이메일 중복 확인 프로세스
@bp.route('/check-duplication', methods=['POST'])
def checkDuplication():
    json_data = request.get_json()
    email = json_data.get('email')
    user = db.user.find_one({'email': email})
    if user :
        return jsonify({'success': False}), 200
    return jsonify({'success': True}), 200

# 회원가입 이메일 전송 프로세스
@bp.route('/send-email', methods=['POST'])
def sendEmail():
    json_data = request.get_json()
    email = json_data.get('email')
    smtp.send_email(email)
    return jsonify({'success': True}), 200

# 인증번호 확인 프로세스
@bp.route('/check-auth', methods=['POST'])
def checkAuth():
    json_data = request.get_json()
    email = json_data.get('email')
    authCode = json_data.get('authCode')
    if authCode == session.get('authCode') and email == session.get('email') :
        return jsonify({'success': True}), 200
    return jsonify({'success': False}), 200