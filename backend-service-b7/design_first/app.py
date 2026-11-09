
import connexion

app = connexion.FlaskApp(
    __name__,
    specification_dir="openapi"
)

app.add_api(
    "products.yaml",
    validate_responses=True,
    strict_validation=True
)

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001
    )
