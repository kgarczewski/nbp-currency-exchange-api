from datetime import datetime


def validate_currency(currency):
    currencies = ['THB', 'USD', 'AUD', 'HKD', 'CAD', 'NZD', 'SGD', 'EUR', 'HUF', 'CHF', 'GBP', 'UAH', 'JPY', 'CZK',
                   'DKK', 'ISK', 'NOK', 'SEK', 'RON', 'BGN', 'TRY', 'ILS', 'CLP', 'PHP', 'MXN', 'ZAR', 'BRL', 'MYR',
                   'IDR', 'INR', 'KRW', 'CNY', 'XDR']
    if currency.upper() not in currencies:
        return f'Invalid currency {currency}, must be one of {currencies}.'
    return None


def validate_date(date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return 'Invalid date format, should be YYYY-MM-DD.'
    if date.weekday() >= 5:
        return 'Invalid date, should be a weekday.'
    if date > datetime.today():
        return 'Invalid date, should be a past date.'


def validate_quotations(quotations):
    if not isinstance(quotations, int):
        return 'Invalid number of quotations, should be an integer.'
    elif quotations < 1 or quotations > 255:
        return 'Invalid number of quotations, should be between 1 and 255 inclusive.'
    else:
        return None
