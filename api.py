from flask import Flask, request
from controllers.auth_controller import login  
from controllers.student_controller import get_students, get_student_detail, create_student_controller, update_student_controller, delete_student_controller
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

if __name__ == "__main__":
    app.run(debug=True)
