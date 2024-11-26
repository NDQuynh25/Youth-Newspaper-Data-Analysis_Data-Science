import mysql.connector
import pandas as pd
import os





# Kết nối tới MySQL
config = {
    'user': 'root',
    'password': 'NguyenQuynh250903@',
    'host': 'localhost',
    'database': 'data_science',
    'port': 3306
}

# Kết nối
conn = mysql.connector.connect(**config)
cursor = conn.cursor()


def save_data_raw ():
    for index in range(1, 2):
        file_path = f"data_raw/crawling_{index}.csv"
        data = pd.read_csv(file_path)
        data.head()

        if os.path.exists(file_path):
            print("Tệp tồn tại!")
        else:
            print("Tệp không tồn tại!")

        insert_query = """
        INSERT INTO data_raw (link, title, description, content, category, author, publish_date, start)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Đọc file CSV và chèn từng dòng
        for index, row in data.iterrows():
            cursor.execute(insert_query, (
                row['Link'], row['Title'], row['Description'], row['Content'],
                row['Category'], row['Author'], row['Publish Date'], row['Start']
            ))

   

save_data_raw()

conn.commit()
cursor.close()
conn.close()
print("Dữ liệu đã được chèn thành công!")
