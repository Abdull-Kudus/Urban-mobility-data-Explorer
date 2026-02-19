import psycopg
from psycopg.rows import dict_row
from flask import current_app


def get_connection():
    return psycopg.connect(
        host        = current_app.config["DB_HOST"],
        port        = current_app.config["DB_PORT"],
        dbname      = current_app.config["DB_NAME"],
        user        = current_app.config["DB_USER"],
        password    = current_app.config["DB_PASSWORD"],
        sslmode     = "disable",
        row_factory = dict_row,
    )