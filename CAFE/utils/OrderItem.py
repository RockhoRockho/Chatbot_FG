import pymysql 

def OrderItem():
    # DB 가져오기
    DB_HOST = "localhost"
    DB_USER = "myuser118"
    DB_PASSWORD = "1234"
    DB_NAME = "mydb118"

    db = None

    db = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            db=DB_NAME,
            charset='utf8'
        )

    sql = ''' 
    SELECT * from order_item
    '''

    with db.cursor() as cur:
        cur.execute(sql)
        order_item = cur.fetchall()

    return order_item