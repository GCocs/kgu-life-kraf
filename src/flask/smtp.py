import smtplib
from dotenv import load_dotenv
import os
from email.mime.text import MIMEText
import random
from flask import session

# 이메일 전송 함수
def send_email(email) : 
    full_email = email + '@kyonggi.ac.kr'
    authCode = str(random.randint(100000, 999999))

    session.pop('authCode', None)
    session.pop('email', None)

    #.env파일 로드
    load_dotenv()
    SMTP_Password = os.getenv('SMTP_PASSWORD')

    #SMTP
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()

    smtp.login('ysh0621000@gmail.com', SMTP_Password)

    # 메일 내용 입력
    msg = MIMEText('<h1 style="font-family:Open Sans,Helvetica,Arial,sans serif;font-size:32px;font-weight:700;line-height:130%;color:#0e1318;letter-spacing:-0.5px;margin:0 0 16px;text-align:left;text-align:start">KRAF에 회원가입</h1><p style="color:#0e1318;font-family:Open Sans,Helvetica,Arial,sans serif;font-weight:400;line-height:160%;font-size:14px;margin:0;text-align:left;text-align:start">KRAF에 처음 방문하신 것을 환영합니다. 10 분 내에 아래 코드를 입력하여 회원가입하세요.</p><div style="color:#0e1318;font-family:Open Sans,Helvetica,Arial,sans serif;font-size:24px;font-weight:700;letter-spacing:-0.3px;line-height:130%;"><br><p style="margin-top:0;margin-bottom:0">'+ authCode +'</p></div>', 'html')
    msg['Subject'] = 'KRAF 코드는 '+ authCode + '입니다.'

    smtp.sendmail('ysh0621000@gmail.com', full_email, msg.as_string())
    
    session['authCode'] = authCode
    session['email'] = email

    smtp.quit()