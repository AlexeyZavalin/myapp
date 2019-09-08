import select
import logging
import threading
from socket import socket


class Application:
    def __init__(self, host, port, buffer_size, handler):
        self._host = host
        self._port = port
        self._buffer_size = buffer_size
        self._handler = handler
        self._sock = socket()
        self._requests = list()
        self._connections = list()

    def bind(self, backlog=5):
        self._sock.bind((self._host, self._port,))
        self._sock.settimeout(0)
        self._sock.listen(backlog)

    def accept(self):
        try:
            client, address = self._sock.accept()
        except Exception:
            pass
        else:
            self._connections.append(client)
            logging.info(
                f'Client was connected with {address[0]}:{address[1]} | Connections: {self._connections}')

    def read(self, sock):
        try:
            bytes_request = sock.recv(self._buffer_size)
        except Exception:
            self._connections.remove(sock)
        else:
            if bytes_request:
                self._requests.append(bytes_request)

    def write(self, sock, response):
        try:
            sock.send(response)
        except Exception:
            self._connections.remove(sock)

    def run(self):
        try:
            logging.info(f'Server was started with {self._host}:{self._port}')

            while True:
                self.accept()
                rlist, wlist, xlist = select.select(
                    self._connections, self._connections, self._connections, 0
                )

                for r_client in rlist:
                    r_thread = threading.Thread(
                        target=self.read, args=(r_client,)
                    )
                    r_thread.start()

                if self._requests:
                    b_request = self._requests.pop()
                    b_response = self._handler(b_request)

                    for w_client in wlist:
                        w_thread = threading.Thread(
                            target=self.write, args=(
                                w_client, b_response)
                        )
                        w_thread.start()
        except KeyboardInterrupt:
            logging.info('Server shutdown')
