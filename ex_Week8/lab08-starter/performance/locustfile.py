"""Lab 4: weighted tasks, optional 404, no deliberate server errors.

search_by_year chứa 1% lỗi GIẢ LẬP phía client (Locust response.failure()),
KHÔNG phải HTTP 500 do server phát. Server không bị sửa.

Run: locust -f performance/locustfile.py --headless -H http://127.0.0.1:5000 \
         -u 10 -r 2 -t 30s --html reports/A.html
"""
import itertools
import random

from locust import HttpUser, between, task

_counter = itertools.count(1)

# Tỉ lệ lỗi GIẢ LẬP của task search_by_year (1%)
# Đây là lỗi phía CLIENT do Locust đánh dấu bằng response.failure(),
# KHÔNG phải HTTP 500 do Flask trả về
INJECTED_FAILURE_RATE = 0.01


class BooksUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def list_books(self):
        self.client.get("/books", name="GET /books")

    @task(2)
    def read_book(self):
        book_id = random.randint(1, 50)
        with self.client.get(
            f"/books/{book_id}", name="GET /books/{id}", catch_response=True
        ) as response:
            # Expected 404 (random id absent) is not an operational failure
            if response.status_code in (200, 404):
                response.success()
            else:
                response.failure(f"Unexpected status {response.status_code}")

    @task(1)
    def create_book(self):
        unique = next(_counter)
        self.client.post(
            "/books",
            json={"title": f"Load test {unique}", "author": "locust"},
            name="POST /books",
        )

    @task(1)
    def search_by_year(self):
        year = random.randint(1990, 2024)
        # name= gộp mọi năm vào 1 dòng thống kê duy nhất trong báo cáo Locust
        with self.client.get(
            "/books",
            params={"year": year},
            name="GET /books?year={year}",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                # Lỗi THẬT: server trả status khác 200.
                response.failure(f"Unexpected status {response.status_code}")
            elif random.random() < INJECTED_FAILURE_RATE:
                # Lỗi GIẢ LẬP: server vẫn trả 200, nhưng Locust ghi nhận là fail
                # Trong bảng "Failures" sẽ thấy đúng chuỗi message bên dưới
                response.failure("Injected failure (client-side, simulated 500)")
            else:
                response.success()