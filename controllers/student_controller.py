from flask import request, jsonify
from controllers.verify_token import verify_token
from models.student_model import get_student_by_id, get_all_students, student_exists, full_name_exists_except_id, create_student, update_student, delete_student
from models.user_model import create_user

# Lấy danh sách sinh viên
def get_students():
    token = request.headers.get('Authorization')  
    if not token:
        return jsonify({"error": "Token is missing!"}), 400

    user_data = verify_token(token)
    if not user_data:
        return jsonify({"error": "Invalid or expired token!"}), 401
    
    if user_data["role"] == 0:
        return jsonify({"data": get_all_students()}), 200  # Admin mới có quyền xem đầy đủ

    return jsonify({"error": "Unauthorized"}), 403  

# Lấy thông tin chi tiết sinh viên
def get_student_detail(student_id):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Token is missing!"}), 400

    user_data = verify_token(token)
    if not user_data:
        return jsonify({"error": "Invalid or expired token!"}), 401
    
    student = get_student_by_id(student_id)
    if not student:
        return jsonify({"error": "Student not found!"}), 404

    if user_data["role"] == 1 and user_data["user_id"] == student_id:
        return jsonify({"data": student}), 200  # Sinh viên chỉ có quyền xem chi tiết bản thân

    if user_data["role"] == 0:  # Admin có quyền xem tất cả thông tin
        return jsonify({"data": student}), 200

    return jsonify({"error": "Unauthorized"}), 403  # Chỉ admin và bản thân sinh viên mới có quyền xem chi tiết

# Controller cho việc tạo học sinh (chỉ cho role=0)
def create_student_controller():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Token is missing!"}), 400

    user_data = verify_token(token)
    if not user_data:
        return jsonify({"error": "Invalid or expired token!"}), 401

    if user_data["role"] == 0:  # Admin mới có quyền tạo
        data = request.get_json()
        student_id = data.get("student_id")
        full_name = data.get("full_name")
        cluster_number = data.get("cluster_number")
        group_number = data.get("group_number")

        if student_exists(student_id):
            return jsonify({"error": "Student already exists!"}), 400

        create_student(student_id, full_name, cluster_number, group_number)
        create_user(student_id)
        return jsonify({"message": "Student created successfully!"}), 201
    else:
        return jsonify({"error": "Unauthorized"}), 403

# Controller cho việc cập nhật học sinh (chỉ cho role=0 hoặc bản thân mình cho role=1)
def update_student_controller(student_id):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Token is missing!"}), 400

    user_data = verify_token(token)
    if not user_data:
        return jsonify({"error": "Invalid or expired token!"}), 401

    if user_data["role"] == 0 or user_data["user_id"] == student_id:  # Admin hoặc bản thân sinh viên
        data = request.get_json()
        full_name = data.get("full_name")
        cluster_number = data.get("cluster_number")
        group_number = data.get("group_number")
        
        if full_name_exists_except_id(student_id, full_name):
            return jsonify({"error": "Full name already exists!"}), 400
        
        update_student(student_id, full_name, cluster_number, group_number)
        return jsonify({"message": "Student updated successfully!"}), 200
    else:
        return jsonify({"error": "Unauthorized"}), 403

# Controller cho việc xóa học sinh (chỉ cho role=0)
def delete_student_controller(student_id):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Token is missing!"}), 400

    user_data = verify_token(token)
    if not user_data:
        return jsonify({"error": "Invalid or expired token!"}), 401

    if user_data["role"] == 0:  # Chỉ admin mới có quyền xóa
        if not student_exists(student_id):
            return jsonify({"error": "Student does not exist!"}), 400
        
        delete_student(student_id)
        return jsonify({"message": "Student deleted successfully!"}), 200
    else:
        return jsonify({"error": "Unauthorized"}), 403
