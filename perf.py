#!/usr/bin/env python

from tornado.ioloop import IOLoop
import tornado.web
import tornado.httpserver
import aiohttp

url = "http://localhost:8080/ping"

 
class MainHandler(tornado.web.RequestHandler):
    async def fetch(session, url):
        async with session.get(url) as response:
            return await response.text()

    async def get(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
                self.write("out: {}".format(text))

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", MainHandler),
    ])
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8888, '127.0.0.1')
    server.start()
    IOLoop.current().start()