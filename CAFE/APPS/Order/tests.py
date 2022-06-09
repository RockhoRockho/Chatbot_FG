from django.test import TestCase
import pymysql 

def ProductOption():
    

    db = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            db=DB_NAME,
            charset='utf8'
        )

    sql = ''' 
    SELECT * from product_option
    '''
    with db.cursor() as cur:
        cur.execute(sql)
        option = cur.fetchall()

    return option

def OrderDetail():
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
        SELECT * from order_detail
    '''

    with db.cursor() as cur:
        cur.execute(sql)
        order_detail = cur.fetchall()

    return order_detail

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

def Product():
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
        SELECT * from product_cafe
    '''

    with db.cursor() as cur:
        cur.execute(sql)
        product = cur.fetchall()

    return product