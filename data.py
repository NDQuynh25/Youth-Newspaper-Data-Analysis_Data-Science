import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file CSV
data = pd.read_csv('C:\\Users\\Admin\\Documents\\KHDL\\3_output_cleaned.csv')

# Hàm để loại bỏ các giá trị ngoại lai bằng phương pháp IQR
def remove_outliers_iqr(data, column):
    # Tính toán IQR cho cột 'column'
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1

    # Xác định giới hạn cho giá trị ngoại lai
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    print(f'>>> Lower bound: {lower_bound}')
    print(f'>>> Upper bound: {upper_bound}')
    # Lọc các hàng có giá trị ngoại lai
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
   
    # Loại bỏ các hàng có giá trị ngoại lai
    cleaned_data = data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]
    
    # Vẽ boxplot để trực quan hóa dữ liệu sau khi loại bỏ ngoại lai
    plt.figure(figsize=(10, 5))
    plt.boxplot(cleaned_data[column], vert=False)
    plt.title(f'Boxplot of {column} after Removing Outliers (IQR Method)')
    plt.xlabel(column)
    plt.show()

    return cleaned_data, outliers

# Gọi hàm để loại bỏ các giá trị ngoại lai trong cột 'Start'

cleaned_data_iqr, outliers_data_iqr = remove_outliers_iqr(data, 'Start')

# Hiển thị các giá trị ngoại lai
print(f'>>> Số lượng giá trị ngoại lai: {len(outliers_data_iqr)}')
print(outliers_data_iqr)

# Ghi dữ liệu đã làm sạch vào file CSV mới
cleaned_data_iqr.to_csv('C:\\Users\\Admin\\Documents\\KHDL\\4_cleaned_data_iqr.csv', index=False)
