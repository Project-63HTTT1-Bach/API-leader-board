from flask import request, jsonify
from controllers.verify_token import verify_token
from models.student_model import get_student_by_id

def get_student_detail():
    try:
        token = request.headers.get('Authorization')
        if not token:
            raise ValueError("Token is missing!")

        user_data = verify_token(token)
        if not user_data:
            raise ValueError("Invalid or expired token!")

        student = get_student_by_id(user_data['user_id'])
        if not student:
            raise ValueError("Student not found!")

        return jsonify({"data": student}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except PermissionError as pe:
        return jsonify({"error": str(pe)}), 403
    except RuntimeError as re:
        return jsonify({"error": str(re)}), 500 

