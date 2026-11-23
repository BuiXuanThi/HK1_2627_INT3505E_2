# Practice 3 – Sunset Middleware với `@deprecate_at` (RFC 8594)

## Mô tả

Decorator `@deprecate_at(sunset_date, replacement)` tự động quản lý vòng đời ngừng hỗ trợ endpoint:

| Trạng thái | Hành vi |
|---|---|
| **Chưa tới `sunset_date`** | Phục vụ bình thường + gắn headers `Sunset`, `Deprecation: true`, `Link` và ghi log `WARNING` |
| **Đã qua `sunset_date`** | Trả về `410 Gone` kèm body JSON hướng dẫn chuyển endpoint |

## Cài đặt & chạy

```bash
# Tạo môi trường ảo (tuỳ chọn)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy server
python app.py
```

Server mặc định chạy tại **http://127.0.0.1:5000**.

## Test bằng `curl`

### 1. Endpoint chưa hết hạn → `200 OK` + Sunset headers

```bash
curl -i http://127.0.0.1:5000/api/v1/users/1
```

**Kết quả mong đợi:**

- Status: `200 OK`
- Headers bao gồm:
  ```
  Sunset: Wed, 31 Dec 2026 23:59:59 GMT
  Deprecation: true
  Link: </api/v2/users>; rel="successor-version"
  ```
- Body: `{"id":1,"full_name":"Văn Nguyễn"}`
- Console server hiển thị: `WARNING  sunset  deprecated_call /api/v1/users/1 127.0.0.1`

---

### 2. Endpoint đã hết hạn → `410 Gone`

```bash
curl -i http://127.0.0.1:5000/api/v0/users/1
```

**Kết quả mong đợi:**

- Status: `410 GONE`
- Body:
  ```json
  {
    "error": "gone",
    "sunset": "Wed, 01 Jan 2025 00:00:00 GMT",
    "use_instead": "/api/v2/users"
  }
  ```

---

### 3. Endpoint mới (không deprecation) → `200 OK` bình thường

```bash
curl -i http://127.0.0.1:5000/api/v2/users/1
```

**Kết quả mong đợi:**

- Status: `200 OK`
- Không có headers `Sunset` / `Deprecation` / `Link`
- Body: `{"id":1,"first_name":"Văn","last_name":"Nguyễn","email":"a@vnu.vn"}`

---

### 4. User không tồn tại (trên endpoint chưa hết hạn)

```bash
curl -i http://127.0.0.1:5000/api/v1/users/999
```

**Kết quả mong đợi:**

- Status: `404 NOT FOUND`
- Headers `Sunset`, `Deprecation: true`, `Link` vẫn được gắn
- Body: `{"error":"not found"}`

## Cấu trúc file

```
practice3-sunset-middleware/
├── sunset.py          # Decorator @deprecate_at (tái sử dụng)
├── app.py             # Flask app demo 3 endpoint
├── requirements.txt
└── README.md
```
