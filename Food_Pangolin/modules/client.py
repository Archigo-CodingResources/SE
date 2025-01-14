from modules import init

cursor, conn = init.get_cursor()

def compose_order(form):
    #從表單提取食物的資料
    food_id = form.getlist("food_id")
    quantity = form.getlist("quantity")
    price = form.getlist("price")
    cid = form['cid']

    data = {}

    #將該資料存入data
    for i in range(min(len(food_id), len(quantity), len(price))):
        data[food_id[i]] = {
            "quantity": int(quantity[i]),
            "price": int(price[i])
            }

    return data, cid

def get_restaurant():
    sql = "SELECT * FROM `account` WHERE role = 0;" 
    cursor.execute(sql)
    return cursor.fetchall()

def get_menu(rid):
    #透過rid傳回參數對應menu資料
    sql = "SELECT * FROM `food` WHERE rid = %s;"
    param = (rid, )
    cursor.execute(sql, param)
    return cursor.fetchall()

def get_cart(cid):
     #透過rid傳回參數對應cart資料
    sql = "SELECT * FROM `cart` inner join `food` on food.food_id = cart.food_id where cid = %s"
    param = (cid, )
    cursor.execute(sql, param)
    return cursor.fetchall()

def get_item(cid, food_id):
    #透過rid傳回參數對應item資料
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

def get_order(cid):
    sql = "SELECT * FROM `the_order` inner join food on the_order.food_id = food.food_id where cid = %s;"
    param = (cid, )
    cursor.execute(sql, param)
    return cursor.fetchall()

def send_order(rid, food_id, quantity, cid, address, now):
    sql = "INSERT INTO `the_order`(`rid`, `food_id`, `cid`, `did`, `quantity`, `address`, `time`, `status`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    param = (rid, food_id, cid, None, quantity, address, now, 0, ) #訂單狀態默認為0
    cursor.execute(sql, param)
    conn.commit()
    return

def get_comment(rid):
    sql = "SELECT * FROM `comment` WHERE rid = %s;"
    param = (rid, )
    cursor.execute(sql, param)
    return cursor.fetchall()

def submit_feedback(rating, feedback, rid):   
    sql = "INSERT INTO `comment`(`rating`, `content`, `rid`) VALUES (%s, %s, %s)"
    param = (rating, feedback, rid,) 
    cursor.execute(sql, param)
    conn.commit()
    return
