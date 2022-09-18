import json
import socket

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

    def poll(self):
        client_socket, addr = self.sock.accept()
        msg = client_socket.recv(self.DEFAULT_MAX_REQEUST_SIZE)
        request = json.loads(msg.decode("utf-8"))

        result = None
        status = Status.ERROR
        try:
            name = request["name"]
            args = request["args"]

            if name in self.binded_method:
                result = self.binded_method[name](*args)
                status = Status.OK
            else:
                status = Status.NOT_FOUND
        except Exception:
            print(f"Error: {Exception}")

        response = {
            "result": result,
            "status": status
        }

        msg = json.dumps(response)
        client_socket.send(msg.encode("utf-8"))
        client_socket.close()

class RpcCaller(RPCBase):

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def call_method(self, name, args):
        self.sock.connect((self.DEFAULT_ADDR, self.DEFAULT_PORT))

        request = {
            "name": name,
            "args": args
        }

        msg = json.dumps(request)
        self.sock.send(msg.encode("utf-8"))

        msg = self.sock.recv(self.DEFAULT_MAX_REQEUST_SIZE)
        response = json.loads(msg.decode("utf-8"))
        return response["result"], response["status"]