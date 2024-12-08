import sqlite3
import requests
import jwt
from datetime import datetime, timedelta
from models.user_model import get_user_from_db, check_password
from response_format import success_response, error_response
from config import SECRET_KEY

def login(username, password):
    if not username or not password:
        return error_response("Username and password are required", 400)

    user = get_user_from_db(username)

    if not user:
        return error_response("User not found", 404, "The user does not exist in the database.")

    # TH1: Nếu đăng nhập được từ OAuth và có trong DB
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
            # Tạo access token bằng JWT cho sinh viên
            payload = {
                "user_id": username,
                "role": 1,
                "exp": datetime.utcnow() + timedelta(hours=1)
            }
            access_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            return success_response({
                "access_token": access_token,
                "user_id": username,
                "role": 1
            }, "Login successful")

        else:
            return error_response("Failed to obtain access token", 500, "Could not get access token from external service.")

    # TH2: Nếu role khác 1 (Admin)
    if user['role'] == 0:
        if not check_password(password, user['password']):
            return error_response("Invalid password", 401, "The password provided is incorrect.")

        # Tạo access token bằng JWT cho admin
        payload = {
            "user_id": username,
            "role": 0,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        access_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return success_response({
            "access_token": access_token,
            "user_id": username,
            "role": 0
        }, "Login successful")

    return error_response("Invalid role", 403, "The user does not have the appropriate role.")
