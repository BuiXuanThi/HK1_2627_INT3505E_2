from flask import Flask

from models import db, Book
from routes.books import bp


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookstore.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

        # Seed sample data only when database is empty
        if not db.session.query(Book).first():
            seed_books()

    return app


def seed_books():
    books = [
        Book(
            title="Clean Code",
            isbn="9780132350884",
            genre="Programming",
            price_vnd=450000,
            stock=10
        ),
        Book(
            title="Design Patterns",
            isbn="9780201633610",
            genre="Programming",
            price_vnd=520000,
            stock=8
        ),
        Book(
            title="Fluent Python",
            isbn="9781492056355",
            genre="Programming",
            price_vnd=600000,
            stock=6
        ),
        Book(
            title="Effective Java",
            isbn="9780134685991",
            genre="Programming",
            price_vnd=550000,
            stock=9
        ),
        Book(
            title="Database System Concepts",
            isbn="9780078022159",
            genre="Database",
            price_vnd=700000,
            stock=5
        ),
        Book(
            title="SQL Fundamentals",
            isbn="9780136788046",
            genre="Database",
            price_vnd=350000,
            stock=12
        ),
        Book(
            title="Learning SQL",
            isbn="9781492057611",
            genre="Database",
            price_vnd=400000,
            stock=7
        ),
        Book(
            title="Computer Networks",
            isbn="9780132126953",
            genre="Networking",
            price_vnd=650000,
            stock=4
        ),
        Book(
            title="Network Warrior",
            isbn="9781449387860",
            genre="Networking",
            price_vnd=500000,
            stock=6
        ),
        Book(
            title="HTTP The Definitive Guide",
            isbn="9781565925090",
            genre="Networking",
            price_vnd=480000,
            stock=3
        )
    ]

    db.session.add_all(books)
    db.session.commit()


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)