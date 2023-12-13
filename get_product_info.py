# Import các thư viện cần thiết
import requests
import json
import pandas as pd
import time

#Thời gian bắt đầu
start_time = time.time()
headers = {
  'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
}
# Hàm requets api của shopee 
def request_get_product(headers, category_id, category_level, offset):
  url = f"https://shopee.vn/api/v4/recommend/recommend?bundle=category_landing_page&cat_level={category_level}&catid={category_id}&limit=60&offset={offset}"
  r = requests.get(url, headers=headers)
  if r.status_code == 200:
    data = r.json()
    return data
  else:
    return False

# Hàm ghi file json
def write_file_js(json_data, js_file_path):
  # Mở file json với đường dẫn js_file_path và ghi dữ liệu từ json_data
  with open(js_file_path, 'w', encoding='utf-8') as js_file:
      js_file.write(str(json_data))
      js_file.close()
  print(f'Done file {js_file_path}')
df_all_category = pd.read_csv('all_category_levels_info.csv')

num_products = 0
for idx, row in df_all_category.iterrows():
  page = 1
  offset = 0
  has_next_page = True
  while has_next_page:
    response_json = request_get_product(headers, category_id = row['category_id'], category_level =row['category_level'], offset = offset)
    if response_json:
      data_items = response_json['data']['sections'][0]['data']['item']
      if data_items:
        js_file_path = f'data_products_js\{row["category_id"]}_{page}.js'
        write_file_js(json_data = data_items, js_file_path = js_file_path)
        num_products += len(data_items)
    if str(response_json['data']['sections'][0]['has_more']) == 'True':
      page += 1
      offset += 60
    else:
      has_next_page = False
  print(f"Done category {row['display_name']}")

#Thời gian kết thúc
end_time = time.time()
elapsed_time_seconds = end_time - start_time
elapsed_time_minutes = elapsed_time_seconds / 60

# Thời gian đã cào dữ liệu
print(f"Tổng thời gian: {elapsed_time_minutes:.2f} phút")
print(f"Tổng sản phẩm đã cào trong json: {num_products} sản phẩm")