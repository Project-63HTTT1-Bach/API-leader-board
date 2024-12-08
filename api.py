from flask import Flask, request
from controllers.auth_controller import login  

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login_api():
    username = request.json.get('username')
    password = request.json.get('password')

    return login(username, password)

if __name__ == "__main__":
    app.run(debug=True)
