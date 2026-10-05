# Lab 3 - Orders Pagination API

## Filter

Request:

```bash
curl -i "http://localhost:5000/orders?status=paid"
```

![alt text](image-1.png)

---

## Customer Filter

Request:

```bash
curl -i "http://localhost:5000/orders?customer_id=2"
```

![alt text](image-2.png)

---

## Cursor Pagination

Request:

```bash
curl -i "http://localhost:5000/orders?cursor=3"
```

![alt text](image-3.png)

---

## Sort

Request:

```bash
curl -i "http://localhost:5000/orders?sort=-total"
```

![alt text](image-4.png)

---

## Sparse Fieldsets

Request:

```bash
curl -i "http://localhost:5000/orders?fields=id,total"
```

![alt text](image-5.png)

---

## Invalid Cursor (400 Bad Request)

Request:

```bash
curl -i "http://localhost:5000/orders?cursor=abc"
```

Expected Status:

```http
HTTP/1.1 400 BAD REQUEST
```
![alt text](image-6.png)