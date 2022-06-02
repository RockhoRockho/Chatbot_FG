# 학습 데이터 초기화

class CartItem():
    
    def __init__(self, db):
        self.db = db
        
    
    def all_clear_train_data(self):
        # 기존 학습 데이터 삭제
        sql = '''
                delete from cart_item
            '''
        with self.db.cursor() as cursor:
            cursor.execute(sql)

        # auto increment 초기화
        sql = '''
        ALTER TABLE cart_item AUTO_INCREMENT=1;
        '''
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            
    # 전부찾기
    def search_all(self):
        sql = "select * from cart_item"
        result = self.db.select_all(sql)

        return result
    
    # count 찾기
    def search_count(self, product_id, option_id):
        
        sql = "select count from cart_item where product_id='{}' and option_id='{}' ".format(product_id, option_id)
        count = self.db.select_one(sql)
        
        return count 

    # db에 데이터 저장
    def insert_data(self, order_id, product_id, option_id, count):
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

        with self.db.cursor() as cursor:
            cursor.execute(sql)
            self.db.commit()

            
    # db 수정          
    def update_data(self, product_id, option_id, count):
        product_id_db = product_id
        option_id_db = option_id
        count_db = count

        sql = "UPDATE `cart_item` set `count` = '{}' where `product_id`='{}' and `option_id`='{}'".format(count_db.value, product_id_db.value, option_id_db.value)

        # 엑셀에서 불러온 cell에 데이터가 없는 경우, null 로 치환
        sql = sql.replace("'None'", "null")

        with self.db.cursor() as cursor:
            cursor.execute(sql)
            self.db.commit()
            
            
    def delete_data(self, product_id, user_id):
        product_id_db = product_id
        user_id_db = user_id

        sql = '''
            DELETE FROM `cart_item` WHERE `product_id` = %s AND `user_id` = %s
        ''' % (product_id_db.value, user_id_db.value)

        sql = sql.replace("'None'", "null")

        with self.db.cursor() as cursor:
            cursor.execute(sql)
            self.db.commit()