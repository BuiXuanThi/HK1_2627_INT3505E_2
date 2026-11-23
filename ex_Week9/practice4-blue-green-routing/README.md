# Practice 4 – Blue-Green Routing (Flask)

## Mô tả

Endpoint duy nhất `POST /orders` đóng vai trò API Gateway, điều hướng request tới handler `v1` hoặc `v2` theo **3 tầng ưu tiên**:

| Ưu tiên | Điều kiện | Kết quả |
|---------|-----------|---------|
| 1 | Header `X-Cohort: beta` hoặc `internal` | → v2 |
| 2 | `account_id` ∈ allow-list (`acct_42`, `acct_99`) | → v2 |
| 3 | MD5 hash bucket < `V2_PERCENT` (mặc định 5%) | → v2 |

Mọi response đều gắn header `X-Order-Handler: v1` hoặc `v2`.

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

### 1. Header cohort `beta` → luôn v2

```bash
curl -i -X POST http://127.0.0.1:5000/orders \
  -H "Content-Type: application/json" \
  -H "X-Cohort: beta" \
  -d '{"account_id": "acct_1", "item": "widget"}'
```

**Kết quả mong đợi:**
- Status: `201 Created`
- Header: `X-Order-Handler: v2`
- Body chứa `"version": "v2"`, `"order_status": "confirmed"`, `"priority_processing": true`

---

### 2. Account allow-list (`acct_42`) → luôn v2

```bash
curl -i -X POST http://127.0.0.1:5000/orders \
  -H "Content-Type: application/json" \
  -d '{"account_id": "acct_42", "item": "gadget"}'
```

**Kết quả mong đợi:**
- Status: `201 Created`
- Header: `X-Order-Handler: v2`

---

### 3. Account bình thường (`acct_100`) ở `V2_PERCENT=5` → v1

```bash
curl -i -X POST http://127.0.0.1:5000/orders \
  -H "Content-Type: application/json" \
  -d '{"account_id": "acct_100", "item": "thing"}'
```

**Kết quả mong đợi:**
- Status: `200 OK`
- Header: `X-Order-Handler: v1`
- Body chứa `"version": "v1"`, `"status": "created"`

---

### 4. Tăng `V2_PERCENT=100` rồi gọi lại → v2

```bash
# Bước 4a: Cập nhật cấu hình
curl -i -X POST http://127.0.0.1:5000/admin/config \
  -H "Content-Type: application/json" \
  -d '{"v2_percent": 100}'

# Bước 4b: Gọi lại với cùng account
curl -i -X POST http://127.0.0.1:5000/orders \
  -H "Content-Type: application/json" \
  -d '{"account_id": "acct_100", "item": "thing"}'
```

**Kết quả mong đợi (bước 4b):**
- Status: `201 Created`
- Header: `X-Order-Handler: v2`

## Cấu trúc file

```
practice4-blue-green-routing/
├── handlers.py        # Business logic v1 & v2
├── gateway.py         # Logic định tuyến 3 tầng
├── app.py             # Flask app + admin endpoint
├── requirements.txt
└── README.md
```
