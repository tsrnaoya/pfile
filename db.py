import os, psycopg2, string, random, hashlib

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset =string.ascii_letters + string.digits
    salt = ''.join(random.choices(charset, k=30))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_password = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 1000).hex()
    return hashed_password
    
    
def insert_user(user_name, password):
    sql = 'INSERT INTO customer VALUES(default, %s, %s, %s)'
    
    salt = get_salt()
    hashed_password = get_hash(password, salt)

    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (user_name, hashed_password, salt))
        count = cursor.rowcount #更新件数を取得
        connection.commit()
        
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
        
    return count

def login(user_name, password):
    sql = 'SELECT hashed_password, salt FROM customer WHERE name = %s' #ユーザー名がに件取れる可能性があるから直すnmae=%sのとこ
    flg = False

    try :
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_name, ))
        user = cursor.fetchone()

        if user != None:
            salt = user[1]

            hashed_password = get_hash(password, salt)

            if hashed_password == user[0]:
                flg = True
    except psycopg2.DatabaseError:
        flg = False
    finally :
        cursor.close()
        connection.close()
        
    return flg

def select_all_shops():
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT id, name, company, price, stock FROM shops'
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def search_shops(key):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT id, name, company, price, stock FROM shops WHERE name LIKE %s'
    key = '%' + key + '%'
    cursor.execute(sql, (key,))
    rows = cursor.fetchall()
    return rows

def insert_shops(shops_name, company, price, stock):
    sql = 'INSERT INTO shops VALUES (default, %s, %s, %s, %s)'
    try :
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (shops_name, company, price, stock))
        count = cursor.rowcount # 更新内容を取得
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
    return count

def shop(id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'UPDATE shops SET stock = stock - 1 WHERE id=%s;'
    cursor.execute(sql,(id,))
    count = cursor.rowcount
    connection.commit()
    cursor.close()
    connection.close()
    return count

def shop_delete(id):
    connection = get_connection()
    connection.cursor()
    cursor = connection.cursor()
    sql = 'DELETE FROM shops WHERE id = %s'
    cursor.execute(sql,(id))
    count = cursor.rowcount
    connection.commit()
    cursor.close()
    connection.close()
    return count