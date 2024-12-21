from modules import init

cursor, conn = init.get_cursor()

def get_restaurant():
    sql = "SELECT * FROM `account` WHERE role = 0;"
    cursor.execute(sql)
    return cursor.fetchall()

def get_menu(rid):
    sql = "SELECT * FROM `food` WHERE rid = %s;"
    param = (rid, )
    cursor.execute(sql, param)
    return cursor.fetchall()

def get_cart(cid):
    sql = "SELECT * FROM `cart` inner join `food` on food.food_id = cart.food_id where cid = %s"
    param = (cid, )
    cursor.execute(sql, param)
    return cursor.fetchall()

def get_item(cid, food_id):
    sql = "SELECT * FROM `cart` WHERE cid = %s and food_id = %s;"
    param = (cid, food_id, )
    cursor.execute(sql, param)
    return cursor.fetchall()

def add_cart(food_id, quantity, cid):
    sql = "INSERT INTO `cart`(`food_id`, `quantity`, `cid`) VALUES (%s, %s ,%s)"
    param = (food_id, quantity, cid)
    cursor.execute(sql, param)
    conn.commit()
    return

def remove_cart(food_id, cid):
    sql = "DELETE FROM `cart` WHERE food_id = %s and cid = %s"
    param = (food_id, cid)
    cursor.execute(sql, param)
    conn.commit()
    return

def clear_cart(cid):
    sql = "DELETE FROM `cart` WHERE cid = %s"
    param = (cid, )
    cursor.execute(sql, param)
    conn.commit()
    return

def update_cart(food_id, quantity, cid):
    sql = "UPDATE `cart` SET `quantity`= %s WHERE cid = %s and food_id = %s"
    param = (quantity, cid, food_id,)
    cursor.execute(sql, param)
    conn.commit()
    return