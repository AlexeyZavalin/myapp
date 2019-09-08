import yaml
import json
import select
import logging
import threading
from socket import socket
from argparse import ArgumentParser
from app import Application
from protocol import validate_request, make_response
from handlers import handle_default_request
from resolvers import resolve


parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str,
    required=False, help='Sets config file path'
)

args = parser.parse_args()

default_config = {
    'host': 'localhost',
    'port': 8000,
    'buffer_size': 1024
}

if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        default_config.update(file_config)


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)


app = Application(default_config.get('host'), default_config.get(
    'port'), default_config.get('buffer_size'), handle_default_request)

app.bind()
app.run()
