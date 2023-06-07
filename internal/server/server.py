import grpc
import consul
import pymongo
import time

from concurrent import futures

from internal.handler import handle
from internal.handler import config
from pkg.helper import internal


class Server:
    def __init__(self, config):
        self.config = config

    def run(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                             options=[('grpc.max_receive_message_length', 100 * 1024 * 1024)])
        mongo = pymongo.MongoClient("mongodb://" + self.config.get('mongo').get('hosts')[0])
        handle.init(config.config(server, mongo))

        ip = internal.get_internal_ip()
        port = internal.get_free_port()

        server.add_insecure_port(f'{ip}:{port}')

        c = consul.Consul(host=self.config.get('consul').get('host'), port=self.config.get('consul').get('port'))
        self.register(c, self.config.get('name'), ip, port)

        server.start()

        try:
            while True:
                time.sleep(186400)
        except:
            self.unregister(c, self.config.get('name'), ip, port)
            server.stop(0)

    def register(self, c, name, ip, port):
        check = consul.Check.tcp(ip, port, "10s")
        c.agent.service.register(name, f'{name}-{ip}-{port}', address=ip, port=port, check=check)
        print(f'{name} register success...')

    def unregister(self, c, name, ip, port):
        c.agent.service.deregister(f'{name}-{ip}-{port}')
        print(f'{name} exited...')



