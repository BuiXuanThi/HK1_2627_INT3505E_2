# BTVN 1 - Resource Design

## Domain

**Hotel Booking**

Bài tập thiết kế resource cho hệ thống đặt phòng khách sạn.

## Nội dung

Bài làm gồm:

- ERD cho hệ thống Hotel Booking.
- Xác định các resource chính.
- Thiết kế danh sách REST API endpoints.
- JSON Schema cho 3 resource chính.

## Resource Set

Các resource chính:

- `hotels`
- `rooms`
- `customers`
- `bookings`

## API Design

Hệ thống gồm **16 endpoints** cho các thao tác với Hotel, Room, Customer và Booking.

Danh sách endpoint và ERD được trình bày chi tiết trong:

```text
report.pdf
```

## JSON Schema

Ba resource chính được định nghĩa bằng JSON Schema:

```text
schemas/
├── hotel.json
├── room.json
└── booking.json
```

Các schema định nghĩa cấu trúc dữ liệu, required fields và các validation constraints cơ bản.

## Cấu trúc thư mục

```text
BTVN1_Resource_Design/
├── README.md
├── report.pdf
└── schemas/
    ├── hotel.json
    ├── room.json
    └── booking.json
```

## Kết quả

Hoàn thành Resource Design cho domain Hotel Booking với ERD, 16 REST API endpoints và JSON Schema cho các resource chính.