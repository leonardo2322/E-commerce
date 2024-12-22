from decimal import Decimal
from datetime import datetime


def decimal_to_float(data):
    for key, value in data.items():
        if isinstance(value, Decimal):
            data[key] = float(value)  # Convertir Decimal a float
        elif isinstance(value, datetime):
            data[key] = value.isoformat()  # Convertir datetime a string (ISO 8601)
    return data