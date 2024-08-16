import os


class BaseConfig:
    # Application settings
    APP_NAME = os.getenv("APP_NAME", "FastAPI app")
    APP_DESCRIPTION = os.getenv("APP_DESCRIPTION")
    APP_VERSION = os.getenv("APP_VERSION")
    APP_DEBUG = os.getenv("APP_DEBUG", True)
    ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")


class MongoConfig:
    # MongoDB settings
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB = os.getenv("MONGO_DB")
    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASS = os.getenv("MONGO_PASS")


class PostgresConfig:
    # PostgreSQL settings
    POSTGRES_URI = os.getenv("POSTGRES_URI")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASS = os.getenv("POSTGRES_PASS")


class Config(BaseConfig, MongoConfig, PostgresConfig):
    pass


config = Config()
