#!/usr/bin/env python

from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient

import tornado.web
import tornado.httpserver
import aiohttp
import httpx

url = "http://localhost:8080/ping"

class AIOHandler(tornado.web.RequestHandler):
    async def fetch(session, url):
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
        self.write("AsyncHTTP out: {}".format(response.body))

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
    ])
    
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8888, '127.0.0.1')
    server.start()
    IOLoop.current().start()