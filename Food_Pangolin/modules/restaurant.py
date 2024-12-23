from modules import init

cursor, conn = init.get_cursor()

def get_menu(rid):
    sql = "SELECT * FROM `food` WHERE rid = %s;"
    param = (rid, )
    cursor.execute(sql, param)
    return cursor.fetchall()

def remove_item(rid, food_id):
    sql = "DELETE FROM `food` WHERE food_id = %s and rid = %s"
    param = (food_id, rid)
    cursor.execute(sql, param)
    conn.commit()
    return

def get_order(rid):
    sql = "SELECT * FROM `cart` inner join `food` on cart.food_id = food.food_id where food.rid = %s"
    param = (rid, )
    cursor.execute(sql, param)
    return cursor.fetchall()

def add_item(name, description, price, rid):
    sql = "INSERT INTO food (name, description, price, rid) VALUES (%s, %s, %s, %s);"
    param = (name, description, price, rid)
    cursor.execute(sql, param)
    conn.commit()
    return

def get_food(food_id):
    sql = "SELECT * FROM food where food_id = %s"
    param = (food_id,)
    cursor.execute(sql, param)
    return cursor.fetchall()

def fix_item(name, description, price, food_id):
    sql = "UPDATE food SET name=%s, description=%s, price=%s WHERE food_id=%s;"
    param = (name, description, price, food_id)
    cursor.execute(sql, param)
    conn.commit()
    return
