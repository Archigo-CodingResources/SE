from modules import delivery
from controllers.general import reload_db

def order_info(request):
    reload_db() #重新加載，確保DB資料最新
    args = request.args
    data = [{}]

    if 'oid' in args and 'did' not in args:  #如果請求中包含訂單ID但不包含外送員ID
        oid = int(args['oid']) #獲取訂單ID

        order_info = delivery.get_order_info()
        
    elif 'did' in args and 'oid' in args: #如果都包含
        oid = int(args['oid'])
        did = int(args['did'])

        order_info = delivery.get_own_order_info(did)
    
    if 'oid' in args:
        order_data = delivery.compose_order(order_info) #根據訂單信息組織訂單數據
        order_list, total = delivery.merge_order_info(order_data[oid - 1]) #合併訂單信息並計算總價
        
        data = [
            {
            "total": total,
            "data": order_list
        }
        ]

    return data

def own_order(request, session):
    reload_db()
    args = request.args

    if args:
        oid = int(args['oid'])
        order_info = delivery.get_order_info() 
        order_data = delivery.compose_order(order_info)
        
        # 遍歷訂單並確認配送員領取訂單
        for inner_order in order_data[oid - 1][:-1]:
            delivery.claim_order(session['id'], inner_order['cid'], inner_order['time'])

    # 獲取該配送員的所有訂單
    order = delivery.get_own_order(session['id'])
    data = delivery.compose_order(order)

    return data

def confirm_order(request, session):
    args = request.args
    cid = args['cid']
    time = args['time']
    total = args['total']
    rid = args['rid']

    delivery.confirm_order(session['id'], cid, time, total, rid)
