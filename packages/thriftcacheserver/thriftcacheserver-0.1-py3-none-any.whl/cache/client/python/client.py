from cache.gen.keyvalue import KeyValueService
from cache.gen.keyvalue.ttypes import (
    GetRequest,
    GetResponse,
    SetRequest,
    KeyNotFound
)
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


def main():
    # Make socket
    transport = TSocket.TSocket('localhost', 9090)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = KeyValueService.Client(protocol)

    # Connect!
    transport.open()

    print("Setting key = shivam, value = mitra")
    client.Set(SetRequest(key="shivam", val="mitra"))
    print("key = shivam, value = mitra is set")
    result: GetResponse = client.Get(GetRequest(key="shivam"))
    print("Getting key = shivam")
    print(result.val)

    try:
        print("Getting key = shiva")
        client.Get(GetRequest(key="shiva"))
    except KeyNotFound:
        print("key=shiva not found")

    # Close!
    transport.close()


if __name__ == '__main__':
    try:
        main()
    except Thrift.TException as tx:
        print(tx.message)
