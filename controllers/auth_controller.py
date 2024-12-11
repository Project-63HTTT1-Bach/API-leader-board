import requests
import jwt
from response_format import success_response, error_response
from config import SECRET_KEY

def login(username, password):
    try:
        if not username or not password:
            return error_response("Username and password are required", 400)

        try:
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
                payload = {
                    "user_id": username,
                    "oauth_token": access_token
                }
                access_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
                return success_response({
                    "access_token": access_token,
                }, "Login successful")
            else:
                return error_response("Failed to obtain access token", 500, "Could not get access token from external service.")
        except requests.exceptions.Timeout:
            return error_response("Request timeout", 408, "The request to obtain access token took too long.")
        except requests.exceptions.RequestException as e:
            return error_response(f"Request error: {str(e)}", 500, "An error occurred while communicating with the external service.")
    
    except RuntimeError as e:
        return error_response(str(e), 500, "An error occurred while logging in.")
