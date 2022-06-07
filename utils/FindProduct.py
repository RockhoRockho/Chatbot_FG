class FindProduct:
    
    # Database 인스턴스 객체로 생성
    def __init__(self, db):
        self.db = db    # 이 객체를 통해 답변을 검색
        
    # 답변 검색
    def search(self, query):  
        # 질문내용 (query)으로 답변 검색
        sql = self._make_query(query)
        answer = self.db.select_all(sql)
            
        return answer
    
    def search_id_from_name(self, name):
        sql = "select id from product_cafe where name = '{}'".format(name)
        product_id = self.db.select_one(sql)
        p_id = product_id['id']
        return p_id
    
    def search_name_from_id(self, pk):
        sql = "select name from product_cafe where id = '{}'".format(pk)
        product_id = self.db.select_one(sql)
        p_name = product_id['name']
        return p_name
    
    def search_detail_from_name(self, name):
        sql = "select detail from product_cafe where name = '{}'".format(name)
        product_detail = self.db.select_one(sql)
        p_detail = product_detail['detail']
        return p_detail
    
    def search_image_from_name(self, name):
        sql = "select image from product_cafe where name = '{}'".format(name)
        product_image = self.db.select_one(sql)
        p_image = product_image['image']
        return p_image
    
    def search_price_from_id(self, product_id):
        sql = "select price from product_cafe where id = '{}'".format(product_id)
        product_price = self.db.select_one(sql)
        p_price = product_price['price']
        return p_price
    
    # 검색 쿼리 생성
    def _make_query(self, query):
        sql = "select * from product_cafe"

        # 해당 query 목록 전부 고르기
        if query == '라떼':
            sql = sql + " where latte=1"
        elif query == '커피':
            sql = sql + " where coffee=1"
        elif query == '음료':
            sql = sql + " where drink=1"
        elif query == '식사':
            sql = sql + " where food=1"
            
        # 추천 목록 대상은 따로 db에 따라 적용
        elif query == '시그니처':
            sql = sql + " where recommend = 1"
        elif query == '인기':
            sql = sql + " where recommend = 2"
        elif query == '추천':
            sql = sql + " where recommend = 3"
        
        # 나머지 
        else:
            sql = sql + " where name = '{}'".format(query)
            
            
        return sql       
