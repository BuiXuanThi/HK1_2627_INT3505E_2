from flask import Flask, jsonify, request

app = Flask(__name__)

posts = [
    {
        "id": 1,
        "title": "First Post",
        "content": "Hello Flask"
    }
]


@app.route("/api/v1/posts", methods=["GET"])
def get_posts():
    return jsonify(posts)


@app.route("/api/v1/posts", methods=["POST"])
def create_post():
    data = request.get_json()

    new_post = {
        "id": len(posts) + 1,
        "title": data["title"],
        "content": data["content"]
    }

    posts.append(new_post)

    return jsonify(new_post), 201


@app.route("/api/v1/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):

    for post in posts:
        if post["id"] == post_id:
            return jsonify(post)

    return jsonify({"error": "Post not found"}), 404


@app.route("/api/v1/posts/<int:post_id>", methods=["PATCH"])
def update_post(post_id):

    data = request.get_json()

    for post in posts:

        if post["id"] == post_id:

            if "title" in data:
                post["title"] = data["title"]

            if "content" in data:
                post["content"] = data["content"]

            return jsonify(post)

    return jsonify({"error": "Post not found"}), 404


@app.route("/api/v1/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):

    for post in posts:

        if post["id"] == post_id:
            posts.remove(post)

            return jsonify({
                "message": "Deleted successfully"
            })

    return jsonify({"error": "Post not found"}), 404



@app.route("/api/v1/posts/<int:post_id>/comments", methods=["GET"])
def get_post_comments(post_id):

    return jsonify({
        "postId": post_id,
        "comments": []
    })


if __name__ == "__main__":
    app.run(debug=True)