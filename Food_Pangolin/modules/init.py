import mysql.connector

def __init__():
    try:
        #連線DB
        conn = mysql.connector.connect(
            user = "se", 
            password = "!se_final", 
            host = "100.76.235.109", 
            port = 3306, 
            database = "final_se"
        )
        #建立執行SQL指令用之cursor,  設定傳回dictionary型態的查詢結果 [{'欄位名':值,  ...},  ...]
        cursor = conn.cursor(dictionary = True)
        return cursor

    except mysql.connector.Error as e: # mariadb.Error as e:
        print(e)
        print("Error connecting to DB")
        exit(1)


def check_account(Id, pwd):
    cursor = __init__()
    sql = "SELECT * FROM `account` WHERE id = %s and pwd = %s;"
    param = (Id, pwd, )
    cursor.execute(sql, param)
    return cursor.fetchall()
