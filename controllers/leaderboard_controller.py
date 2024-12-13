from flask import request, jsonify
from models.leaderboard_model import get_leaderboard_scores 
from controllers.verify_token import verify_token
from models.student_model import get_student_by_id

def get_total_scores():
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing!"}), 400

        user_data = verify_token(token)
        if not user_data:
            return jsonify({"error": "Invalid or expired token!"}), 401

        total_scores = get_leaderboard_scores()

        if total_scores is None or len(total_scores) == 0:
            return jsonify({"error": "No data found!"}), 404

        return jsonify({"data": total_scores}), 200

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

def get_user_detail(student_id):
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing!"}), 400

        user_data = verify_token(token)
        if not user_data:
            return jsonify({"error": "Invalid or expired token!"}), 401

        student = get_student_by_id(student_id)
        if not student:
            return jsonify({"error": "Student not found!"}), 404

        return jsonify({"data": student}), 200
    
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    