from flask import Flask, request, jsonify
import search

app = Flask(__name__)


@app.route("/")
def home():
    return "Home"


@app.route("/search", methods=["POST"])
def handle_search():
    user_query = request.form["query"]
    print(user_query)
    return search.query_vector(user_query)


if __name__ == "__main__":
    app.run(debug=True)
