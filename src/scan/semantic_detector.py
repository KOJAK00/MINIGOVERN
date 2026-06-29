import re
from src.db.enum import SemanticType

NAME_RULES = {
    "email": SemanticType.EMAIL,
    "mail": SemanticType.EMAIL,

    "phone": SemanticType.PHONE,
    "mobile": SemanticType.PHONE,
    "telephone": SemanticType.PHONE,
    
    "country": SemanticType.COUNTRY,
    "nation": SemanticType.COUNTRY,
    
    "currency": SemanticType.CURRENCY,
    "currency_code": SemanticType.CURRENCY,
    
    "date": SemanticType.DATE,
    "created_at": SemanticType.DATE,
    "updated_at": SemanticType.DATE,
    "birth_date": SemanticType.DATE,
    
    "uuid": SemanticType.UUID,
    "id": SemanticType.IDENTIFIER,
    
    "name": SemanticType.PERSON_NAME,
    "first_name": SemanticType.PERSON_NAME,
    "last_name": SemanticType.PERSON_NAME,
}

EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)
PHONE_REGEX = re.compile(
    r"^\+?[0-9\s\-()]{7,20}$"
)

UUID_REGEX = re.compile(
    r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$",
    re.I
)

def detect_by_name(column_name: str):

    column_name = column_name.lower()

    for key, semantic in NAME_RULES.items():

        if key == column_name:
            return semantic.value

    return None
def detect_by_values(values: list):

    values = [
        str(v).strip()
        for v in values
        if v is not None
    ]

    if not values:
        return SemanticType.UNKNOWN.value

    if all(
        EMAIL_REGEX.match(v)
        for v in values
    ):
        return SemanticType.EMAIL.value

    if all(
        PHONE_REGEX.match(v)
        for v in values
    ):
        return SemanticType.PHONE.value

    if all(
        UUID_REGEX.match(v)
        for v in values
    ):
        return SemanticType.UUID.value

    lower_values = [
        v.lower()
        for v in values
    ]

    """ if all(
        v in COUNTRIES
        for v in lower_values
    ):
        return SemanticType.COUNTRY.value
        """

    return SemanticType.UNKNOWN.value

def detect_semantic_type(
    sample_values: list,
    column_name: str,
):

    by_name = detect_by_name(column_name)

    if by_name:
        return by_name

    return detect_by_values(sample_values)
