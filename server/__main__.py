from socket import socket
import yaml
import json
import logging
from argparse import ArgumentParser

from protocol import validate_request, make_response

from resolvers import resolve


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

sock = socket()
sock.bind((config.get('host'), config.get('port'),))
sock.listen(5)

host = config.get("host")
port = config.get("port")

print(f'Server was started with {host}:{port}')

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

handler = logging.FileHandler('main.log')
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)

try:
    while True:
        client, address = sock.accept()
        logger.info(f'Client was connected with {address[0]}:{address[1]}')
        b_request = client.recv(config.get('buffer_size'))
        request = json.loads(b_request.decode())

        if validate_request(request):
            action_name = request.get('action')
            controller = resolve(action_name)
            if controller:
                try:
                    logger.debug(
                        f'Controller {action_name} resolverd witch request: {request}')
                    response = controller(request)
                except Exception as err:
                    logger.critical(f'Controller {action_name} error: {err}')
                    response = make_response(
                        request, 500, 'Internal server error')
            else:
                logger.error(f'Controller {action_name} not found')
                response = make_response(
                    request, 404, f'action with name {action_name} not supported')
        else:
            logger.error(f'Controller wrong request: {request}')
            response = make_response(request, 400, 'wrong request format')

        client.send(
            json.dumps(response).encode()
        )
        client.close()

except KeyboardInterrupt:
    logger.info('Server shutdown')
