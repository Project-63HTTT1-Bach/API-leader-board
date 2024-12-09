from flask import request, jsonify
from models.leaderboard_model import get_leaderboard_scores 
from controllers.verify_token import verify_token

def get_total_scores():
    try:
        # Lấy token từ header
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing!"}), 400

        # Kiểm tra token hợp lệ
        user_data = verify_token(token)
        if not user_data:
            return jsonify({"error": "Invalid or expired token!"}), 401

        # Lấy role và student_id
        role = user_data["role"]
        student_id = None
        if role == 1:  # Nếu là sinh viên, lấy student_id từ user_data
            student_id = user_data["user_id"]

        # Gọi model để lấy điểm tổng
        total_scores = get_leaderboard_scores(student_id)

        if total_scores is None or len(total_scores) == 0:
            return jsonify({"error": "No data found!"}), 404

        return jsonify({"data": total_scores}), 200

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
