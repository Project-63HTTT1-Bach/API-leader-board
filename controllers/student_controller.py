from flask import request, jsonify
from controllers.verify_token import verify_token
from models.student_model import (
    get_student_by_id,
    get_all_students,
    student_exists,
    create_student,
    update_student,
    delete_student,
)
from models.user_model import create_user, delete_user

# Lấy danh sách sinh viên
def get_students():
    try:
        token = request.headers.get('Authorization')
        if not token:
            raise ValueError("Token is missing!")

        user_data = verify_token(token)
        if not user_data:
            raise ValueError("Invalid or expired token!")

        if user_data["role"] == 0:  # Admin có quyền xem đầy đủ
            return jsonify({"data": get_all_students()}), 200
        else:
            raise PermissionError("Unauthorized")
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except PermissionError as pe:
        return jsonify({"error": str(pe)}), 403
    except RuntimeError as re:
        return jsonify({"error": str(re)}), 500

# Lấy thông tin chi tiết sinh viên
def get_student_detail(student_id):
    try:
        token = request.headers.get('Authorization')
        if not token:
            raise ValueError("Token is missing!")

        user_data = verify_token(token)
        if not user_data:
            raise ValueError("Invalid or expired token!")

        student = get_student_by_id(student_id)
        if not student:
            raise ValueError("Student not found!")

        if user_data["role"] == 1 and user_data["user_id"] == student_id:
            return jsonify({"data": student}), 200
        elif user_data["role"] == 0:
            return jsonify({"data": student}), 200
        else:
            raise PermissionError("Unauthorized")
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except PermissionError as pe:
        return jsonify({"error": str(pe)}), 403
    except RuntimeError as re:
        return jsonify({"error": str(re)}), 500 

# Tạo sinh viên
def create_student_controller():
    try:
        token = request.headers.get('Authorization')
        if not token:
            raise ValueError("Token is missing!")

        user_data = verify_token(token)
        if not user_data:
            raise ValueError("Invalid or expired token!")

        if user_data["role"] != 0:
            raise PermissionError("Unauthorized")

        data = request.get_json()
        student_id = data.get("student_id")
        full_name = data.get("full_name")
        cluster_number = data.get("cluster_number")
        group_number = data.get("group_number")

        if student_exists(student_id):
            raise ValueError("Student already exists!")

        create_student(student_id, full_name, cluster_number, group_number)
        create_user(student_id)

        return jsonify({"message": "Student created successfully!"}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except PermissionError as pe:
        return jsonify({"error": str(pe)}), 403
    except RuntimeError as re:
        return jsonify({"error": str(re)}), 500
    
# Cập nhật sinh viên
def update_student_controller(student_id):
    try:
        token = request.headers.get('Authorization')
        if not token:
            raise ValueError("Token is missing!")

        user_data = verify_token(token)
        if not user_data:
            raise ValueError("Invalid or expired token!")

        if user_data["role"] != 0 and user_data["user_id"] != student_id:
            raise PermissionError("Unauthorized")

        if not student_exists(student_id):
            raise ValueError("Student does not exist!")

        data = request.get_json()
        full_name = data.get("full_name")
        cluster_number = data.get("cluster_number")
        group_number = data.get("group_number")

        update_student(student_id, full_name, cluster_number, group_number)

        return jsonify({"message": "Student updated successfully!"}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except PermissionError as pe:
        return jsonify({"error": str(pe)}), 403
    except RuntimeError as re:
        return jsonify({"error": str(re)}), 500
    
# Xóa sinh viên
def delete_student_controller(student_id):
    try:
        token = request.headers.get('Authorization')
        if not token:
            raise ValueError("Token is missing!")

        user_data = verify_token(token)
        if not user_data:
            raise ValueError("Invalid or expired token!")

        if user_data["role"] != 0:
            raise PermissionError("Unauthorized")

        if not student_exists(student_id):
            raise ValueError("Student does not exist!")

        delete_student(student_id)
        delete_user(student_id)
        
        return jsonify({"message": "Student deleted successfully!"}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except PermissionError as pe:
        return jsonify({"error": str(pe)}), 403
    except RuntimeError as re:
        return jsonify({"error": str(re)}), 500
