# Crawl-Shopee
## Test 1:  Crawl tất cả các sản phẩm thuộc các nhóm hàng lớn liệt kê ở trang chủ của shopee.vn
- Các thông số đạt được:
    - Tổng thời gian: 23.36 phút
    - Tổng sản phẩm đã cào trong json: 146211 sản phẩm
    - Mỗi phút cào được: 6259 sản phẩm
- Quy trình:
    - Bước 1: Thu thập các đường dẫn của các danh mục chính (file code: get_category_info.py). Output của file này là csv gồm
