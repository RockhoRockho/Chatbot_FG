# 학습 데이터 초기화

class OrderCancel():
    
    def __init__(self, db):
        self.db = db
        
    
    def all_clear_train_data(db):
        # 기존 학습 데이터 삭제
        sql = '''
                delete from order_detail
            '''
        with db.cursor() as cursor:
            cursor.execute(sql)

        # auto increment 초기화
        sql = '''
        ALTER TABLE order_detail
        '''
        with db.cursor() as cursor:
            cursor.execute(sql)


    # db에 데이터 저장
    def delete_data(db, product_id, order_id):
        pk_db = pk
        product_id_db = product_id
        order_id_db = order_id

        sql = '''
            DELETE FROM `order_item` WHERE `product_id` = product_id AND `order_id` = order_id

        ''' 

        # 엑셀에서 불러온 cell에 데이터가 없는 경우, null 로 치환
        sql = sql.replace("'None'", "null")

        with db.cursor() as cursor:
            cursor.execute(sql)
            db.commit()
