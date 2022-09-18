
import rpc

c = rpc.RpcCaller()

print(c.call_method(rpc._METHOD_GET_IDS, []))