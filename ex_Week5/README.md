# Week 5 - Data Modeling and Resource Design

## Mô tả

Repository thực hành và bài tập Buổi 5 môn Service-Oriented Architecture (SOA).

Nội dung chính bao gồm:

- Data Modeling.
- Resource Design.
- JSON Schema.
- REST API với Flask.
- Filtering và Sorting.
- Offset Pagination.
- Cursor Pagination.
- Automated Testing.
- API Testing với Postman.

## Cấu trúc Repository

```text
ex_Week5/
├── Lab1/
├── Lab2/
├── BTVN1_Resource_Design/
├── BTVN2_Flask_Pagination/
├── .gitignore
└── README.md
```

---

# Lab 1 - Bookstore API

Thư mục:

```text
Lab1/
```

Lab 1 xây dựng REST API cơ bản cho hệ thống Bookstore bằng Flask và SQLAlchemy.

## Nội dung

Các model chính:

- Book
- Author
- Category
- User
- Review

Quan hệ giữa các resource được biểu diễn bằng SQLAlchemy ORM.

API chính:

```text
GET     /api/v1/books
GET     /api/v1/books/{id}
POST    /api/v1/books
PUT     /api/v1/books/{id}
DELETE  /api/v1/books/{id}
```

Dữ liệu gửi lên khi tạo và cập nhật Book được kiểm tra bằng JSON Schema.

Chi tiết và kết quả kiểm thử:

```text
Lab1/README.md
```

---

# Lab 2 - Filtering, Sorting and Cursor Pagination

Thư mục:

```text
Lab2/
```

Lab 2 mở rộng Bookstore API với các chức năng truy vấn dữ liệu.

## Nội dung

- Filter theo category.
- Sort theo `id` hoặc `price`.
- Sort tăng dần và giảm dần.
- Cursor pagination.
- Composite cursor sử dụng giá trị sort và `id`.

Ví dụ:

```text
GET /api/v1/books?limit=2

GET /api/v1/books?sort=price

GET /api/v1/books?sort=-price

GET /api/v1/books?category=1

GET /api/v1/books?category=1&sort=-price
```

Cursor pagination:

```text
GET /api/v1/books?limit=2&sort=-price
```

Response trả về `next` cursor để sử dụng cho request tiếp theo.

Chi tiết:

```text
Lab2/README.md
```

---

# BTVN 1 - Resource Design

Thư mục:

```text
BTVN1_Resource_Design/
```

Domain được lựa chọn:

```text
Hotel Booking
```

## Resource Set

Các resource chính:

- Hotel
- Room
- Customer
- Booking

## ERD

Hệ thống mô hình hóa các quan hệ chính:

```text
HOTEL   1 ---- N   ROOM

CUSTOMER 1 ---- N BOOKING

ROOM    1 ---- N   BOOKING
```

## REST API Design

Thiết kế gồm 16 REST API endpoints cho các resource:

```text
/api/v1/hotels
/api/v1/rooms
/api/v1/customers
/api/v1/bookings
```

Bao gồm các thao tác:

- List resources.
- Get resource by ID.
- Create resource.
- Update resource.
- Delete resource.
- Truy cập nested resources.

## JSON Schema

Ba resource chính được định nghĩa bằng JSON Schema:

```text
schemas/
├── hotel.json
├── room.json
└── booking.json
```

ERD và danh sách endpoint được trình bày trong:

```text
BTVN1_Resource_Design/report.pdf
```

Chi tiết:

```text
BTVN1_Resource_Design/README.md
```

---

# BTVN 2 - Flask Pagination

Thư mục:

```text
BTVN2_Flask_Pagination/
```

BTVN 2 mở rộng endpoint:

```text
GET /api/v1/books
```

với hai chiến lược pagination.

## Offset Pagination

Chọn bằng:

```text
?strategy=offset
```

Ví dụ:

```text
GET /api/v1/books?strategy=offset&offset=0&limit=3
```

## Cursor Pagination

Chọn bằng:

```text
?strategy=cursor
```

Ví dụ:

```text
GET /api/v1/books?strategy=cursor&limit=3&sort=price,id
```

Response trả về `next` cursor để truy vấn trang tiếp theo.

## Genre Filtering

```text
GET /api/v1/books?strategy=offset&genre=Programming
```

## Multi-key Sorting

Ví dụ:

```text
GET /api/v1/books?strategy=offset&sort=genre,price
```

Sort giảm dần:

```text
GET /api/v1/books?strategy=offset&sort=-price,-id
```

Có thể kết hợp filter và sort:

```text
GET /api/v1/books?strategy=offset&genre=Programming&sort=-price,-id
```

## Automated Tests

Tests được viết bằng pytest:

```text
BTVN2_Flask_Pagination/tests/test_books.py
```

Chạy:

```bash
pytest -v
```

Kết quả:

```text
9 passed
```

Các test kiểm tra:

- Offset pagination.
- Offset second page.
- Genre filtering.
- Multi-key sorting.
- Cursor first page.
- Cursor next page.
- Invalid strategy.
- Invalid sort.
- Invalid offset.

## Postman Collection

Postman collection:

```text
BTVN2_Flask_Pagination/postman/bookstore.postman_collection.json
```

Collection chứa các request kiểm thử offset pagination, cursor pagination, filtering, sorting và các trường hợp request không hợp lệ.

Chi tiết:

```text
BTVN2_Flask_Pagination/README.md
```

---

# Cài đặt

Tạo virtual environment tại thư mục `ex_Week5`:

```bash
python -m venv venv
```

Kích hoạt trên Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Cài đặt các thư viện cần thiết:

```bash
pip install flask flask-sqlalchemy jsonschema pytest
```

---

# Chạy các Lab và Bài tập

Ví dụ chạy Lab 1:

```bash
cd Lab1
python app.py
```

Lab 2:

```bash
cd Lab2
python app.py
```

BTVN 2:

```bash
cd BTVN2_Flask_Pagination
python app.py
```

Server Flask mặc định:

```text
http://127.0.0.1:5000
```

---

# Tổng kết

Buổi 5 tập trung vào quá trình chuyển từ mô hình dữ liệu sang thiết kế REST resource và hiện thực API.

Các nội dung đã hoàn thành:

| Phần | Nội dung | Trạng thái |
|---|---|---|
| Lab 1 | Bookstore Models, CRUD API, JSON Schema | Completed |
| Lab 2 | Filtering, Sorting, Cursor Pagination | Completed |
| BTVN 1 | Hotel Booking Resource Design | Completed |
| BTVN 2 | Offset/Cursor Pagination, Genre Filter, Multi-key Sort | Completed |
| Testing | Pytest | 9 tests passed |
| API Testing | Postman Collection | Completed |