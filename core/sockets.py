import socketserver

from core.runners.downloader import FileTransmitter
from database.models import Transmissions
from database.session import SessionFactoryPool


class OwncloudSocketRequestHandler(socketserver.BaseRequestHandler):
    """
    Handles the traffic received over a TCP socket. The request must specify a
    transmission key (generated using the REST API)
    """

    def handle(self):
        """Hook that handles the traffic.

        TODO: Added erorr handling
        """
        # Receive the initial 8-character Transmission Key
        transmission_key = self.request.recv(16).decode()

        database_session = SessionFactoryPool.create_new_session()

        try:
            tran = database_session.query(Transmissions).filter(
                Transmissions.transmission_key == transmission_key).first()
            if not tran:
                raise ValueError()

            if tran.transmission_type == Transmissions.TYPE_GET:
                # Run the GET FILE runner
                FileTransmitter(tran.user, self.request).run()

            elif tran.transmission_type == Transmissions.TYPE_UPLOAD:
                pass
            else:
                raise ValueError()
        except Exception as err:
            print(err)
        finally:
            # Always end the transmission
            if tran:
                database_session.query(Transmissions).filter(
                    Transmissions.id == tran.id).delete()

            if database_session:
                database_session.close()
