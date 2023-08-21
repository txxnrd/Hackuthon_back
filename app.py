from flask import Flask, render_template, request, make_response, redirect, session
import sqlite3
import json

import Util.load_excel_data as excel
from Util.load_excel_data import location_to_filename
import Util.load_weather_data as weather
import Util.calculate_day as cd

app = Flask(__name__)
app.secret_key = 'asdf0192958'

TODAY = [8, 21]

@app.route('/')
def index():
    return "success"
    #return render_template('./index.html')

@app.route('/mypage')
def mypage():
    
    return render_template('/mypage.html')

def is_available_date(month, day):
    if cd.bitween_days([int(month), int(day)], TODAY)<31:
        return True
    return False

def is_available_place(place):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM places WHERE place='{location_to_filename[place]}'")
    res = cur.fetchall()
    if len(res[0])==0:
        return False
    return True

@app.route('/get_place_data', methods=["GET"])
def get_place_data():
    args = request.args
    date = args['date'].split(' ')[0].split('-')
    month = int(date[1])
    day = int(date[2])
    place = args['place']
    
    res = {
        'user_data': {},
        'past_data': {},
        'past_color': {},
        'status': None
    }
    res['weather'] = weather.get_weather_data(location_to_filename[place], cd.bitween_days([month, day], TODAY) , 1)
    
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    for i in range(-3, 3):
        sum = 0
        temp1, temp2 = cd.add_day(month, day, i)
        for j in range(2020, 2023):
            data = excel.get_data(j, temp1, temp2, place)
            if data[2] == None:
                continue
            sum += data[2]
        sum //= 3
        past_min = 100000000
        if sum<past_min:
            past_min = sum
            
        if i == 0:
            cur.execute(f"SELECT info FROM places WHERE place='{location_to_filename[place]}'")
            rows = cur.fetchall()
            past_blue = False
            boundary = json.loads(rows[0][0])
            print(boundary)
            if sum < int(boundary['0']):
                res['status'] = 'happy'
                res['past_color'][i]=0xFF7190FF
                
            elif sum < int(boundary['1']):
                res['status'] = 'soso'
                res['past_color'][i]=0xFFFFFB90
            else: 
                res['status'] = 'mad'
                past_blue = True

        res['past_data'][i] = sum
        
        cur.execute(f"SELECT people_num FROM plan_data WHERE place='{location_to_filename[place]}' AND date="+"{}{:02d}".format(temp1, temp2))
        rows = cur.fetchall()[0][0]
        print(rows)
        res['user_data'][i] = rows
        past_min = 100000000
        if rows<past_min:
            past_min = rows
    if past_blue:
        for i in range(-3, 3):
            if past_min == res['past_data'][i]:
                res['past_color'][i]=0xFF7190FF
            else:
                res['past_color'][i]=0xFF9D9D9D
        res['past_color'][i]=0xFFFFD7D7
    else:
        for i in range(-3, 3):
            if i==0: continue
            res['past_color'][i]=0xFF9D9D9D
    
    conn.close()
    return json.dumps(res)

@app.route('/add', methods=["GET"])
def add_plan(): #username, session(cookie), date, place, plan_name
    args = request.args
    #username = request.form.get("username", "Default username")
    username = 'HackKuthon2023'
    #sess = request.form.get("session", "Default password")
    
    #if session['user:'+username] != username:
    #    return "fail!"
    
    #user
    
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT * FROM users WHERE username='{username}'")
        rows = cur.fetchall()
    except:
        return "Invalid username!"
    
    date = args['date'].split(' ')[0].split('-')
    month = date[1]
    day = date[2]
    date = month+day
    if not is_available_date(month, day):
        return "date over!"
    
    place = args['place']
    if not is_available_place(place):#겹치는 장소면 덮어씌우기
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
    plans[date+place] = addition
    cur.execute(f"UPDATE users SET plans='{json.dumps(plans)}' WHERE username='{username}'")
    conn.commit()
    conn.close()
    print(plans)
    
    return json.dumps(plans)

@app.route('/modify', methods=["GET"])
def modify_plan():
    
    resp = make_response(redirect("/mypage"))
    return resp

@app.route('/list')
def get_place_list():
    username = request.args["username"]
    username = 'HackKuthon2023'
    
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(f"SELECT plans FROM users WHERE username='{username}'")
    rows = json.loads(cur.fetchall()[0][0])
    
    temp = []
    for i in rows:
        temp.append([rows[i]['date'], rows[i]['place']])  
    temp.sort()
    res = {}
    
    temp1, temp2 = int(temp[0][0][:2]), int(temp[0][0][2:4])
    if temp1==TODAY[0] and temp2==TODAY[1]:
        cur.execute(f"SELECT recent FROM users WHERE username='{username}'")
        recent = cur.fetchall()[0][0]
        for i in recent:
            exist = False
            date = "{:02d}{:02d}".format(TODAY[0], TODAY[1])
            if date in recent[i]['date']:
                exist = True
                break
        if not exist:
            place = temp[0][1]
            recent[date] = place
            addition = {'place':place, 'date':date}
            recent[date+place] = addition
            cur.execute(f"UPDATE users SET plans='{json.dumps(recent)}' WHERE username='{username}'")
            conn.commit()        
    
    for i in range(len(temp)):
        sum = 0
        temp1, temp2 = int(temp[i][0][:2]), int(temp[i][0][2:4])
        for j in range(2020, 2023):
            data = excel.get_data(j, temp1, temp2, temp[i][1])
            if data[2] == None:
                continue
            sum += data[2]
        sum //= 3
        
        res[i] = {'month': temp1, 'day': temp2, 'place':temp[i][1]}
        cur.execute(f"SELECT info FROM places WHERE place='{location_to_filename[temp[i][1]]}'")
        rows = cur.fetchall()
        boundary = json.loads(rows[0][0])
        print(boundary)
        if sum < int(boundary['0']):
            res[i]['status'] = 'happy'
        elif sum < int(boundary['1']):
            res[i]['status'] = 'soso'
        else: 
            res[i]['status'] = 'mad'
            
    conn.close()
    return res


@app.route('/recent', methods=["GET"])
def get_recent():
    username = request.args["username"]
    username = 'HackKuthon2023'
    
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(f"SELECT recent FROM users WHERE username='{username}'")
    try:
        rows = json.loads(cur.fetchall()[0][0])
    except:
        return "fail!"
    temp = []
    for i in rows:
        temp.append([rows[i]['date'], rows[i]['place']])  
    temp.sort()
    res = {}
    temp = temp[::-1]
    for i in range(temp):
        temp1, temp2 = int(temp[i][0][:2]), int(temp[i][0][2:4])
        if temp1==TODAY[0] and temp2==TODAY[1]:
            today = True
        else:
            today = False
        res[i] = {'month': temp1, 'day': temp2, 'place':f'{temp[i][1]}', 'today':f"{today}"}
            
    conn.close()
    return json.dumps(res)


@app.route('/verify_place', methods=["GET"])
def verify_place():
    args = request.args
    username = args['username']
    place = args['place']
    username = 'HackKuthon2023'
    
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(f"SELECT plans FROM users WHERE username='{username}'")
    rows = json.loads(cur.fetchall()[0][0])
    
    temp = []
    for i in rows:
        temp.append([rows[i]['date'], rows[i]['place']])  
    temp.sort()
    if temp[0][0] == "{:02d}{:02d}".format(TODAY[0], TODAY[1]):
        if temp[0][1] == location_to_filename[place]:
            cur.execute(f"SELECT reward FROM users WHERE username='{username}'")
            reward = cur.fetchall()[0][0]
            cur.execute(f"UPDATE users SET reward={reward+200}")
            #f"UPDATE users SET plans='{json.dumps(plans)}' WHERE username='{username}'"
            conn.commit()
            return True
    
    conn.close()
    return False

@app.route('/reward', methods=["GET"])
def get_reward():
    args = request.args
    username = args['username']
    username = 'HackKuthon2023'
    
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(f"SELECT reward FROM users WHERE username='{username}'")
    res = cur.fetchall()[0][0]
    
    return {"reward": res}

if __name__ == '__main__':
    app.run(host="0.0.0.0")