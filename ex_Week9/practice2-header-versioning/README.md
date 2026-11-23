# Practice 2 – Header Versioning với `@api_version` (Flask)

## Mô tả

Endpoint duy nhất `GET /users/<uid>` phục vụ đồng thời **3 phiên bản** API (`1`, `2`, `2024-06-20`).  
Client chọn phiên bản qua header **`X-API-Version`**; server phản hồi kèm header **`X-API-Version-Served`**.

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

### 1. Không gửi header → mặc định v2

```bash
curl -i http://127.0.0.1:5000/users/1
```

**Kết quả mong đợi:**  
- Status `200`  
- Header `X-API-Version-Served: 2`  
- Body: `{"id":1,"first_name":"Văn","last_name":"Nguyễn","email":"a@vnu.vn"}`

---

### 2. Gửi `X-API-Version: 1` → schema v1 (full_name)

```bash
curl -i -H "X-API-Version: 1" http://127.0.0.1:5000/users/1
```

**Kết quả mong đợi:**  
- Status `200`  
- Header `X-API-Version-Served: 1`  
- Body: `{"id":1,"full_name":"Văn Nguyễn"}`

---

### 3. Gửi `X-API-Version: 2024-06-20` → schema v2

```bash
curl -i -H "X-API-Version: 2024-06-20" http://127.0.0.1:5000/users/1
```

**Kết quả mong đợi:**  
- Status `200`  
- Header `X-API-Version-Served: 2024-06-20`  
- Body: `{"id":1,"first_name":"Văn","last_name":"Nguyễn","email":"a@vnu.vn"}`

---

### 4. Gửi version không hỗ trợ → 400 Bad Request

```bash
curl -i -H "X-API-Version: 99" http://127.0.0.1:5000/users/1
```

**Kết quả mong đợi:**  
- Status `400`  
- Body: `{"error":"unsupported version"}`
