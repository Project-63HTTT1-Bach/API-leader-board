from flask import Flask, request
from controllers.auth_controller import login  
from controllers.student_controller import (
    get_students, 
    get_student_detail, 
    create_student_controller, 
    update_student_controller, 
    delete_student_controller)
from controllers.attendance_controller import (
    get_attendance_list, 
    get_attendance_detail, 
    create_attendance, 
    update_attendance, 
    delete_attendance)
from controllers.leaderboard_controller import (
    get_leaderboard_scores
)


app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login_api():
    username = request.json.get('username')
    password = request.json.get('password')

    return login(username, password)

app.add_url_rule('/students', 'get_students', get_students, methods=['GET'])
app.add_url_rule('/students/<student_id>', 'get_student_detail', get_student_detail, methods=['GET'])
app.add_url_rule('/students', 'create_student_controller', create_student_controller, methods=['POST'])
app.add_url_rule('/students/<student_id>', 'update_student_controller', update_student_controller, methods=['PUT'])
app.add_url_rule('/students/<student_id>', 'delete_student_controller', delete_student_controller, methods=['DELETE'])

app.add_url_rule('/attendance', 'get_attendance_list', get_attendance_list, methods=['GET'])
app.add_url_rule('/attendance/<int:id>', 'get_attendance_detail', get_attendance_detail, methods=['GET'])
app.add_url_rule('/attendance', 'create_attendance', create_attendance, methods=['POST'])
app.add_url_rule('/attendance/<int:id>', 'update_attendance', update_attendance, methods=['PUT'])
app.add_url_rule('/attendance/<int:id>', 'delete_attendance', delete_attendance, methods=['DELETE'])

app.add_url_rule('/leaderboard', 'get_leaderboard_scores', get_leaderboard_scores, methods=['GET'])

if __name__ == "__main__":
    app.run(debug=True)

