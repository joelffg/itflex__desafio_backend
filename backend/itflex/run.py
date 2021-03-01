from gevent import monkey  # isort:skip

monkey.patch_all()  # isort:skip

import signal  # noqa: E402

from geventwebsocket.server import WebSocketServer  # noqa: E402

from itflex.api import app  # noqa: E402
from itflex.config import HTTP_HOST, HTTP_PORT, VERBOSE  # noqa: E402
#from itflex.deps import events  # noqa: E402
#from itflex.deps import tasks  # noqa: E402

#events.start()
#tasks.start()


def main():
    log = None
    if VERBOSE:
        log = "default"

    server = WebSocketServer((HTTP_HOST, HTTP_PORT), app, log=log)

    def term_handler(signum, frame):
        server.stop()

    signal.signal(signal.SIGINT, term_handler)
    signal.signal(signal.SIGTERM, term_handler)

    print("Listening at http://{}:{}/".format(HTTP_HOST, HTTP_PORT))
    server.serve_forever()


if __name__ == "__main__":
    main()

