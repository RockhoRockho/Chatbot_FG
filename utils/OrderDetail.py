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
        
    def search_last_id(self):
        sql = 'select id from order_detail order by id desc limit 1'
        orderDetail_id = self.db.select_one(sql)
        pk = orderDetail_id['id']
        
        return pk
    
    def search_id_from_orderNum(self, orderNum):
        sql = "select id from order_detail where user_id = '{}'".format(orderNum)
        orderDetail_id = self.db.select_one(sql)
        pk = orderDetail_id['id']
        
        return pk
        
    # db에 데이터 저장
    def insert_data(self, user_id):

        sql = "INSERT order_detail(user_id) values({})".format(user_id)

        self.db.execute(sql)

    # db 삭제
    def delete_data(self, order_id):

        sql = "DELETE FROM order_detail WHERE user_id = '{}'".format(order_id)

        self.db.execute(sql)
