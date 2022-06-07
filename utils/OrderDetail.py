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
    
    def search_all(self, user_id):
        sql = "select id from order_detail where user_id = '{}'".format(user_id)
        result = self.db.select_all(sql)
        
        return result

        
    def search_last_id(self, user_id):
        sql = "select id from order_detail where user_id = '{}' order by id desc limit 1".format(user_id)
        orderDetail_id = self.db.select_one(sql)
        pk = orderDetail_id['id']
        
        return pk
        
    # db에 데이터 저장
    def insert_data(self, user_id):

        sql = "INSERT order_detail(user_id) values({})".format(user_id)

        self.db.execute(sql)

    # db 삭제
    def delete_data(self, pk, user_id):

        sql = "DELETE FROM order_detail WHERE id = '{}' and user_id = '{}'".format(pk, user_id)

        self.db.execute(sql)
