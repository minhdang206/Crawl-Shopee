import ast
import json
import os
import re
import pandas as pd
import time
import warnings

warnings.simplefilter("ignore")
#Thời gian bắt đầu
start_time = time.time()

# Hàm đọc file json
def read_js_file(file_path):
  try:
    with open(file_path, 'r', encoding="utf8") as file:
      js_code = file.read()
      return js_code
  except FileNotFoundError:
    print(f"File '{file_path}' not found.")
    return None

#Hàm chuyển đổi liên kết sản phẩm từ tên, mã sản phẩm, mã shop
def transform_product_url(product_name, product_id, shop_id):
  # Thay thế các kí tự đặt biệt trừ dấu () thành kí tự '-'
  modified_string = re.sub(r'[ \!\@\#\$\%\^\&\*\_\+\{\}\:\\\"\<\>\?\[\]\;\'\,\.\/\\\\\`\~]', '-', product_name)
  # Thay thế các cụm kí tự '-+' thành '-'
  modified_string = re.sub(r'-+', '-', modified_string)
  # Tạo chuỗi liên kết sản phẩm theo quy luật của Shopee
  product_url = f"https://shopee.vn/{modified_string}-i.{shop_id}.{product_id}"
  return product_url

folder = 'data_products_js'
files_in_folder = os.listdir(folder)

list_info_products = []
# Lặp qua các file trong folder data_products_js
for file in files_in_folder:
  # Đường dẫn file json
  js_file_path = os.path.join(folder, file)
  # Đọc nội dung file json
  js_content = read_js_file(js_file_path)
  # Kiểm tra nếu file json tồn tại và có dữ liệu trong file json
  if js_content:
    # Chuyển giá trị chuỗi của nội dung file json thành kiểu dữ liệu list
    product_data = ast.literal_eval(js_content)
    # Lặp qua các product trong list product_data
    for product in product_data:
      # Tạo liên kết sản phẩm bằng hàm transform_product_url tạo ở trên
      product_url = transform_product_url(product_name = product["name"] , product_id = product["itemid"], shop_id = product["shopid"])
      # Cập nhật vào list_info_products một dictionary chứa các key là trường cần lấy. 
      list_info_products.append({
        'product_name': str(product["name"]),
        'product_url':  product_url,
        'product_rating': product['item_rating']['rating_star'],
        'product_price': product["price"]/100000,
        'product_revenue': (product["price"]/100000) * product["historical_sold"],
      })
    print(f"Done {len(list_info_products)} products")
# Lưu file dưới dạng csv và excel
df_products = pd.DataFrame(list_info_products)
df_products.to_csv('data_transformed\shopee_products.csv', index=False)
df_products.to_excel('data_transformed\shopee_products.xlsx', index=False)

#Thời gian kết thúc
end_time = time.time()
elapsed_time_seconds = end_time - start_time
elapsed_time_minutes = elapsed_time_seconds / 60

# Thời gian đã cào dữ liệu
print(f"Tổng thời gian: {elapsed_time_minutes:.2f} phút")
print(f"Tổng sản phẩm đã transform: {len(list_info_products)} sản phẩm")
print(f"Số sản phẩm transform trung bình mỗi phút: {round(len(list_info_products)/ round(elapsed_time_minutes))} sản phẩm")