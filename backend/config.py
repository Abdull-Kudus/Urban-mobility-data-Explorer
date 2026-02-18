

import sys
import os


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from db_config import DB_CONFIG


class Config:
    DB_HOST     = DB_CONFIG["host"]
    DB_PORT     = DB_CONFIG.get("port", 26257)  # Default CockroachDB port
    DB_NAME     = DB_CONFIG["database"]
    DB_USER     = DB_CONFIG["user"]
    DB_PASSWORD = DB_CONFIG["password"]

    DEBUG   = False
    TESTING = False

    DEFAULT_PAGE_SIZE = 50
    MAX_PAGE_SIZE     = 500


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_map = {
    "development": DevelopmentConfig,
    "production":  ProductionConfig,
}