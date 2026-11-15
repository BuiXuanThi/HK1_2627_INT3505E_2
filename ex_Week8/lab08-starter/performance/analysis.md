# Lab 4 — Phân tích kết quả

| Kịch bản | Users | Spawn rate | Duration | p95 (ms) | Failure rate | RPS |
| A | 10 | 2 | 30s | 18 | 0.00% (0/137) | 4.71 |
| B | 50 | 5 | 60s | 19 | 0.00% (0/1384) | 23.31 |
| C | 200 | 50 | 30s | 83 | 0.21% (6/2835) | 97.23 |

1. Kịch bản có p95 cao nhất là gì? Dùng số liệu quan sát để giải thích.

**Trả lời:** Kịch bản C (200 users) có p95 cao nhất: 83 ms, so với 19 ms ở B và 18 ms ở A.

| Endpoint | p95 A (ms) | p95 B (ms) | p95 C (ms) |
|---|---:|---:|---:|
| GET /books | 17 | 15 | 97 |
| GET /books/{id} | 17 | 17 | 73 |
| GET /books?year={year} | 18 | 11 | 54 |
| POST /books | 47 | 25 | 66 |

Quan sát từ số liệu:
- Từ A lên B (10 → 50 users) p95 gần như không đổi (18 → 19 ms), và RPS tăng gần tuyến tính theo users (4.71 → 23.31 → 97.23, tức tăng khoảng 20.6 lần khi users tăng 20 lần). Ở mức 50 users chưa thấy dấu hiệu quá tải.
- Ở C, p95 tăng khoảng 4.6 lần so với A (83/18) và phần đuôi dài ra: p99 từ 33 ms (A) và 26 ms (B) lên 160 ms, max từ 47 ms và 45 ms lên 240 ms.
- Median gần như không đổi (p50 lần lượt 5, 6, 7 ms ở A, B, C). Phần lớn request vẫn nhanh, chỉ một nhóm nhỏ request chậm hơn nhiều.
- Cả bốn endpoint đều tăng p95 ở C, kể cả các GET chỉ đọc, nên độ chậm không gắn với riêng một endpoint.
- POST /books có median cao hơn các endpoint còn lại ở cả ba kịch bản (17, 12, 14 ms so với khoảng 4-7 ms).

Giả thuyết (chưa kiểm chứng): 200 users được tạo trong khoảng 4 giây (spawn rate 50/s) làm nhiều request đến cùng lúc trên Flask development server; Locust và server tranh CPU trên cùng một máy; SQLite xử lý ghi tuần tự nên POST chậm hơn. Cách xác nhận: xem biểu đồ response time theo thời gian trong `reports/C.html` (nếu p95 cao tập trung ở vài giây đầu thì ramp-up là nguyên nhân chính), chạy lại C với spawn rate thấp hơn, và theo dõi CPU của máy trong lúc chạy.

2. Endpoint nào tăng failure rate? Phân biệt lỗi HTTP thực và lỗi đánh dấu trong Locust.

**Trả lời:** Chỉ có `GET /books?year={year}` ở kịch bản C có lỗi: 6 lỗi trên 414 request (1.45%). Kịch bản A và B không có lỗi nào, và các endpoint còn lại không có lỗi ở cả ba kịch bản. File `C_failures.csv` ghi cả 6 lỗi cùng một loại: `Injected failure (client-side, simulated 500)`.

Phân biệt hai loại lỗi:
- **Lỗi HTTP thực:** server trả status 5xx, hoặc có timeout/lỗi kết nối; Locust tự ghi nhận là failure. Trong cả ba lần chạy không có lỗi nào thuộc loại này.
- **Lỗi đánh dấu trong Locust:** task `search_by_year` gọi `response.failure(...)` ngẫu nhiên khoảng 1% sau khi server đã trả HTTP 200. Đây là lỗi giả lập phía client, không phải HTTP 500 của server, dù message có chữ "500".

Failure rate không tăng theo số users. Tổng cộng có 633 request search (17 + 202 + 414) và 6 lỗi, tức 0.95%, phù hợp với tỉ lệ cố định 1% trong code. Ở A và B gộp lại có 219 request search và 0 lỗi; nếu tỉ lệ là 1% thì khả năng không có lỗi nào khoảng 11%, không bất thường. Việc lỗi chỉ xuất hiện ở C là vì C có nhiều request search hơn nhiều, không chứng tỏ server lỗi nhiều hơn khi tải cao. Tỉ lệ 0.21% của C (6/2835) cũng không phản ánh chất lượng server, vì chỉ một trong bốn endpoint có lỗi giả lập.

3. Với SLO giả định p95 < 300 ms, kịch bản nào đạt? Nêu giới hạn của phép đo.

**Trả lời:** Cả ba kịch bản đều đạt: p95 tổng hợp là 18, 19 và 83 ms. p95 cao nhất của một endpoint riêng lẻ là 97 ms (`GET /books` ở C), và request chậm nhất trong cả ba lần chạy là 240 ms (C), vẫn dưới 300 ms. Kết luận này chỉ đúng cho thí nghiệm này, vì các giới hạn sau:
- Locust và server chạy trên cùng một máy (127.0.0.1), tranh nhau CPU và không có độ trễ mạng.
- API chạy trên Flask development server với SQLite, không phải cấu hình production, nên không suy ra được SLO production.
- Mỗi kịch bản chỉ chạy một lần, 30-60 giây, không lặp lại nên không ước lượng được độ biến thiên giữa các lần chạy. Ở A, mỗi endpoint chỉ có 17-56 request, và p95 gần bằng giá trị lớn nhất (POST /books có p95 = p99 = max = 47 ms).
- Mô hình tải là closed-loop với `wait_time` 1-3 giây nên RPS bị quyết định bởi thời gian nghỉ của user ảo (RPS xấp xỉ users chia 2: 4.71, 23.31, 97.23 so với 5, 25, 100), không phải bởi năng lực server. Chưa kịch bản nào làm server bão hòa, nên chưa biết ngưỡng chịu tải.
- Mỗi lần chạy bao gồm cả giai đoạn tăng user (ramp-up); percentile do Locust tính và làm tròn các giá trị lớn.
- Không theo dõi CPU/RAM của máy trong lúc chạy nên không có tín hiệu saturation.
4. Nếu connection pool bị giới hạn ở 5, bạn sẽ kiểm chứng ảnh hưởng như thế nào?

> Không điền số liệu giả định vào bảng. Không khẳng định hiệu năng production
> từ SQLite + Flask development server trên máy cá nhân.
