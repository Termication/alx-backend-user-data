#!/usr/bin/env python3
"""
filtered_logger
"""

import re


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Obfuscate specific fields in a log message.
    """
    for field in fields:
        message = re.sub(
            field + "=.*?" + separator, field + "=" +
            redaction + separator, message
        )
    return message
