from flask import Flask, render_template, request, make_response, redirect, session
import sqlite3
import json

import Util.load_excel_data as excel
import Util.load_weather_data as weather

app = Flask(__name__)
app.secret_key = 'asdf0192958'

def get_data(board):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {board}")
    rows = cur.fetchall()
    return rows, conn, cur
    
def close_db(conn):
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return "success"
    #return render_template('./index.html')

@app.route('/mypage')
def mypage():
    
    return render_template('/mypage.html')

def is_available_date(date):
    pass
    return True

@app.route('/get_place_data', methods=["POST"])
def get_place_data():
    month = request.form.get("month", "1")
    day = request.form.get("day", "1")
    place = request.form.get("place", "default_place")
    
    sum = 0
    for i in range(2020, 2023):
        sum += excel.get_data(i, month, day, place)
    sum //= 3

@app.route('/add', methods=["POST"])
def add_plan(): #username, session(cookie), date, place, plan_name
    username = request.form.get("username", "Default username")
    sess = request.form.get("session", "Default password")
    
    #if session['user:'+username] != username:
    #    return "fail!"
    
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT * FROM users WHERE username='{username}'")
        rows = cur.fetchall()
    except:
        return "Invalid username!"
    
    date = request.form.get("date", "Default date")
    if not is_available_date(date):
        return "date over!"
    
    place = request.form.get("place", "Default place")
    if not is_available_date(date):#겹치는 장소면 덮어씌우기
        return "Invalid place!"
    
    #if new
    
    USERNAME, PW, AGREE, REWARD, PLANS, KEY_CODE = 0, 1, 2, 3, 4, 5
    print(rows[0][PLANS])
    try:
        plans = json.loads(rows[0][PLANS])
    except:
        plans = {}
    
    print(plans)
    
    for i in plans:
        if date in plans[i]['date']:
            plans[i]['place'] = place
            cur.execute(f"UPDATE users SET plans='{json.dumps(plans)}' WHERE username='{username}'")
            conn.commit()
            conn.close()
            print(plans)
            return json.dumps(plans)
    
    addition = {'place':place, 'date':date}
    plans[place+date] = addition
    cur.execute(f"UPDATE users SET plans='{json.dumps(plans)}' WHERE username='{username}'")
    conn.commit()
    conn.close()
    print(plans)
    
    return json.dumps(plans)

@app.route('/modify', methods=["POST"])
def modify_plan():
    
    resp = make_response(redirect("/mypage"))
    return resp

@app.route('/list')
def get_place_list():
    
    pass

if __name__ == '__main__':
    app.run(host="0.0.0.0")