import sqlite3
import json
import random
from Util.db import currentDB

def init():
    #password - hash
    currentDB.execute(f"CREATE TABLE users (username, password, agree, reward, plans, recent, key_code);", get_result=False)
    USERNAME, PW, AGREE, REWARD, PLANS, KEY_CODE = 0, 1, 2, 3, 4, 5

    
    currentDB.execute(f"CREATE TABLE places (place, info, category);", get_result=False)
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
        currentDB.execute(f"INSERT INTO places values ('{i}', '{json.dumps(temp)}', '한강공원');")
        conn.commit()
    
    currentDB.execute(f"CREATE TABLE plan_data (place, date, people_num, specificity);", get_result=False)
    for j in boundary:
        for i in range(20):
            currentDB.execute(f"INSERT INTO plan_data values ('{j}', 08{12+i}, {round(random.random()*6000)}, 'None');", get_result=False)
        for i in range(1, 10):
            currentDB.execute(f"INSERT INTO plan_data values ('{j}', 090{i}, {round(random.random()*2000)}, 'None');", get_result=False)
    
    #cur.execute(f"CREATE TABLE personal_plans (plan_name, place, date, user_key_code);")
    #conn.commit()
    currentDB.execute(f"CREATE TABLE search_data (place, date, people_num, datas);", get_result=False)

currentDB.connect()
init()
#test data - Need to delete
currentDB.execute(f"INSERT INTO users values ('HackKuthon2023', 'test', '1011001', '0', 'None', 'None','aliwgheilh');", get_result=False)

rows = currentDB.execute(f"SELECT * FROM users WHERE username='HackKuthon2023'")
print(rows)

currentDB.close()