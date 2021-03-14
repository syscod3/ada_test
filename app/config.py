from pydantic import BaseSettings


class Config(BaseSettings):
    EXPOSE_PORT = 8800
    DEBUG = True
    RELOAD = False
    WORKERS = 1
    TIMEOUT = 5
