from datetime import datetime, timezone, timedelta
import re

def convert_to_minutes(time_str, epoch=datetime(1970, 1, 1, tzinfo=timezone.utc)):
    """
    Chuyển đổi thời gian từ chuỗi có định dạng "dd/mm/yyyy hh:mm GMT+offset"
    thành số phút từ thời điểm epoch đã chọn.
    
    Parameters:
    - time_str (str): Chuỗi thời gian cần chuyển đổi (vd: "26/05/2024 07:19 GMT+7").
    - epoch (datetime): Thời điểm gốc để tính số phút (mặc định là Unix epoch).
    
    Returns:
    - int: Số phút từ thời điểm epoch đến thời điểm trong time_str.
    """
    # Loại bỏ "GMT" và thay đổi định dạng múi giờ
    time_str = time_str.replace("GMT+7", "+0700").strip()


    # Chuyển chuỗi thời gian thành datetime
    time_obj = datetime.strptime(time_str, "%d/%m/%Y %H:%M %z")
    
    # Đảm bảo epoch cũng có thông tin múi giờ
    epoch = epoch.astimezone(timezone.utc)
    
    # Tính số phút từ epoch đến thời điểm đã cho
    minutes_from_epoch = int((time_obj - epoch).total_seconds() / 60)
    
    return minutes_from_epoch

# Ví dụ sử dụng
time_str = "26/05/2024 07:19 GMT+7"
print(convert_to_minutes(time_str))  # Sẽ trả về số phút tính từ Unix epoch
