#!/usr/bin/env python

from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient

import tornado.web
import tornado.httpserver
import aiohttp
import httpx
import datetime
import time
import uvloop
import asyncio
import os
import base64
import logging
import argparse
import warnings
import sys

url = "http://localhost:8080/random"

app_settings = {
    "port": os.environ.get("PERF_PORT", "9000"),
}

from plop.collector import Collector, PlopFormatter

class ProfileHandler(tornado.web.RequestHandler):

    async def get(self):
        self.collector = Collector()
        self.collector.start()
        return await self.finish_profile()


    async def finish_profile(self):
        time.sleep(1)
        self.collector.stop()
        formatter = PlopFormatter()
        self.finish(formatter.format(self.collector))

class AIOHandler(tornado.web.RequestHandler):
    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def get(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
                out = base64.b64decode(text)
                self.write("AIO out: {}".format(out))

class AsyncHTTPHandler(tornado.web.RequestHandler):
    async def get(self):
        http_client = AsyncHTTPClient()
        response = await http_client.fetch(url)
        out = base64.b64decode(response.body)
        self.write("AsyncHTTP out: {}".format(out))


class AsyncHTTPHandlerLongBlock(tornado.web.RequestHandler):
    async def get(self):
        logging.warning('LONGBLOCK started')
        time.sleep(10)
        logging.info('LONGBLOCK completed')
        self.write("AsyncHTTP LONG out: DONE")

class HttpXHandler(tornado.web.RequestHandler):
    async def get(self):
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
            self.write("Httpx out: {}".format(r.text))




parser = argparse.ArgumentParser('Tornado Perf')
parser.add_argument(
    '-d',
    dest='debug',
    default=False,
    action='store_true',
)
parser.add_argument(
    '-v',
    dest='verbose',
    default=False,
    action='store_true',
)

parser.add_argument(
    '-uvloop',
    dest='uvloop',
    default=False,
    action='store_true',
)


if __name__ == "__main__":

    args = parser.parse_args()

    event_loop = asyncio.get_event_loop()
    
    if args.debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(levelname)7s: %(message)s',
            stream=sys.stderr,
        )

        logging.debug('enabling debugging')

        event_loop.set_debug(True)
        event_loop.slow_callback_duration = 0.005 #500ms

        warnings.simplefilter('always', ResourceWarning)
    else:
        logging.basicConfig(
            level=logging.WARN,
            format='%(levelname)7s: %(message)s',
            stream=sys.stderr,
        )

    AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")



    app = tornado.web.Application([
        ("/ping1", AIOHandler),
        ("/ping2", AsyncHTTPHandler),
        ("/ping3", HttpXHandler),
        ('/_profile', ProfileHandler),
        ("/block", AsyncHTTPHandlerLongBlock),
    ])

    server = tornado.httpserver.HTTPServer(app)
    server.bind(app_settings["port"], '127.0.0.1')
    server.start()

    if args.uvloop:
        uvloop.install()

    IOLoop.current().start()