import jwt
from datetime import datetime
from flask import jsonify
from config import SECRET_KEY  # Đảm bảo bạn đã cấu hình SECRET_KEY trong file config.py

def verify_token(token):
    """
    Hàm kiểm tra token.
    :param token: JWT token từ header Authorization.
    :return: Payload của token nếu hợp lệ, None nếu không hợp lệ hoặc hết hạn.
    """
    try:
        # Xóa từ "Bearer " nếu có trong token
        if token.startswith("Bearer "):
            token = token[7:]

        # Giải mã JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # Kiểm tra nếu token không hết hạn
        if datetime.utcfromtimestamp(payload['exp']) < datetime.utcnow():
            return None  # Token đã hết hạn

        return payload  # Trả về dữ liệu của payload (user_id, role, ...)

    except jwt.ExpiredSignatureError:
        return None  # Token đã hết hạn
    except jwt.InvalidTokenError:
        return None  # Token không hợp lệ
