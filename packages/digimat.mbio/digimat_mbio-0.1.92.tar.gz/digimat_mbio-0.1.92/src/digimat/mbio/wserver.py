import functools
import http.server
import threading
import time
import os


class WebServer(object):
    def __init__(self, fpath=None, port=8000):
        self._port=port
        self._interface=''
        self._fpath=fpath
        self._thread=None
        self._httpd=None

    def server(self):
        handler=functools.partial(http.server.SimpleHTTPRequestHandler, directory=self._fpath)
        with http.server.ThreadingHTTPServer((self._interface, self._port), handler) as httpd:
            try:
                self._httpd=httpd
                httpd.serve_forever()
            except:
                pass
            httpd.server_close()

        self._httpd=None

    def start(self):
        self._thread=threading.Thread(target=self.server)
        self._thread.daemon=True
        self._thread.start()
        while True:
            time.sleep(1)
            try:
                files=os.listdir(self._fpath)
                if not files:
                    break
            except:
                break

        self.stop()

    def stop(self):
        if self._thread:
            try:
                self._httpd.shutdown()
            except Exception as e:
                print(e)
                pass
            self._thread.join()
            self._thread=None


if __name__ == '__main__':
    ws=WebServer('/tmp/test')
    ws.start()
