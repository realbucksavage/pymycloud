import zlib

import constants
from database.models import Users


class FileTransmitter:
    """
    Writes a requested file over the TCP Socket. The file is divided into
    blocks 64 Bytes.
    """

    def __init__(self, user: Users, request):
        self._user = user
        self._request = request

        self._block_size = 64
        self._compressor = zlib.compressobj(1)

    def run(self):
        base_dir = f"{constants.work_dir}/{self._user.username}/_user"

        # Requested file
        request_file = self._request.recv(1024).decode()
        if not request_file[0] == "/":
            request_file = f"/{request_file}"

        with open(f"{base_dir}{request_file}", "rb") as input:
            while True:
                block = input.read(self._block_size)
                if not block:
                    break

                compressed = self._compressor.compress(block)
                if compressed:
                    self._request.send(compressed)

            remaining_buffer = self._compressor.flush()
            while remaining_buffer:
                to_send = remaining_buffer[:self._block_size]
                remaining_buffer = remaining_buffer[self._block_size:]
                self._request.send(to_send)
