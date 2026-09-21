PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    status TEXT DEFAULT 'pending'
);

INSERT INTO orders (id, item_name, quantity, status) VALUES
(1, 'Laptop Lenovo ThinkPad E14', 1, 'completed');

INSERT INTO orders (id, item_name, quantity, status) VALUES
(2, 'Tai nghe Sony WH-1000XM5', 2, 'pending');

INSERT INTO orders (id, item_name, quantity, status) VALUES
(3, 'SSD Samsung 990 Pro 1TB', 3, 'completed');

INSERT INTO orders (id, item_name, quantity, status) VALUES
(4, 'Bàn nâng hạ Flexispot', 1, 'pending');

INSERT INTO orders (id, item_name, quantity, status) VALUES
(5, 'Webcam Logitech C920', 2, 'completed');

DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('orders', 5);

COMMIT;