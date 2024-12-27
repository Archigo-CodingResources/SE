import mysql.connector

_cursor = None
_conn = None

def __init__():
    global _cursor, _conn #宣告全域變數 _cursor 和 _conn，這樣其他函數可以使用這兩個變數來操作資料庫
    try:
        #連線DB
        conn = mysql.connector.connect(
            user = "se", 
            password = "!se_final", 
            host = "100.76.235.109", 
            port = 3306, 
            database = "final_se"
        )
            #建立執行SQL指令用之cursor,設定傳回dictionary型態的查詢結果 [{'欄位名':值,  ...},  ...]
        cursor = conn.cursor(dictionary = True)
        _cursor = cursor
        _conn = conn

    except mysql.connector.Error as e: # mariadb.Error as e: #如果連線失敗，捕捉錯誤並顯示錯誤訊息
        print(e)
        print("Error connecting to DB")
        exit(1)

def get_cursor():
    return _cursor, _conn


def check_account(mail):
    cursor, conn = get_cursor() 
    sql = "SELECT * FROM `account` WHERE email = %s"
    param = (mail, )
    cursor.execute(sql, param)
    return cursor.fetchall() #返回查詢結果，使用fetchall()方法獲取所有匹配的結果

def register(name, mail, pwd, address, role):
    cursor, conn = get_cursor()
    sql = "INSERT INTO `account`(`name`, `email`, `pwd`, `address`, `role`) VALUES (%s, %s, %s, %s, %s)"
    param = (name, mail, pwd, address, role)
    cursor.execute(sql, param)
    conn.commit()
    return

def get_summary(role):
    cursor, conn = get_cursor()
    sql = "SELECT * FROM `account` where role = %s"
    param = (role, )
    cursor.execute(sql, param)
    return cursor.fetchall() #返回查詢結果，所有符合角色條件的帳號資料


__init__()
