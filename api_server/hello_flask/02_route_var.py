from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello 플라스크'

@app.route('/info/<name>')
def get_name(name):
    return f"hello {name}"

@app.route('/user/<int:id>')
def get_user(id):
    return f'id:{id}, id+1:{id+1}'

@app.route('/json/<int:dest_id>/<message>')
@app.route('/JSON/<int:dest_id>/<message>')
def send_message(dest_id, message):
    data = {
        'bot_id': dest_id,
        'message': message
    }
    return data  # dict 를 리턴하면 application/json 으로 response 된드아!

if __name__ == '__main__':
    app.run(debug=True)