import requests
import jwt
from models.user_model import get_user_from_db, check_password
from response_format import success_response, error_response
from config import SECRET_KEY  

def login(username, password):
    if not username or not password:
        return error_response("Username and password are required", 400)

    user = get_user_from_db(username)

    if not user:
        return error_response("User not found", 404, "The user with the provided username does not exist.")

    # Nếu role = 1 (Sinh viên), không cần kiểm tra mật khẩu, chỉ lấy token từ OAuth
    if user['role'] == 1:
        token_url = "https://sinhvien1.tlu.edu.vn/education/oauth/token"
        credentials = {
            "username": username,
            "password": password,  
            "grant_type": "password",
            "client_id": "education_client",
            "client_secret": "password"
        }

        token_response = requests.post(token_url, data=credentials, verify=False)

        if token_response.status_code == 200:
            token_data = token_response.json()
            access_token = token_data.get("access_token")

            return success_response({
                "access_token": access_token,
                "user_id": username
            }, "Login successful")
        else:
            return error_response("Failed to obtain access token", 500, "Could not get access token from external service.")
    
    # Nếu role = 0 (Admin), kiểm tra mật khẩu trong cơ sở dữ liệu
    if user['role'] == 0:
        if not check_password(password, user['password']):
            return error_response("Invalid password", 401, "The password provided is incorrect.")

        # Tạo access token bằng JWT cho admin
        payload = {
            "user_id": username,
            "role": user['role']
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return success_response({
            "access_token": access_token,
            "user_id": username
        }, "Login successful")

    return error_response("Invalid role", 403, "The user does not have the appropriate role.")
