from modules import init

cursor, conn = init.get_cursor()

def get_menu(rid):
    sql = "SELECT * FROM `account` WHERE rid = %s;"
    param = (rid, )
    cursor.execute(sql, param)
    return cursor.fetchall()