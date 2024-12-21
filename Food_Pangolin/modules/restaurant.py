from modules import init

cursor, conn = init.get_cursor()

def compose_order(cart_data):
    grouped_by_cid = {}
    for item in cart_data:
        cid = item['cid']
        if cid not in grouped_by_cid:
            grouped_by_cid[cid] = []
        grouped_by_cid[cid].append(item)

    grouped_by_cid = list(grouped_by_cid.values())
    
    for items in grouped_by_cid:
        total = 0
        for item in items:
            total += item['price'] * item['quantity']
        items.append(total)

    return grouped_by_cid

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
