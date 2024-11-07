#!/usr/bin/env python3
"""A module for filtering sensitive data in logs."""

import os
import re
import logging
import mysql.connector
from typing import List


# Constants and patterns used for redacting sensitive information
patterns = {
    "extract": lambda x, y: r"(?P<field>{})=[^{}]*".format("|".join(x), y),
    "replace": lambda x: r"\g<field>={}".format(x),
}
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Obfuscates specified fields in a log message."""
    extract, replace = patterns["extract"], patterns["replace"]
    return re.sub(extract(fields, separator), replace(redaction), message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter for log messages
    containing sensitive information."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats and redacts sensitive fields in a log record."""
        msg = super().format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Creates and configures a logger for user data."""
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Establishes a connection to the database using environment variables."""
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    return mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )


def main():
    """Logs user records from the database."""
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(",")
    query = f"SELECT {fields} FROM users;"
    info_logger = get_logger()
    connection = get_db()

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(lambda x: f"{x[0]}={x[1]}", zip(columns, row))
            msg = "; ".join(list(record)) + ";"
            log_record = logging.LogRecord(
                "user_data", logging.INFO, None, None, msg, None, None
            )
            info_logger.handle(log_record)


if __name__ == "__main__":
    main()
