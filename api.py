from flask import Flask, request, jsonify
from flask_cors import CORS  
from controllers.auth_controller import login, logout
from controllers.student_controller import get_student_detail
from controllers.leaderboard_controller import get_leaderboard_scores, get_user_detail
from models.student_model import get_bonus_points_by_student_id, get_bonus_points, delete_bonus_point, add_bonus_point
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

# API để nhận dữ liệu từ Google Apps Script
@app.route('/update', methods=['POST'])
def update_data():
    try:
        # Lấy dữ liệu từ request
        data = request.get_json()
        
        # In dữ liệu nhận được (để kiểm tra)
        print("Received data:", data)
        
        # Xử lý dữ liệu
        sheet_name = data.get("sheetName")
        row = data.get("row")
        col = data.get("col")

        rowData = data.get("rowData")
        
        bonusPoint = rowData[23]
        
        studentId = rowData[1]
        
        aWardedDate = data.get("columnEdited")
        
        sumBonusPoint = get_bonus_points_by_student_id(studentId).get("sum")
        
        if (bonusPoint, sumBonusPoint, studentId, aWardedDate is not None):

            if(bonusPoint < sumBonusPoint):
                bonusPointId = get_bonus_points(studentId, aWardedDate).get("id")
                if(bonusPointId is None):
                    raise ValueError("bonusPoint cannot be found")
                delete_bonus_point(bonusPointId)
            elif(bonusPoint > sumBonusPoint):
                add_bonus_point(studentId, aWardedDate)

        return jsonify({"status": "success", "message": "Data received and processed"}), 200
    except Exception as e:
        # Xử lý lỗi
        print("Error:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500
    except ValueError as ve:
        # Xử lý lỗi
        print("Error:", str(ve))
        return jsonify({"status": "error", "message": str(ve)}), 500

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

