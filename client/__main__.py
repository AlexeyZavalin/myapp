from socket import socket
import yaml
import json
from datetime import datetime
from argparse import ArgumentParser

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

print('Client was started')

action = input('Enter action: ')
data = input('Enter data: ')

request = {
    'action': action,
    'time': datetime.now().timestamp(),
    'data': data
}

s_request = json.dumps(request)

sock.send(s_request.encode())

print(f'Client send data: {data}')
b_response = sock.recv(config.get('buffer_size'))
print(b_response.decode())
