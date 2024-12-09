from flask import Flask, request
from controllers.auth_controller import login, logout
from controllers.student_controller import get_student_detail
from controllers.leaderboard_controller import get_leaderboard_scores
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

@app.route('/login', methods=['POST'])
def login_api():
    username = request.json.get('username')
    password = request.json.get('password')

    return login(username, password)

@app.route('/logout', methods=['POST'])
def logout_api():
    return logout()

app.add_url_rule('/students', 'get_student_detail', get_student_detail, methods=['GET'])

app.add_url_rule('/leaderboard', 'get_leaderboard_scores', get_leaderboard_scores, methods=['GET'])

if __name__ == "__main__":
    app.run(debug=True)

