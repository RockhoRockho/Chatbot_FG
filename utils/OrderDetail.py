# 학습 데이터 초기화

class OrderDetail():
    
    def __init__(self, db):
        self.db = db
        
    
    def all_clear_train_data(self):
        # 기존 학습 데이터 삭제
        sql = '''
                delete from order_detail
            '''
        self.db.execute(sql)

        # auto increment 초기화
        sql = '''
        ALTER TABLE order_detail
        '''
        self.db.execute(sql)

    # db에 데이터 저장
    def insert_data(self, user_id):

        sql = "INSERT order_detail(user_id) values({})".format(user_id)

        # 엑셀에서 불러온 cell에 데이터가 없는 경우, null 로 치환
        sql = sql.replace("'None'", "null")

        self.db.execute(sql)
