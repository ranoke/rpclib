import json
import socket
import threading

class Status:
    OK = 0
    NOT_FOUND = 1
    ERROR = 2

class RPCBase:
    DEFAULT_ADDR = "localhost"
    DEFAULT_PORT = 13749
    DEFAULT_MAX_REQEUST_SIZE = 1024

class RPCListener(RPCBase):

    def __init__(self) -> None:
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.DEFAULT_ADDR, self.DEFAULT_PORT))
        self.sock.listen()
        self.binded_method = {}
        pass

    def add_method(self, name : str, method):
        self.binded_method[name] = method

    def handle_poll(self, lock, client_socket):
        request = None
        try:
            msg = client_socket.recv(self.DEFAULT_MAX_REQEUST_SIZE)
        except:
            return
        request = json.loads(msg.decode("utf-8"))


        result = None
        status = Status.ERROR

        name = request["name"]
        args = request["args"]

        if name in self.binded_method:
            if lock:
                lock.acquire()
            result = self.binded_method[name](*args)
            if lock:
                lock.release()
            status = Status.OK
        else:
            status = Status.NOT_FOUND

        response = {
            "result": result,
            "status": status
        }

        msg = json.dumps(response)
        try:
            client_socket.send(msg.encode("utf-8"))
        except:
            return

    def poll(self, lock = None):
        client_socket, addr = self.sock.accept()
        t = threading.Thread(target=self.handle_poll, args=[lock, client_socket])
        t.start()


class RpcCaller(RPCBase):

    def call_method(self, name, args = []):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.DEFAULT_ADDR, self.DEFAULT_PORT))

        request = {
            "name": name,
            "args": args
        }

        msg = json.dumps(request)
        self.sock.send(msg.encode("utf-8"))

        msg = self.sock.recv(self.DEFAULT_MAX_REQEUST_SIZE)
        response = json.loads(msg.decode("utf-8"))
        self.sock.close()

        return response["result"], response["status"]
