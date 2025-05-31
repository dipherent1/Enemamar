import re

def normalize_phone_number(phone: str) -> str:
    # Strip +251, 251, or 0 at the start
    return re.sub(r'^(?:\+251|251|0)', '', phone)

def format_phone_for_sending(phone: str, use_plus_prefix=True) -> str:
    if use_plus_prefix:
        return f'+251{normalize_phone_number(phone)}'
    else:
        return f'0{normalize_phone_number(phone)}'