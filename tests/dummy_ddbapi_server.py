import contextlib
import multiprocessing
import os
import signal
import time
import urllib.parse

import uvicorn


def uvicorn_run_app_with_environ(app, *args, env=None, **kwargs):
    env = env or {}

    for k, v in env.items():
        os.environ[k] = v

    uvicorn.run(app, *args, **kwargs)


@contextlib.contextmanager
def run_dummy_server(url, mongo_uri=None, mongo_db=None):
    pr = urllib.parse.urlparse(url)

    app = "ddbapi.app.app:app"

    add_env = {
        k: v for k, v in [
            ("DISPIMDB_MONGO_URI", mongo_uri),
            ("DISPIMDB_DATABASE_NAME", mongo_db)
        ] if v is not None}

    def terminate_server(s):
        """os.kill termination hack to get server codecov"""
        os.kill(s.pid, signal.SIGINT)
        s.join()

    server = multiprocessing.Process(
        target=uvicorn_run_app_with_environ,
        args=(app,), kwargs={
            'host': pr.hostname, 'port': pr.port,
            'env': add_env
            })

    server.start()
    time.sleep(1)  # force sleep so the process has some time to start
    yield url
    terminate_server(server)
