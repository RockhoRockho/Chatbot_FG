# 학습 데이터 초기화

class OrderCancel():
    
    def __init__(self, db):
        self.db = db


    # db에 데이터 저장
    def delete_data(db, product_id, order_id):
        pk_db = pk
        product_id_db = product_id
        order_id_db = order_id

        sql = '''
            DELETE FROM `order_item` WHERE `product_id` = %s AND `order_id` = %s

        ''' % (product_id_db.value, order_id_db.value)

        # 엑셀에서 불러온 cell에 데이터가 없는 경우, null 로 치환
        sql = sql.replace("'None'", "null")

        with db.cursor() as cursor:
            cursor.execute(sql)
            db.commit()
