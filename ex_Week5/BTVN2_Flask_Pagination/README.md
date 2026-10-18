# BTVN 2 - Flask Pagination

## Mô tả

Hoàn thiện API `GET /api/v1/books` với các chức năng:

- Offset pagination.
- Cursor pagination.
- Lựa chọn pagination strategy bằng `?strategy=...`.
- Filter theo `genre`.
- Multi-key sorting.
- Automated tests với pytest.
- Postman collection để kiểm thử API.

## Cấu trúc thư mục

```text
BTVN2_Flask_Pagination/
├── app.py
├── models.py
├── README.md
├── routes/
│   └── books.py
├── tests/
│   └── test_books.py
├── postman/
│   └── bookstore.postman_collection.json
└── images/
    ├── offset-pagination.png
    ├── cursor-first-page.png
    ├── cursor-next-page.png
    ├── genre-multikey-sort.png
    └── pytest-tests.png
```

## Cài đặt

Từ virtual environment của project, cài các thư viện cần thiết:

```bash
pip install flask flask-sqlalchemy pytest
```

## Chạy ứng dụng

```bash
python app.py
```

Server chạy tại:

```text
http://127.0.0.1:5000
```

Endpoint chính:

```text
GET /api/v1/books
```

---

## 1. Offset Pagination

Sử dụng:

```text
?strategy=offset
```

Ví dụ:

```bash
curl.exe -i "http://127.0.0.1:5000/api/v1/books?strategy=offset&offset=0&limit=3"
```

Trang tiếp theo:

```bash
curl.exe -i "http://127.0.0.1:5000/api/v1/books?strategy=offset&offset=3&limit=3"
```

Response chứa thông tin pagination:

```json
{
  "page": {
    "strategy": "offset",
    "offset": 0,
    "limit": 3,
    "total": 10
  }
}
```

### Kết quả kiểm thử trên Postman

![alt text](image.png)

---

## 2. Cursor Pagination

Sử dụng:

```text
?strategy=cursor
```

Request trang đầu:

```bash
curl.exe -i "http://127.0.0.1:5000/api/v1/books?strategy=cursor&limit=3&sort=price,id"
```

Response trả về `next` cursor:

```json
{
  "page": {
    "strategy": "cursor",
    "limit": 3,
    "next": "...",
    "more": true
  }
}
```

### Cursor - First Page

![alt text](image-1.png)

Sử dụng giá trị `next` cho request tiếp theo:

```text
GET /api/v1/books?strategy=cursor&limit=3&sort=price,id&cursor=<next_cursor>
```

Cursor lưu các giá trị sort cần thiết để tiếp tục lấy dữ liệu từ vị trí của trang trước.

### Cursor - Next Page
![alt text](image-2.png)

---

## 3. Filter theo Genre

Sử dụng query parameter:

```text
?genre=Programming
```

Ví dụ:

```bash
curl.exe -i "http://127.0.0.1:5000/api/v1/books?strategy=offset&genre=Programming"
```

API chỉ trả về các book có:

```json
"genre": "Programming"
```

---

## 4. Multi-key Sorting

Các trường hỗ trợ sort:

```text
id
title
price
genre
```

Sort tăng dần:

```text
?sort=genre,price
```

Ví dụ:

```bash
curl.exe -i "http://127.0.0.1:5000/api/v1/books?strategy=offset&sort=genre,price"
```

Sort giảm dần sử dụng dấu `-`:

```text
?sort=-price,-id
```

Ví dụ:

```bash
curl.exe -i "http://127.0.0.1:5000/api/v1/books?strategy=offset&sort=-price,-id"
```

Có thể kết hợp filter và multi-key sort:

```bash
curl.exe -i "http://127.0.0.1:5000/api/v1/books?strategy=offset&genre=Programming&sort=-price,-id"
```

### Kết quả Filter + Multi-key Sort

![alt text](image-3.png)

---

## 5. Validation

Strategy không hợp lệ:

```bash
curl.exe -i "http://127.0.0.1:5000/api/v1/books?strategy=abc"
```

Response:

```text
HTTP 400
```

Sort field không được hỗ trợ:

```bash
curl.exe -i "http://127.0.0.1:5000/api/v1/books?strategy=offset&sort=foo"
```

Response:

```text
HTTP 400
```

---

## 6. Automated Tests

Các test được đặt trong:

```text
tests/test_books.py
```

Chạy:

```bash
pytest -v
```

Các trường hợp được kiểm thử:

- Offset pagination.
- Offset second page.
- Genre filtering.
- Multi-key sorting.
- Cursor first page.
- Cursor next page.
- Invalid strategy.
- Invalid sort.
- Invalid offset.

Kết quả:

```text
9 passed
```

### Kết quả Pytest

![Pytest Results](images/pytest-tests.png)

---

## 7. Postman Collection

Postman collection được lưu tại:

```text
postman/bookstore.postman_collection.json
```

Collection bao gồm các request kiểm thử:

1. Offset Pagination
2. Offset Second Page
3. Filter by Genre
4. Multi-key Sort
5. Cursor First Page
6. Cursor Next Page
7. Genre + Multi-key Sort
8. Invalid Strategy
9. Invalid Sort

Request `Cursor First Page` tự động lưu giá trị `next` vào collection variable `cursor`.

Request `Cursor Next Page` sử dụng:

```text
{{cursor}}
```

để lấy trang tiếp theo.

---

## Kết quả

API `GET /api/v1/books` đã hỗ trợ:

- Offset pagination.
- Cursor pagination.
- Genre filtering.
- Multi-key sorting.
- Validation cho query parameters.
- Automated testing bằng pytest.
- API testing bằng Postman collection.