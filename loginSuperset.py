import requests
import urllib3
import webbrowser

# Tắt cảnh báo SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL đăng nhập của Superset
token_url = "https://wired-comic-monkfish.ngrok-free.app/login/"

# Thông tin đăng nhập
credentials = {
    "username": "user",  
    "password": "user",  
    "csrf_token": "IjMzYjE4MmYyOGZlZmE2NmY0ZjIwZmUwYmY3OGQ5ODA2MDEwNmY5YmMi.Z1-W3g.vwWniycdmV349vggQN2Ho_xpE4Y"
}

# Gửi yêu cầu POST để đăng nhập
session = requests.Session()
token_response = session.post(token_url, data=credentials, verify=False)

if token_response.status_code == 200:
    print("Đăng nhập thành công!")
    
    # URL chính của Superset
    superset_main_url = "https://wired-comic-monkfish.ngrok-free.app/explore/?form_data_key=5CbEGC9GpiBftrhF85sWfPDvbjR03sz8fKPMiecssRha4aqdhDIPJn04iWUwyZxJ&slice_id=985"
    
    # Mở giao diện chính của Superset trong trình duyệt
    webbrowser.open(superset_main_url)
else:
    print(f"Đăng nhập thất bại! Mã lỗi: {token_response.status_code}")
    print(f"Nội dung trả về: {token_response.text}")
