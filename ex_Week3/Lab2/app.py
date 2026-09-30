from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.ERROR)


class ProblemError(Exception):

    def __init__(
        self,
        status,
        title,
        detail,
        type="about:blank"
    ):
        self.status = status
        self.title = title
        self.detail = detail
        self.type = type


@app.errorhandler(ProblemError)
def handle_problem_error(error):

    response = {
        "type": error.type,
        "title": error.title,
        "detail": error.detail,
        "status": error.status,
        "instance": request.path
    }

    return jsonify(response), error.status


@app.errorhandler(HTTPException)
def handle_http_exception(error):

    response = {
        "type": "about:blank",
        "title": error.name,
        "detail": error.description,
        "status": error.code,
        "instance": request.path
    }

    return jsonify(response), error.code


@app.errorhandler(Exception)
def handle_unexpected_error(error):

    app.logger.exception(error)

    response = {
        "type": "about:blank",
        "title": "Internal Server Error",
        "detail": "An unexpected error occurred.",
        "status": 500,
        "instance": request.path
    }

    return jsonify(response), 500


resources = {
    1: "Laptop",
    2: "Phone"
}


@app.route("/resources/<int:resource_id>")
def get_resource(resource_id):

    if resource_id not in resources:

        raise ProblemError(
            status=404,
            title="Resource Not Found",
            detail=f"Resource {resource_id} does not exist."
        )

    return jsonify({
        "id": resource_id,
        "name": resources[resource_id]
    })


@app.route("/boom")
def boom():

    x = 1 / 0

    return str(x)


if __name__ == "__main__":
    app.run(debug=True)