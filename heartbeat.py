import os
import sys
import json
import argparse
import requests
import pygsheets
from datetime import datetime

__status__ = 'http://{ip}:{port}/api/v1/status'
__sheet__ = 'https://docs.google.com/spreadsheets/d/{id}/edit?usp=sharing'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('farm', help='')
    parser.add_argument('cell', help='')
    parser.add_argument('--ip', default='127.0.0.1', help='')
    parser.add_argument('--port', default=22333, help='')
    parser.add_argument('--key', default='key.json', help='')
    parser.add_argument('--sheet', default='1O34xZfhJdFeZd-s4M4bIOhdNhbyFw7M7y4nzoHyknwQ', help='')

    args = parser.parse_args()

    status = requests.get(__status__.format(
        ip=args.ip,
        port=args.port
    )).json()

    certificate = pygsheets.authorize(service_file=args.key)
    sht = certificate.open_by_url(__sheet__.format(id=args.sheet))
    wks = sht.worksheet_by_title(args.farm)
    wks.update_values(args.cell, [[
        datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        status['miner']['total_hashrate'][:-2]
    ]])

if __name__ == '__main__':
    main()