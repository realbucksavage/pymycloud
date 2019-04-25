class SocketError(ValueError):
    def __init__(self, err_code: str):
        self._error_code = err_code if err_code else "UNKNOWN"

        super(self._error_code)

    def get_error_code(self):
        return self._error_code


class InvalidTransmissionKeyError(SocketError):
    def __init__(self):
        super("INV_TRAN_KEY")


class InvalidTransmissionTypeError(SocketError):
    def __init__(self):
        super("INV_TRAN_TYP")
