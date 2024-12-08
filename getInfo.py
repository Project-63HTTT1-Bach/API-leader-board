import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

token_url = "https://sinhvien1.tlu.edu.vn/education/oauth/token"

credentials = {
    "username": "",  
    "password": "",  
    "grant_type": "password", 
    "client_id": "education_client",
    "client_secret": "password"
}

token_response = requests.post(token_url, data=credentials, verify=False)

if token_response.status_code == 200:
    print("Lấy token thành công!")
    token_data = token_response.json()
    access_token = token_data.get("access_token")

    headers = {
        "Authorization": f"Bearer {access_token}",  
        "Accept": "application/json",
    }

    url = "https://sinhvien1.tlu.edu.vn/education/api/users/getCurrentUser"
    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        data = response.json()
        print("Thông tin người dùng:")
        print(f"Họ và tên: {data.get('displayName', 'N/A')}")
        print(f"Email: {data.get('email', 'N/A')}")
        print(f"Mã sinh viên: {data.get('username', 'N/A')}")
        print("-" * 50)
    else:
        print("Lỗi khi lấy dữ liệu:", response.status_code)
        print(response.text)
        
    url = "https://sinhvien1.tlu.edu.vn/education/api/StudentCourseSubject/studentLoginUser/11"
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        data = response.json()
        
        for subject in data:
            try:
                if subject.get("id", "N/A") == 1834567:
                    subject_id = subject.get("id", "N/A")
                    subject_code = subject.get("subjectCode", "N/A")
                    
                    timetables = subject.get("courseSubject", {}).get("timetables", [])
                    
                    if len(timetables) > 0:
                        week_index_0 = timetables[0].get("weekIndex", "N/A")
                        start_hour_name_0 = timetables[0].get("startHour", {}).get("name", "N/A")
                        start_hour_string_0 = timetables[0].get("startHour", {}).get("startString", "N/A")
                        end_hour_name_0 = timetables[0].get("endHour", {}).get("name", "N/A")
                        end_hour_string_0 = timetables[0].get("endHour", {}).get("endString", "N/A")
                        room_0 = timetables[0].get("room", {}).get("name", "N/A")
                    else:
                        week_index_0 = start_hour_name_0 = start_hour_string_0 = "N/A"
                        end_hour_name_0 = end_hour_string_0 = room_0 = "N/A"
                        
                    if len(timetables) > 1:
                        week_index_1 = timetables[1].get("weekIndex", "N/A")
                        start_hour_name_1 = timetables[1].get("startHour", {}).get("name", "N/A")
                        start_hour_string_1 = timetables[1].get("startHour", {}).get("startString", "N/A")
                        end_hour_name_1 = timetables[1].get("endHour", {}).get("name", "N/A")
                        end_hour_string_1 = timetables[1].get("endHour", {}).get("endString", "N/A")
                        room_1 = timetables[1].get("room", {}).get("name", "N/A")
                        from_week = timetables[1].get("fromWeek", "N/A")
                        to_week = timetables[1].get("toWeek", "N/A")
                    else:
                        week_index_1 = start_hour_name_1 = start_hour_string_1 = "N/A"
                        end_hour_name_1 = end_hour_string_1 = room_1 = from_week = to_week = "N/A"
                    
                    print(f"ID môn: {subject_id}")
                    print(f"Tên môn: {subject_code}")
                    print(f"Tuần bắt đầu: {from_week} - Tuần kết thúc: {to_week}")
                    print(f"Thứ: {week_index_0} - Phòng: {room_0}")
                    print(f"Giờ bắt đầu: {start_hour_name_0} - {start_hour_string_0}")
                    print(f"Giờ kết thúc: {end_hour_name_0} - {end_hour_string_0}")
                    print(f"Thứ: {week_index_1} - Phòng: {room_1}")
                    print(f"Giờ bắt đầu: {start_hour_name_1} - {start_hour_string_1}")
                    print(f"Giờ kết thúc: {end_hour_name_1} - {end_hour_string_1}")
                    
                    print("-" * 50)
            except KeyError as e:
                print(f"Lỗi khi trích xuất dữ liệu: {e}")
    else:
        print("Lỗi khi lấy dữ liệu:", response.status_code)
        print(response.text)
else:
    print("Lấy token thất bại!")
    print(token_response.text)
