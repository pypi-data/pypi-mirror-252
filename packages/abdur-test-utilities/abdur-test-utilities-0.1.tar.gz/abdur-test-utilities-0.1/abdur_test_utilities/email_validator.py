import re


def is_valid_email(email):
    """Validate if a given string is a properly formatted email address."""
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(email_regex, email) is not None
