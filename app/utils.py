from datetime import datetime
from typing import Union, List

import requests
import holidays


def get_currencies() -> List[str]:
    """
    Retrieves a list of valid currency codes from the NBP API and returns it as a List[str].
    Returns:
    List[str]: A list of valid currency codes retrieved from the NBP API.
    """
    currencies_endpoint = "http://api.nbp.pl/api/exchangerates/tables/a"
    currencies_data = requests.get(currencies_endpoint).json()[0]["rates"]
    currencies = [q["code"] for q in currencies_data]
    return currencies


def validate_currency(currency: str, currencies: List[str]) -> Union[str, None]:
    """
    Validates the given currency code.
    """
    if currency.upper() not in currencies:
        return f"Invalid currency {currency}, must be one of {currencies}."
    return None


def validate_date(date_str: str) -> Union[str, None]:
    """
    Validates that the input string is a valid date in the format 'YYYY-MM-DD',
    and that it is a weekday in the past, and not a Polish holiday.
    """
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format, should be YYYY-MM-DD."
    if date.weekday() >= 5:
        return "Invalid date, should be a weekday."
    if date > datetime.today():
        return "Invalid date, should be a past date."
    year = date.year
    if year < 2002:
        return "Data is only available since 2002."
    pl_holidays = holidays.Poland(years=[year])
    if date in pl_holidays:
        return "Invalid date, should not be a Polish holiday."
    return None


def validate_currency_quotes(currency_quotes) -> Union[str, None]:
    """
    Validates the number of currency quotations.
    """
    if not isinstance(currency_quotes, int):
        return "Invalid number of quotations, should be an integer."
    elif currency_quotes < 1 or currency_quotes > 255:
        return "Invalid number of quotations, should be between 1 and 255 inclusive."
    return None
