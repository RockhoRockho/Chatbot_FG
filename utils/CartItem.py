# 학습 데이터 초기화

class CartItem():
    
    def __init__(self, db):
        self.db = db
        
    
    def all_clear_train_data(db):
        # 기존 학습 데이터 삭제
        sql = '''
                delete from cart_item
            '''
        with db.cursor() as cursor:
            cursor.execute(sql)

        # auto increment 초기화
        sql = '''
        ALTER TABLE cart_item
        '''
        with db.cursor() as cursor:
            cursor.execute(sql)


    # db에 데이터 저장
    def insert_data(db, order_id, product_id, option_id, count):
        order_id_db = order_id
        product_id_db = product_id
        option_id_db = option_id
        count_db = count

        sql = '''
            INSERT cart_item(order_id, product_id, option_id, count) 
            values('%s', '%s', '%s', '%s')
        ''' % (order_id_db, product_id_db.value, option_id_db.value, count_db.value)

        # 엑셀에서 불러온 cell에 데이터가 없는 경우, null 로 치환
        sql = sql.replace("'None'", "null")

        with db.cursor() as cursor:
            cursor.execute(sql)
            db.commit()