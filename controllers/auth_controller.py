import requests
import jwt
from datetime import datetime, timedelta
from models.user_model import get_user_from_db, check_password
from response_format import success_response, error_response
from config import SECRET_KEY

def login(username, password):
    try:
        if not username or not password:
            return error_response("Username and password are required", 400)

        user = get_user_from_db(username)

        if not user:
            return error_response("User not found", 404, "The user does not exist in the database.")

        # If role is 1 (Student) and logging in from OAuth
        if user['role'] == 1 and user['user_id'] != "2151161167":
            token_url = "https://sinhvien1.tlu.edu.vn/education/oauth/token"
            credentials = {
                "username": username,
                "password": password,
                "grant_type": "password",
                "client_id": "education_client",
                "client_secret": "password"
            }

            try:
                token_response = requests.post(token_url, data=credentials, verify=False, timeout=10)  # Timeout after 10 seconds

                if token_response.status_code == 200:
                    # Create access token for student using JWT
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
            except requests.exceptions.Timeout:
                return error_response("Request timeout", 408, "The request to obtain access token took too long.")
            except requests.exceptions.RequestException as e:
                return error_response(f"Request error: {str(e)}", 500, "An error occurred while communicating with the external service.")

        # If role is 0 (Admin)
        if user['role'] == 0 or user['user_id'] == "2151161167":
            if not check_password(password, user['password']):
                return error_response("Invalid password", 401, "The password provided is incorrect.")
            role = 0
            if user['user_id'] == "2151161167":
                role = 1
            # Create access token for admin using JWT
            payload = {
                "user_id": username,
                "role": role,
                "exp": datetime.utcnow() + timedelta(hours=1)
            }
            access_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            return success_response({
                "access_token": access_token,
                "user_id": username,
                "role": role
            }, "Login successful")

        return error_response("Invalid role", 403, "The user does not have the appropriate role.")
    
    except RuntimeError as e:
        return error_response(str(e), 500, "An error occurred while logging in.")
