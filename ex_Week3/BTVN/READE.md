## 3. Status Codes Usage

Spotify Web API sử dụng HTTP status codes một cách nhất quán và đúng ngữ nghĩa RESTful.

### Success Responses

- **200 OK**: Request được xử lý thành công và trả về dữ liệu.
  - Ví dụ: `GET /me`, `GET /playlists/{playlist_id}`.

- **201 Created**: Tài nguyên mới được tạo thành công.
  - Ví dụ: `POST /users/{user_id}/playlists` tạo playlist mới.

- **204 No Content**: Request thành công nhưng không cần trả về dữ liệu.
  - Ví dụ: xóa bài hát khỏi playlist hoặc hủy theo dõi một nghệ sĩ.

### Client Error Responses

- **400 Bad Request**: Request không hợp lệ hoặc tham số sai định dạng.
- **401 Unauthorized**: Thiếu hoặc token xác thực không hợp lệ.
- **403 Forbidden**: Người dùng đã xác thực nhưng không có quyền thực hiện thao tác.
- **404 Not Found**: Không tìm thấy tài nguyên được yêu cầu.
- **429 Too Many Requests**: Vượt quá giới hạn tốc độ (rate limiting).

### Server Error Responses

- **500 Internal Server Error**: Lỗi phía máy chủ.
- **502/503 Service Unavailable**: Dịch vụ tạm thời không khả dụng.

### Assessment

Spotify sử dụng status codes phù hợp với chuẩn HTTP và RESTful API. Các mã phản hồi phản ánh chính xác kết quả xử lý của request, giúp client dễ dàng phát hiện và xử lý lỗi.

---

## 4. Idempotency

Idempotency là tính chất mà việc thực hiện cùng một request nhiều lần sẽ tạo ra cùng một trạng thái cuối cùng của hệ thống.

### Idempotent Operations

#### GET

Ví dụ:

```http
GET /playlists/{playlist_id}
```

Việc gọi nhiều lần chỉ đọc dữ liệu và không làm thay đổi trạng thái hệ thống.

#### PUT

Ví dụ:

```http
PUT /playlists/{playlist_id}/followers
```

Thao tác theo dõi (follow) một playlist.

Nếu người dùng đã follow playlist, việc gửi lại cùng request nhiều lần vẫn dẫn đến trạng thái cuối cùng là:

```text
User follows the playlist.
```

#### DELETE

Ví dụ:

```http
DELETE /playlists/{playlist_id}/followers
```

Thao tác hủy theo dõi playlist.

Dù request được gửi nhiều lần, trạng thái cuối cùng vẫn là:

```text
User does not follow the playlist.
```

### Non-Idempotent Operations

#### POST

Ví dụ:

```http
POST /users/{user_id}/playlists
```

Mỗi request tạo một playlist mới.

Nếu gửi cùng request nhiều lần, nhiều playlist khác nhau sẽ được tạo ra.

Do đó thao tác này không idempotent.

### Assessment

Spotify Web API thể hiện rõ sự khác biệt giữa các thao tác đọc, cập nhật và tạo mới tài nguyên. Các endpoint GET, PUT và DELETE nhìn chung tuân thủ nguyên tắc idempotency, trong khi các endpoint POST dùng để tạo tài nguyên mới là non-idempotent. Thiết kế này phù hợp với các nguyên tắc RESTful API và giúp hệ thống hoạt động ổn định trong môi trường mạng có thể xảy ra retry request.