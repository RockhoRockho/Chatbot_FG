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
    def search_all(self):
        sql = "select * from cart_item"
        result = self.db.select_all(sql)

        return result
    
    # count 찾기
    def search_count(self, product_id, option_id):
        
        sql = "select count from cart_item where product_id='{}' and option_id='{}' ".format(product_id, option_id)
        countdic = self.db.select_one(sql)
        count = countdic['count']
        return count

    # db에 데이터 저장
    def insert_data(self, product_id, option_id, count):

        sql = '''
            INSERT cart_item(product_id, option_id, count) 
            values('%s', '%s', '%s')
        ''' % (product_id, option_id, count)

        # 엑셀에서 불러온 cell에 데이터가 없는 경우, null 로 치환
        sql = sql.replace("'None'", "null")

        self.db.execute(sql)


            
    # db 수정          
    def update_data(self, product_id, option_id, count):


        sql = "UPDATE `cart_item` set `count` = '{}' where `product_id`='{}' and `option_id`='{}'".format(count, product_id, option_id)

        # 엑셀에서 불러온 cell에 데이터가 없는 경우, null 로 치환
        sql = sql.replace("'None'", "null")

        self.db.execute(sql)

