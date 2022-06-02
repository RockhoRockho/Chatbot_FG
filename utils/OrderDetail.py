# 학습 데이터 초기화

class OrderDetail():
    
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
    def insert_data(db, pk, user_id):
        pk_db = pk
        user_id_db = user_id

        sql = '''
            INSERT product_option(id, user_id) 
            values('%s', '%s')
        ''' % (pk_db.value, user_id_db)

        # 엑셀에서 불러온 cell에 데이터가 없는 경우, null 로 치환
        sql = sql.replace("'None'", "null")

        with db.cursor() as cursor:
            cursor.execute(sql)
            db.commit()
