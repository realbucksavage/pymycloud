import logging
import socketserver
import threading

from flask import Flask
from flask_restful import Api

from constants import constants
from apis.client.api import ClientFileManagementApi, ClientLoginApi
from apis.client.transmissions import ClientTransmissionApi
from core.sockets import SocketRequestHandler

app = Flask(__name__, static_folder="frontend", static_url_path="/frontend")
api = Api(app)

# Api routes

# For desktop clients
api.add_resource(ClientLoginApi, "/api/client/login")
api.add_resource(ClientFileManagementApi, '/api/client/manage')
api.add_resource(ClientTransmissionApi, '/api/client/transmit')


@app.route("/")
def root_controller():
    return app.send_static_file("src/index.html")


if __name__ == "__main__":
    logging.basicConfig(file=f"{constants.work_dir()}/pymycloud.log", level=logging.INFO)

    address = ("0.0.0.0", 9795)
    server = socketserver.TCPServer(address, SocketRequestHandler)

    socket_thread = threading.Thread(target=server.serve_forever)
    socket_thread.setDaemon(True)
    socket_thread.start()

    app.run(host="0.0.0.0", port=8000)
