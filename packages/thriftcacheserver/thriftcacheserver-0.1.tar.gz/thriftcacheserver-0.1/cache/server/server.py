from cache.server.cachehandler import CacheHandler

from cache.gen.keyvalue import KeyValueService

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


def main():
    handler = CacheHandler()
    processor = KeyValueService.Processor(handler)
    transport = TSocket.TServerSocket(host='127.0.0.1', port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    print('Server started...')
    server.serve()
    print('Server shut down...')


if __name__ == "__main__":
    main()
