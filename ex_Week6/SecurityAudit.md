# Security Audit – Social Network API

## 1. Lộ Password

**Rủi ro:**  
Endpoint `POST /auth/login` nhận `email` và `password` của người dùng. Nếu API không sử dụng `HTTPS`, thông tin đăng nhập có thể bị lộ trong quá trình truyền dữ liệu.

**Cách giảm thiểu:**
- Luôn sử dụng `HTTPS/TLS`.
- Không ghi `password` vào log.
- Lưu password bằng các thuật toán `Password Hashing` an toàn như `Argon2id`, `bcrypt` hoặc `PBKDF2`.
- Không lưu password dưới dạng `plaintext`.

---

## 2. Brute-Force Login

**Rủi ro:**  
Attacker có thể liên tục gửi request tới `POST /auth/login` để thử nhiều password khác nhau.

**Cách giảm thiểu:**
- Áp dụng `Rate Limiting` cho endpoint login.
- Trả về `429 Too Many Requests` khi vượt quá giới hạn.
- Sử dụng thông báo lỗi chung để tránh tiết lộ một email có tồn tại trong hệ thống hay không.

---

## 3. Lộ Access Token

**Rủi ro:**  
Nếu `Access Token` bị lộ qua log, cách lưu trữ không an toàn hoặc quá trình truyền dữ liệu, attacker có thể sử dụng token để truy cập các protected resources.

**Cách giảm thiểu:**
- Không ghi `Access Token` vào log.
- Luôn sử dụng `HTTPS`.
- Sử dụng `Access Token` có thời gian sống ngắn.
- Không lưu thông tin nhạy cảm trong `JWT Payload`.

---

## 4. Refresh Token bị đánh cắp

**Rủi ro:**  
`Refresh Token` thường có thời gian sống dài. Nếu bị đánh cắp, attacker có thể sử dụng nó để liên tục xin `Access Token` mới.

**Cách giảm thiểu:**
- Lưu `Refresh Token` an toàn.
- Thiết lập thời gian hết hạn (`Expiration`).
- Hỗ trợ `Token Revocation`.
- Sử dụng `Refresh Token Rotation` khi phù hợp.
- Khi logout, vô hiệu hóa `Refresh Token` nếu hệ thống yêu cầu logout có hiệu lực ngay.

---

## 5. Không kiểm tra Scope

**Rủi ro:**  
Endpoint `GET /posts/{id}` yêu cầu scope `posts:read`. Nếu server chỉ kiểm tra `Access Token` hợp lệ mà không kiểm tra `Scope`, một client không đủ quyền vẫn có thể đọc post.

**Cách giảm thiểu:**

Server phải kiểm tra:

`Valid Access Token + Required Scope (posts:read)`

trước khi cho phép truy cập resource.

---

## 6. Broken Object Level Authorization (BOLA)

**Rủi ro:**  
Người dùng có thể thay đổi ID của resource trên URL, ví dụ:

`GET /posts/15`

thành:

`GET /posts/16`

Có `Access Token` hợp lệ và scope `posts:read` không đồng nghĩa với việc user được phép truy cập mọi post, nếu hệ thống có các post bị giới hạn bởi owner hoặc visibility.

**Cách giảm thiểu:**
- Thực hiện `Object-Level Authorization` với các resource bị giới hạn truy cập.
- Kiểm tra quan hệ giữa authenticated user và post được yêu cầu.
- Không chỉ dựa vào ID mà client gửi lên.

---

## 7. Kiểm tra JWT không đầy đủ

**Rủi ro:**  
Attacker có thể sử dụng JWT đã hết hạn, bị chỉnh sửa hoặc được phát hành không đúng cho API.

**Cách giảm thiểu:**
- Kiểm tra `JWT Signature`.
- Kiểm tra claim `exp`.
- Kiểm tra `iss` và `aud` khi hệ thống sử dụng các claim này.
- Chỉ chấp nhận các `Signing Algorithm` được cho phép.
- Kiểm tra token có bị `revoked` hay không nếu hệ thống hỗ trợ `Revocation`.

---

## 8. Lộ thông tin qua Error Response

**Rủi ro:**  
Error response quá chi tiết có thể làm lộ thông tin như tài khoản có tồn tại hay không, chi tiết quá trình kiểm tra token, `Stack Trace` hoặc thông tin triển khai bên trong server.

**Cách giảm thiểu:**
- Sử dụng thông báo lỗi chung cho các lỗi authentication.
- Không trả `Stack Trace` hoặc internal exception cho client.
- Thông tin phục vụ debug chỉ nên được lưu trong server log được bảo vệ.

---

## Tổng kết

Các rủi ro bảo mật chính được xác định:

1. Lộ `Password`.
2. `Brute-Force Login`.
3. Lộ `Access Token`.
4. `Refresh Token` bị đánh cắp.
5. Thiếu kiểm tra `Scope`.
6. `Broken Object Level Authorization (BOLA)`.
7. Kiểm tra `JWT` không đầy đủ.
8. Lộ thông tin qua `Error Response`.

API cần kết hợp `Authentication`, `Scope-Based Authorization`, `Object-Level Authorization`, `HTTPS`, `Rate Limiting`, `Secure Token Handling` và `Password Hashing` để giảm thiểu các rủi ro trên.