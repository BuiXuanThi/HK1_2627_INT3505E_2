# BÀI TẬP 2: AUDIT GITHUB REST API

## 1. Giới thiệu

Trong bài tập này, em lựa chọn GitHub REST API để khảo sát và đánh giá. Đây là một API công khai được sử dụng rộng rãi trong phát triển phần mềm, cho phép truy cập và quản lý các tài nguyên như người dùng (users), kho mã nguồn (repositories), issues và pull requests thông qua giao thức HTTP.

Base URL:

```text
https://api.github.com
```

---

## 2. Phân tích một số Endpoint

### Endpoint 1: Lấy thông tin người dùng

**Method:** GET

**URL:**

```http
/users/{username}
```

**Ví dụ:**

```http
GET /users/octocat
```

**Status Code:**

* 200 OK
* 404 Not Found

**Headers thường gặp:**

* Accept: application/vnd.github+json
* Content-Type: application/json

**Đánh giá:**

Endpoint sử dụng phương thức GET để truy xuất tài nguyên người dùng, tuân thủ nguyên tắc RESTful.

---

### Endpoint 2: Lấy danh sách repository của người dùng

**Method:** GET

**URL:**

```http
/users/{username}/repos
```

**Status Code:**

* 200 OK

**Headers thường gặp:**

* Accept: application/vnd.github+json
* Content-Type: application/json

**Đánh giá:**

Tài nguyên được biểu diễn bằng danh từ số nhiều (repos), dễ hiểu và nhất quán.

---

### Endpoint 3: Tạo repository mới

**Method:** POST

**URL:**

```http
/user/repos
```

**Status Code:**

* 201 Created
* 401 Unauthorized

**Headers thường gặp:**

* Authorization: Bearer Token
* Content-Type: application/json
* Location

**Đánh giá:**

Sử dụng POST để tạo tài nguyên mới và trả về mã 201 Created. Thiết kế phù hợp với REST.

---

### Endpoint 4: Cập nhật repository

**Method:** PATCH

**URL:**

```http
/repos/{owner}/{repo}
```

**Status Code:**

* 200 OK
* 403 Forbidden
* 404 Not Found

**Headers thường gặp:**

* Authorization: Bearer Token
* Content-Type: application/json

**Đánh giá:**

PATCH được dùng để cập nhật một phần tài nguyên thay vì thay thế toàn bộ dữ liệu.

---

### Endpoint 5: Xóa repository

**Method:** DELETE

**URL:**

```http
/repos/{owner}/{repo}
```

**Status Code:**

* 204 No Content
* 403 Forbidden
* 404 Not Found

**Headers thường gặp:**

* Authorization: Bearer Token

**Đánh giá:**

DELETE được sử dụng đúng mục đích để xóa tài nguyên. Khi thành công, API trả về 204 No Content.

---

## 3. Nhận xét chung

GitHub REST API được thiết kế khá tốt theo các nguyên tắc RESTful:

* Sử dụng danh từ để biểu diễn tài nguyên.
* Sử dụng đúng HTTP Methods (GET, POST, PATCH, DELETE).
* Trả về HTTP Status Codes phù hợp với từng trường hợp.
* Sử dụng các HTTP Headers quan trọng như Accept, Content-Type, Authorization và Location.
* Endpoint được đặt tên rõ ràng, nhất quán và dễ mở rộng.

## 4. Kết luận

Qua quá trình khảo sát, có thể thấy GitHub REST API là một ví dụ điển hình của RESTful API. Việc sử dụng hợp lý tài nguyên, phương thức HTTP, status codes và headers giúp API dễ sử dụng, dễ bảo trì và thuận tiện cho việc tích hợp với các hệ thống khác.
