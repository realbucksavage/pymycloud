from flask import Flask

app = Flask(__name__, static_folder="frontend", static_url_path="/frontend")


@app.route("/")
def root_controller():
    return app.send_static_file("src/index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
