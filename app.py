from flask import Flask
from flask_restful import Api

from apis.client.api import ClientLoginApi, ClientFileManagementApi

app = Flask(__name__, static_folder="frontend", static_url_path="/frontend")
api = Api(app)

# Api routes

# For desktop clients
api.add_resource(ClientLoginApi, "/api/client/login")
api.add_resource(ClientFileManagementApi, '/api/client/manage')


@app.route("/")
def root_controller():
    return app.send_static_file("src/index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
