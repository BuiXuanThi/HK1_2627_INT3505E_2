# Homework ý 1 - Bổ sung /orders

## Cursor Test

```bash
curl -i "http://localhost:5000/orders?cursor=3"
```
![alt text](image.png)

---

## Invalid Cursor Test

```bash
curl -i "http://localhost:5000/orders?cursor=abc"
```

![alt text](image-1.png)

---

## Sort Test

```bash
curl -i "http://localhost:5000/orders?sort=-total"
```

![alt text](image-2.png)