import requests
from datetime import datetime

# Thông tin cần thiết
spreadsheet_id = '1gkEoNyGar6bqgAQRJdFlpvIK033j821K1pk5vUWJyss'  # Thay bằng ID của Google Sheet
range_ = 'Trang tính1!A1:C66'  
api_key = 'AIzaSyDMaZNpl9Kg-MkBfjhpTFE0XdsPaQQsIKs'  # Thay bằng API Key của bạn

# URL của API
url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_}?key={api_key}"

# Gửi yêu cầu GET đến API
response = requests.get(url)

# Kiểm tra kết quả và in ra
if response.status_code == 200:
    data = response.json()['values']
    print(data)
else:
    print(f"Error: {response.status_code}")
