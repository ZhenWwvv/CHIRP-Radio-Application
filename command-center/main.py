from tornado.ioloop import IOLoop

from commandcenter import get_app


if __name__ == '__main__':
    app = get_app(debug=True)
    app.listen(8000)
    print('Serving on http://localhost:8000')
    loop = IOLoop.current()
    loop.start()
