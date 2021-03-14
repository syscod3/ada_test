#!/usr/bin/env python3

import uvicorn
from app.config import Config
from app.main import app

conf = Config()
# Importing app here. start the app and bind port
if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=conf.EXPOSE_PORT,
        reload=conf.RELOAD,
        debug=conf.DEBUG,
        workers=conf.WORKERS,
        timeout_keep_alive=conf.TIMEOUT,
    )
