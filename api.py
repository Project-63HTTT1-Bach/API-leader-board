from flask import Flask, request
from flask_cors import CORS  
from controllers.auth_controller import login, logout
from controllers.student_controller import get_student_detail
from controllers.leaderboard_controller import get_leaderboard_scores
import config

app = Flask(__name__)
# Cấu hình CORS
CORS(app)
app.config['SECRET_KEY'] = config.SECRET_KEY

@app.route('/login', methods=['POST'])
def login_api():
    username = request.json.get('username')
    password = request.json.get('password')

    return login(username, password)

@app.route('/logout', methods=['POST'])
def logout_api():
    return logout()

# # API để nhận dữ liệu từ Google Apps Script
# @app.route('/update', methods=['POST'])
# def update_data():
#     try:
#         # Lấy dữ liệu từ request
#         data = request.get_json()
        
#         # In dữ liệu nhận được (để kiểm tra)
#         print("Received data:", data)
        
#         # Xử lý dữ liệu
#         sheet_name = data.get("sheetName")
#         row = data.get("row")
#         col = data.get("col")
#         new_value = data.get("newValue")
#         old_value = data.get("oldValue")

#         # Ở đây bạn có thể thêm logic để cập nhật vào cơ sở dữ liệu
#         # Ví dụ: Cập nhật vào một bảng PostgreSQL hoặc MySQL

#         # Phản hồi lại Google Apps Script
#         return jsonify({"status": "success", "message": "Data received and processed"}), 200
#     except Exception as e:
#         # Xử lý lỗi
#         print("Error:", str(e))
#         return jsonify({"status": "error", "message": str(e)}), 500

app.add_url_rule('/students', 'get_student_detail', get_student_detail, methods=['GET'])

app.add_url_rule('/leaderboard', 'get_leaderboard_scores', get_leaderboard_scores, methods=['GET'])

if __name__ == "__main__":
    app.run(debug=True)

