from modules import init

cursor, conn = init.get_cursor()

def compose_order(cart_data):
    grouped_by_cid_time = {}

    # 按 (cid, time) 分组
    for item in cart_data:
        key = (item['cid'], item['time'])  # 使用 (cid, time) 作为分组键
        if key not in grouped_by_cid_time:
            grouped_by_cid_time[key] = []
        grouped_by_cid_time[key].append(item)

    # 将分组结果转换为列表
    grouped_by_cid_time = list(grouped_by_cid_time.values())
    
    for items in grouped_by_cid_time:
        total = 0
        for item in items:
            total += item['quantity'] * item['price']

        items.append(total)

    return grouped_by_cid_time


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
    sql = "SELECT * FROM `the_order` inner join `food` on the_order.food_id = food.food_id WHERE the_order.rid = %s"
    param = (rid, )
    cursor.execute(sql, param)
    return cursor.fetchall()

def update_order(cid, time, rid):
    sql = "UPDATE `the_order` SET `status`= 2 WHERE cid = %s and time = %s and rid = %s"
    param = (cid, time, rid)
    cursor.execute(sql, param)
    conn.commit()
    return

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

def get_restaurant_comment(rid):
    sql = "SELECT * FROM comment where rid = %s"
    param = (rid,)
    cursor.execute(sql, param)
    return cursor.fetchall()
    

