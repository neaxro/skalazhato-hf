import os

class Config:
    def __init__(self):
        # App settings
        self.ROOTPATH = os.getenv("ROOTPATH")
        self.RECIPE_SERVICE_HOST = os.getenv("RECIPE_SERVICE_HOST", "skalazhato")
        self.RECIPE_SERVICE_NAMESPACE = os.getenv("RECIPE_SERVICE_NAMESPACE", "default")

        # POSTGRES database related config
        self.POSTGRES_USER = os.getenv("POSTGRES_USER")
        self.POSTGRES_PASS = os.getenv("POSTGRES_PASS")
        self.POSTGRES_HOST = os.getenv("POSTGRES_HOST")
        self.POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
        self.POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
        
        # REDIS cache related config
        self.REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
        self.REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

config = Config()
