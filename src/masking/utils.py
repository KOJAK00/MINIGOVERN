import re

def mask_email(value: str) -> str:
    username, domain = value.split("@", 1)
    if len(username) <= 1:
        return "*" + "@" + domain
    return username[0] + "*" * (len(username) - 1) + "@" + domain

def mask_phone(value: str) -> str:
    digits = re.sub(r"\D", "", value)
    if len(digits) < 7:
        return "*" * len(digits)
    return digits[:3] + "*" * (len(digits) - 6) + digits[-3:]

def mask_identifier(value: str) -> str:
    if len(value) <= 4:
        return "*" * len(value)
    return "*" * (len(value) - 4) + value[-4:]

def mask_person_name(value: str) -> str:
    if len(value) <= 2:
        return value[0] + "*"
    return value[0] + "*" * (len(value) - 2) + value[-1]

def mask_password(value: str) -> str:
    return "********"

def mask_value(value, semantic_type):
    if value is None:
        return None

    semantic_type = (semantic_type or "").upper()
    value = str(value)
    if semantic_type == "EMAIL":
        return mask_email(value)

    if semantic_type == "PHONE":
        return mask_phone(value)

    if semantic_type == "IDENTIFIER":
        return mask_identifier(value)

    if semantic_type == "PERSON_NAME":
        return mask_person_name(value)
    
    if semantic_type == "PASSWORD":
        return mask_password(value)
    
    return value