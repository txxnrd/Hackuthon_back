import sqlite3


def init(conn):
    cur.execute(f"CREATE TABLE users (username, password, agree, reward, plans, key_code);")#password - hash
    USERNAME, PW, AGREE, REWARD, PLANS, KEY_CODE = 0, 1, 2, 3, 4, 5
    conn.commit()
    
    cur.execute(f"CREATE TABLE place (place, info, category);")
    conn.commit()
    
    cur.execute(f"CREATE TABLE plan_data (place, date, people_num, specificity);")
    conn.commit()
    #cur.execute(f"CREATE TABLE personal_plans (plan_name, place, date, user_key_code);")
    #conn.commit()
    cur.execute(f"CREATE TABLE search_data (place, date, people_num, datas);")
    conn.commit()

conn = sqlite3.connect("database.db")
#cur.execute(f"DROP TABLE board")
cur = conn.cursor()
cur.execute(f"INSERT INTO users values ('asdf', 'test', '1011001', '0', 'None', 'aliwgheilh');")
#cur.execute(f"SELECT * FROM users WHERE username=asdf")
rows = cur.fetchall()
print(rows)
conn.commit()
cur.execute(f"UPDATE users SET plans='None' WHERE username='asdf'")
rows = cur.fetchall()
print(rows)
conn.commit()
conn.close()