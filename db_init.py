import sqlite3
import json
import random

def init(conn):
    cur = conn.cursor()
    cur.execute(f"CREATE TABLE users (username, password, agree, reward, plans, recent, key_code);")#password - hash
    USERNAME, PW, AGREE, REWARD, PLANS, KEY_CODE = 0, 1, 2, 3, 4, 5
    conn.commit()
    
    cur.execute(f"CREATE TABLE places (place, info, category);")
    conn.commit()
    boundary = {
    "강서" : [350, 450], 
    "광나루" : [5000,  6000],
    "난지" : [3000, 4000],
    "뚝섬" : [3000, 4000],
    "망원" : [2000, 3000],
    "반포" : [4000, 5000],
    "양화" : [3000, 4000],
    "여의도" : [4500, 5500],
    "이촌" : [3000, 4000],
    "잠실": [3500, 4500],
    "잠원" : [2500, 3500]
    }
    
    for i in boundary:
        temp = {}
        for j in range(2):
            temp[f'{j}'] = str(boundary[i][j])
        #print(temp)
        cur.execute(f"INSERT INTO places values ('{i}', '{json.dumps(temp)}', '한강공원');")
        conn.commit()
    
    cur.execute(f"CREATE TABLE plan_data (place, date, people_num, specificity);")
    conn.commit()
    for j in boundary:
        for i in range(20):
            cur.execute(f"INSERT INTO plan_data values ('{j}', 08{12+i}, {round(random.random()*6000)}, 'None');")
            conn.commit()
        for i in range(1, 10):
            cur.execute(f"INSERT INTO plan_data values ('{j}', 090{i}, {round(random.random()*2000)}, 'None');")
            conn.commit()
    #cur.execute(f"CREATE TABLE personal_plans (plan_name, place, date, user_key_code);")
    #conn.commit()
    cur.execute(f"CREATE TABLE search_data (place, date, people_num, datas);")
    conn.commit()

conn = sqlite3.connect("database.db")
init(conn)
#cur.execute(f"DROP TABLE board")
cur = conn.cursor()
cur.execute(f"INSERT INTO users values ('HackKuthon2023', 'test', '1011001', '0', 'None', 'None','aliwgheilh');")
cur.execute(f"SELECT * FROM users WHERE username='HackKuthon2023'")
rows = cur.fetchall()
print(rows)
conn.commit()
cur.execute(f"UPDATE users SET plans='None' WHERE username='HackKuthon2023'")
rows = cur.fetchall()
print(rows)
conn.commit()
conn.close()