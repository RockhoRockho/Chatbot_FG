'''
GET        서버 리소스를 읽어올때
POST       서버 리소스를 생성할때
PUT/PATCH  서버 리소스를 수정할때
DELETE     서버 리소스를 삭제할때
'''

# request  : 클라이언트로부터 HTTP 요청 (request) 을 받았을때 요청 정보 확인
# jsonify  : 데이터 객체를 json response 로 변환
from flask import Flask, request, jsonify
app = Flask(__name__)


# 데이터 (사용자)
resource = []

# 사용자 정보 조회
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):

    for user in resource:
        if user['user_id'] is user_id:
            return jsonify(user)

    return jsonify(None)

# 사용자 추가
@app.route('/user', methods=['POST'])
def add_user():
    user = request.get_json()  # request 에 담겨 있는  parameter 들
    print('POST', user)
    resource.append(user)
    return jsonify(resource)


if __name__ == '__main__':
    app.run(debug=True)