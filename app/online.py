import threading

from prometheus_client import Gauge, start_http_server
import random
import time
import http.server

import requests
from bs4 import BeautifulSoup, Tag

pride_online_gauge = Gauge(name='pride_online', documentation='Pride x1.5 online')
prime_online_gauge = Gauge(name='prime_online', documentation='Prime x1 online')
asterios_online_gauge = Gauge(name='asterios_online', documentation='Asterios x5 online')
hunter_online_gauge = Gauge(name='hunter_online', documentation='Hunter x55 online')


class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()


def scrape():
    while True:
        resp = requests.get('https://asterios.tm/index.php')
        soup = BeautifulSoup(resp.text, features='html.parser')

        pride_online_gauge.set(get_online(soup.select('div.block1')[0]))
        prime_online_gauge.set(get_online(soup.select('div.block12')[0]))
        asterios_online_gauge.set(get_online(soup.select('div.block2')[0]))
        hunter_online_gauge.set(get_online(soup.select('div.block4')[0]))
        time.sleep(60 * 5 + random.randint(-30, -2))


def get_online(tag: Tag) -> int:
    try:
        online = tag.select('font')[0].text
        return int(online)
    except:
        print("Error during online parsing")
        return 0


if __name__ == '__main__':
    threading.Thread(target=scrape, name="Check server online", daemon=True).start()
    start_http_server(port=7755)
    server = http.server.HTTPServer(('localhost', 7756), MyHandler)
    server.serve_forever()
