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
                self.write("AIO out: {}".format(text))


class AsyncHTTPHandler(tornado.web.RequestHandler):
    async def get(self):
        http_client = AsyncHTTPClient()
        response = await http_client.fetch(url)
        out = base64.b64decode(response.body)
        self.write("AsyncHTTP out: {}".format(out))


class HttpXHandler(tornado.web.RequestHandler):
    async def get(self):
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
            self.write("Httpx out: {}".format(r.text))


if __name__ == "__main__":
    AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

    app = tornado.web.Application([
        ("/ping1", AIOHandler),
        ("/ping2", AsyncHTTPHandler),
        ("/ping3", HttpXHandler),
        ('/_profile', ProfileHandler),
    ])

    server = tornado.httpserver.HTTPServer(app)
    server.bind(app_settings["port"], '127.0.0.1')
    server.start()

    # uvloop.install()
    IOLoop.current().start()