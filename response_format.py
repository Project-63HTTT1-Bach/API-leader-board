from flask import jsonify

def success_response(data, message="Success"):
    """
    Trả về response thành công.
    :param data: Dữ liệu cần trả về.
    :param message: Thông báo.
    :return: Response JSON.
    """
    return jsonify({
        "status": "success",
        "data": data,
        "message": message,
        "error": None
    }), 200

def error_response(message, error_code, description=""):
    """
    Trả về response lỗi.
    :param message: Thông báo lỗi.
    :param error_code: Mã lỗi.
    :param description: Mô tả lỗi chi tiết.
    :return: Response JSON.
    """
    return jsonify({
        "status": "error",
        "data": None,
        "message": message,
        "error": {
            "code": error_code,
            "description": description
        }
    }), error_code
