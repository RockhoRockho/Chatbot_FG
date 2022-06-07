# 학습 데이터 초기화

class CartItem():
    
    def __init__(self, db):
        self.db = db
        
    
    def all_clear_train_data(self):
        # 기존 학습 데이터 삭제
        sql = '''
                delete from cart_item
            '''
        self.db.execute(sql)


        # auto increment 초기화
        sql = '''
        ALTER TABLE cart_item AUTO_INCREMENT=1;
        '''
        self.db.execute(sql)

            
    # 전부찾기
    def search_all(self, user_id):
        sql = "select * from cart_item where user_id = '{}'".format(user_id)
        result = self.db.select_all(sql)

        return result
    
    # count 찾기
    def search_count(self, user_id, product_id, option_id):
        
        sql = "select count from cart_item where user_id='{}' and product_id='{}' and option_id='{}' ".format(user_id, product_id, option_id)
        countdic = self.db.select_one(sql)
        count = countdic['count']
        return count

    # db에 데이터 저장
    def insert_data(self, user_id, product_id, option_id, count):

        sql = '''
            INSERT cart_item(user_id, product_id, option_id, count) 
            values('%s', '%s', '%s', '%s')
        ''' % (user_id, product_id, option_id, count)

        self.db.execute(sql)


            
    # db 수정          
    def update_data(self, user_id, product_id, option_id, count):

        sql = "UPDATE `cart_item` set `count` = '{}' where `user_id`='{}' and `product_id`='{}' and `option_id`='{}'".format(count, user_id, product_id, option_id)

        self.db.execute(sql)

