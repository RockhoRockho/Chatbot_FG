# 학습 데이터 초기화

class OrderItem():
    
    def __init__(self, db):
        self.db = db
        
    
    def all_clear_train_data(self):
        # 기존 학습 데이터 삭제
        sql = '''
                delete from order_item
            '''
        self.db.execute(sql)


        # auto increment 초기화
        sql = '''
        ALTER TABLE order_item AUTO_INCREMENT=1;
        '''
        self.db.execute(sql)

    # 전부찾기
    def search_all(self):
        sql = "select * from order_item"
        result = self.db.select_all(sql)

        return result
    
    # db에 데이터 저장
    def insert_data(self, order_id, product_id, option_id, count):

        sql = '''
            INSERT order_item(order_id, product_id, option_id, count) 
            values('%s', '%s', '%s', '%s')
        ''' % (order_id, product_id, option_id, count)

        # 엑셀에서 불러온 cell에 데이터가 없는 경우, null 로 치환
        sql = sql.replace("'None'", "null")

        self.db.execute(sql)

            
    
            
    def delete_data(self, product_id, order_id):
        product_id_db = product_id
        order_id_db = order_id

        sql = '''
            DELETE FROM `order_item` WHERE `product_id` = %s AND `order_id` = %s
        ''' % (product_id_db.value, order_id_db.value)

        sql = sql.replace("'None'", "null")

        self.db.execute(sql)
