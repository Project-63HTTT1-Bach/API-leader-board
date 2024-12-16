from flask import Flask, request
from flask_cors import CORS  
from controllers.auth_controller import login, logout
from controllers.student_controller import get_student_detail
from controllers.leaderboard_controller import get_leaderboard_scores, get_user_detail
import config
import requests
import webbrowser

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

CORS(app, resources={r"/*": {"origins": "*"}})

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
app.add_url_rule('/leaderboard/<int:student_id>', 'get_user_detail', get_user_detail, methods=['GET'])

@app.route('/login_superset', methods=['POST'])
def login_superset_api():
    url = "https://wired-comic-monkfish.ngrok-free.app/login/"
    
    credentials = {
    "username": "user",  
    "password": "user",  
    "csrf_token": "IjMzYjE4MmYyOGZlZmE2NmY0ZjIwZmUwYmY3OGQ5ODA2MDEwNmY5YmMi.Z1-W3g.vwWniycdmV349vggQN2Ho_xpE4Y"
    }
    
    session = requests.Session()
    token_response = session.post(url, data=credentials, verify=False)
    
    if token_response.status_code == 200:        
        superset_main_url = "https://wired-comic-monkfish.ngrok-free.app/explore/?form_data_key=5CbEGC9GpiBftrhF85sWfPDvbjR03sz8fKPMiecssRha4aqdhDIPJn04iWUwyZxJ&slice_id=985"
        
        webbrowser.open(superset_main_url)

if __name__ == "__main__":
    app.run(debug=True)

