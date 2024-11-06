# PII Data Management and Security

This project demonstrates effective handling, obfuscation, and security practices for Personally Identifiable Information (PII) within a system. It includes steps for creating a log filter to protect sensitive fields, encrypting and validating passwords, and using environment variables for secure database authentication.
#### Table of Contents

    About PII
    Log Filtering for PII
    Password Encryption
    Database Authentication with Environment Variables
    Installation and Usage

## About PII

Personally Identifiable Information (PII) includes any data that can be used to uniquely identify an individual, such as:

    Names
    Social Security Numbers
    Email Addresses
    Phone Numbers
    Financial Details

Protecting PII is crucial to ensure user privacy and comply with data protection regulations.
#### Log Filtering for PII

Logging PII data in raw form can expose sensitive information if logs are compromised. This project includes a log filter that obfuscates PII fields in logs, such as:

    Masking names, email addresses, and account details
    Ensuring log outputs are anonymized and comply with privacy standards

#### Example Usage

```python

from log_filter import PiiLogFilter

# Initialize the log filter
filter = PiiLogFilter(["name", "email", "phone"])

# Example log with sensitive data
log_entry = "User: name=John Doe, email=johndoe@example.com, phone=123-456-7890"

# Filtered log output
filtered_log = filter.apply(log_entry)
print(filtered_log)  # Output: "User: name=****, email=****, phone=****"
```
### Password Encryption

Secure password storage is essential to protect user credentials. This project demonstrates how to:

-Encrypt passwords using hashing algorithms
-Validate passwords securely, without storing plaintext versions

##### Example Usage

```python

from security import encrypt_password, check_password

# Encrypt a new password
hashed_password = encrypt_password("your_password")

# Check the validity of an input password
is_valid = check_password("your_password", hashed_password)
print(is_valid)  # Output: True or False
```
### Database Authentication with Environment Variables

To enhance security, database authentication should use environment variables for storing credentials rather than hardcoding them into code files. This project includes best practices for:

-Loading sensitive credentials from environment variables
-Using secure database connections

#### Example Configuration

```shell

# In your .env file
DB_USER=username
DB_PASSWORD=secure_password
DB_HOST=database_host
```
```python

from db_connect import get_db_connection

# Authenticate to the database
connection = get_db_connection()
```
