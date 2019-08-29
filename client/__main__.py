from socket import socket
import yaml
import json
import hashlib
from datetime import datetime
from argparse import ArgumentParser
import logging

parser = ArgumentParser()
parser.add_argument(
    '-c', '--config', type=str,
    required=False, help='Sets config file path'
)

args = parser.parse_args()

config = {
    'host': 'localhost',
    'port': 8000,
    'buffer_size': 1024
}
if args.config:
    with open(args.config) as file:
        config_load = yaml.load(file, Loader=yaml.Loader)
        config.update(config_load)

host = config.get("host")
port = config.get("port")

sock = socket()
sock.connect((host, port,))

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logging.info('Client was started')

hash_obj = hashlib.sha256()
hash_obj.update(
    str(datetime.now().timestamp()).encode()
)

action = input('Enter action: ')
data = input('Enter data: ')

request = {
    'action': action,
    'time': datetime.now().timestamp(),
    'data': data,
    'token': hash_obj.hexdigest()
}

s_request = json.dumps(request)

sock.send(s_request.encode())

logging.info(f'Client send data: {data}')
b_response = sock.recv(config.get('buffer_size'))
logging.info(b_response.decode())
