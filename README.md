# Crawl-Shopee
## Test 1:  Crawl tất cả các sản phẩm thuộc các nhóm hàng lớn liệt kê ở trang chủ của shopee.vn
- Các thông số đạt được:
    - Tổng thời gian: 23.36 phút
    - Tổng sản phẩm đã cào trong json: 146211 sản phẩm
    - Mỗi phút cào được: 6259 sản phẩm
- Quy trình:
    - Bước 1: Thu thập các đường dẫn của các danh mục chính *(file code: get_category_info.py)*. Output của bước này là file **category_info.csv** chứa các trường dữ liệu như sau:
                            <img src="https://i.imgur.com/cSNLjoW.png">
    - Bước 2: Thu thập các danh mục con của từng danh mục chính qua api của shopee *(file code: transform_catid_lv2.ipynb)*. Output của bước này là file **all_category_levels_info.csv** chứa đầy đủ các category cấp 1 và 2:
                            <img src="https://i.imgur.com/8VIkAkF.png">
    - Bước 3: Requests các trang sản phẩm của từng category ở file csv của bước 2, dùng api public của Shopee. Lưu trữ từng file json chứa dữ liệu của các sản phẩm trả về vào thư mục **[data_products_js](https://drive.google.com/drive/folders/1bbj4Jcru2xb9AIHVxb1SWKCash6pncXD?usp=sharing)**:

## Test 2: Transform dữ liệu đã lấy được ra định dạng csv và excel với cấu trúc dưới đây:
- Các thông số đạt được:
    - Tổng thời gian: 3.38 phút
    - Tổng sản phẩm đã transform: 146211 sản phẩm
    - Số sản phẩm transform trung bình mỗi phút: 48737 sản phẩm
