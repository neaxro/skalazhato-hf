import os

class Config:
    def __init__(self):
        # App settings
        self.ROOTPATH = os.getenv("ROOTPATH")

        # POSTGRES database related config
        self.POSTGRES_USER = os.getenv("POSTGRES_USER")
        self.POSTGRES_PASS = os.getenv("POSTGRES_PASS")
        self.POSTGRES_HOST = os.getenv("POSTGRES_HOST")
        self.POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
        self.POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))

config = Config()
