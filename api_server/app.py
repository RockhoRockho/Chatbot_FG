from flask import Flask, request, jsonify

import socket
import json


# 챗봇 엔진 서버 접속 정보
# 이전에 만든 챗봇 엔진 서버에서 설정한 포트를 사용해야 한다
host = "127.0.0.1"  # 챗봇 엔진 서버 IP 주소
port = 5050  # 챗봇 엔진 서버 통신 포트

# Flask 어플리케이션
app = Flask(__name__)

# cors 가 문제다...
from flask_cors import CORS
CORS(app)


json_data = {
    "BotType" : "ProjectFG_Cafe",
    }
temp_state = 0
temp_product = 0
temp_price = 0
temp_option = 1
temp_detail = ''

@app.route('/query/<bot_type>', methods=['POST'])
def query(bot_type):
    while True:
        global temp_state
        global temp_product
        global temp_price
        global temp_option
        global temp_detail

        dataj = request.get_json()
        query = dataj['query']
        user = dataj['user']

        mySocket = socket.socket()
        mySocket.connect((host, port))

        json_data["Query"] = query
        json_data["State"] = temp_state
        json_data["Product"] = temp_product
        json_data['Price'] = temp_price
        json_data['Option'] = temp_option
        json_data['Detail'] = temp_detail
        json_data['UserId'] = user
        print(json_data)
        message = json.dumps(json_data)
        mySocket.send(message.encode())

        data = mySocket.recv(32768).decode()
        ret_data = json.loads(data)

        print("답변 : ")
        print(ret_data['Answer'])
        print(ret_data)
        print(type(ret_data))
        print("\n")

        temp_state = ret_data['State']
        temp_product = ret_data['Product']
        temp_price = ret_data['Price']
        temp_option = ret_data['Option']

        mySocket.close()
        return jsonify(ret_data)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.10', port=5000)