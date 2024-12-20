from modules import init

cursor, conn = init.get_cursor()

def get_restaurant():
    sql = "SELECT * FROM `account` WHERE role = 0;"
    cursor.execute(sql)
    return cursor.fetchall()

def get_menu(rid):
    sql = "SELECT * FROM `account` WHERE rid = %s;"
    param = (rid, )
    cursor.execute(sql, param)
    return cursor.fetchall()