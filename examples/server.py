import rpc

class TestC:

    def __init__(self) -> None:
        self.x = 0

    def inc_and_return(self):
        self.x += 1
        return self.x

test = TestC()

l = rpc.RPCListener()
l.add_method(rpc._METHOD_GET_IDS, test.inc_and_return)

while True:
    l.poll()
    pass