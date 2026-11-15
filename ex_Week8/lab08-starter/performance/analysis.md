# Lab 4 — Phân tích kết quả

| Kịch bản | Users | Spawn rate | Duration | p95 (ms) | Failure rate | RPS |
| A | 10 | 2 | 30s | 18 | 0.00% (0/137) | 4.71 |
| B | 50 | 5 | 60s | 19 | 0.00% (0/1384) | 23.31 |
| C | 200 | 50 | 30s | 83 | 0.21% (6/2835) | 97.23 |

1. Kịch bản có p95 cao nhất là gì? Dùng số liệu quan sát để giải thích.
2. Endpoint nào tăng failure rate? Phân biệt lỗi HTTP thực và lỗi đánh dấu trong Locust.
3. Với SLO giả định p95 < 300 ms, kịch bản nào đạt? Nêu giới hạn của phép đo.
4. Nếu connection pool bị giới hạn ở 5, bạn sẽ kiểm chứng ảnh hưởng như thế nào?

> Không điền số liệu giả định vào bảng. Không khẳng định hiệu năng production
> từ SQLite + Flask development server trên máy cá nhân.
