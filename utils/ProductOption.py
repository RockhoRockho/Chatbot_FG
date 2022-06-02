# 학습 데이터 초기화

class ProductOption():
    
    def __init__(self, db):
        self.db = db
        
    
    def all_clear_train_data(self):
        # 기존 학습 데이터 삭제
        sql = '''
                delete from product_option
            '''
        with self.db.cursor() as cursor:
            cursor.execute(sql)

        # auto increment 초기화
        sql = '''
        ALTER TABLE product_option
        '''
        with self.db.cursor() as cursor:
            cursor.execute(sql)


    # db에 데이터 저장
    def insert_data(self, pk, option_id, product_id):
        pk_db = pk
        option_id_db = option_id
        product_id_db = product_id

        sql = '''
            INSERT product_option(id, option_id, product_id) 
            values('%s', '%s', '%s')
        ''' % (pk_db.value, option_id_db, product_id_db.value)

        # 엑셀에서 불러온 cell에 데이터가 없는 경우, null 로 치환
        sql = sql.replace("'None'", "null")

        with self.db.cursor() as cursor:
            cursor.execute(sql)
            self.db.commit()
