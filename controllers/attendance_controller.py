from flask import request, jsonify
from models.attendance_model import (
    get_all_attendance,
    get_attendance_by_id,
    create_attendance_record,
    update_attendance_record,
    delete_attendance_record,
)
from controllers.verify_token import verify_token

def get_attendance_list():
    try:
        token = request.headers.get('Authorization')
        if not token:
            raise ValueError("Token is missing!")

        user_data = verify_token(token)
        if not user_data:
            raise ValueError("Invalid or expired token!")

        if user_data["role"] == 0:  
            return jsonify({"data": get_all_attendance()}), 200
        elif user_data["role"] == 1: 
            student_id = user_data["user_id"]
            attendance_data = get_all_attendance(student_id)
            return jsonify({"data": attendance_data}), 200
        else:
            raise PermissionError("Unauthorized")
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except PermissionError as pe:
        return jsonify({"error": str(pe)}), 403
    except RuntimeError as re:
        return jsonify({"error": str(re)}), 500


def get_attendance_detail(id):
    try:
        token = request.headers.get('Authorization')
        if not token:
            raise ValueError("Token is missing!")

        user_data = verify_token(token)
        if not user_data:
            raise ValueError("Invalid or expired token!")

        attendance = get_attendance_by_id(id)
        if not attendance:
            raise ValueError("Attendance not found!")

        if user_data["role"] == 0 or (user_data["role"] == 1 and attendance['student_id'] == user_data["user_id"]):
            return jsonify({"data": attendance}), 200
        else:
            raise PermissionError("Unauthorized")
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except PermissionError as pe:
        return jsonify({"error": str(pe)}), 403
    except RuntimeError as re:
        return jsonify({"error": str(re)}), 500

def create_attendance():
    try:
        token = request.headers.get('Authorization')
        if not token:
            raise ValueError("Token is missing!")

        user_data = verify_token(token)
        if not user_data:
            raise ValueError("Invalid or expired token!")

        data = request.get_json()
        if user_data["role"] == 1 and data.get("student_id") != user_data["user_id"]:
            raise PermissionError("Unauthorized")

        create_attendance_record(data)
        return jsonify({"message": "Attendance created successfully!"}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except PermissionError as pe:
        return jsonify({"error": str(pe)}), 403
    except RuntimeError as re:
        return jsonify({"error": str(re)}), 500

def update_attendance(id):
    try:
        token = request.headers.get('Authorization')
        if not token:
            raise ValueError("Token is missing!")

        user_data = verify_token(token)
        if not user_data:
            raise ValueError("Invalid or expired token!")

        attendance = get_attendance_by_id(id)
        if not attendance:
            raise ValueError("Attendance not found!")

        if user_data["role"] != 0 and attendance['student_id'] != user_data["user_id"]:
            raise PermissionError("Unauthorized")

        data = request.get_json()
        update_attendance_record(id, data)
        return jsonify({"message": "Attendance updated successfully!"}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except PermissionError as pe:
        return jsonify({"error": str(pe)}), 403
    except RuntimeError as re:
        return jsonify({"error": str(re)}), 500

def delete_attendance(id):
    try:
        token = request.headers.get('Authorization')
        if not token:
            raise ValueError("Token is missing!")

        user_data = verify_token(token)
        if not user_data:
            raise ValueError("Invalid or expired token!")

        attendance = get_attendance_by_id(id)
        if not attendance:
            raise ValueError("Attendance not found!")

        if user_data["role"] != 0:
            raise PermissionError("Unauthorized")

        delete_attendance_record(id)
        return jsonify({"message": "Attendance deleted successfully!"}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except PermissionError as pe:
        return jsonify({"error": str(pe)}), 403
    except RuntimeError as re:
        return jsonify({"error": str(re)}), 500
