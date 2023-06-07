import os, sys
sys.path.append(os.getcwd() + '/protopb/gen/py3')

import yaml
import consul

from internal.server.server import Server

WebConfigPath = "configs/conf.yml"
WebLog = "logs"


def init_config_from_consul():
    # 本地获取配置
    with open(WebConfigPath, 'r') as f:
        config = yaml.load(f, yaml.FullLoader)

    # 链接consul获取配置
    c = consul.Consul(host=config.get('consul').get('host'), port=config.get('consul').get('port'))
    config = yaml.safe_load(c.kv.get(config.get('config_path'))[1].get('Value').decode())
    return config


if __name__ == '__main__':
    # 初始化配置
    Server(config=init_config_from_consul()).run()


