import re

def filter_datum(fields, redaction, message, separator):
    """
    Obfuscate specific fields in a log message.
    """
    pattern = r'(' + '|'.join([f"{field}=[^;]*" for field in fields]) + ')'
    return re.sub(pattern, lambda match: match.group(0).split('=')[0] + '=' + redaction, message)
