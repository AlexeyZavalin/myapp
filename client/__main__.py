from socket import socket
import yaml
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument(
    '-c', '--config', type=str,
    required=False, help='Sets config file path'
)

args = parser.parse_args()

config = {
    'host': 'localhost',
    'port': 8000
}
if args.config:
    with open(args.config) as file:
        config_load = yaml.load(file, Loader=yaml.Loader)
        config = config_load
sock = socket()
sock.connect((config.get('host'), config.get('port'),))

print('Client was started')

data = input('Enter data: ')

sock.send(data.encode())

print(f'Client send data: {data}')
b_response = sock.recv(1024)
print(b_response.decode())
