import requests


def get_avg_rate(currency: str, date: str) -> float:
    url = f"http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{date}/"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}: {response.status_code} {response.text}")

    data = response.json()
    rates = data.get("rates", [])

    if not rates:
        raise Exception(f"No exchange rates found for {currency} on {date}")

    avg_rate = sum([rate.get("mid", 0) for rate in rates]) / len(rates)
    return avg_rate


def get_max_and_min_average_value(currency: str, n: int) -> tuple:
    if not isinstance(n, int) or n <= 0 or n > 255:
        return None, None, {'error': 'Invalid value for N: N must be a positive integer less than or equal to 255.'}

    url = f"http://api.nbp.pl/api/exchangerates/rates/a/{currency}/last/{n}/"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}: {response.status_code} {response.text}")

    data = response.json()
    quotations = data['rates']

    if not quotations:
        raise Exception(f"No exchange rates found for {currency} on {n} quotations")
    mid_values = [q['mid'] for q in quotations[:n]]
    min_mid = min(mid_values)
    max_mid = max(mid_values)

    return min_mid, max_mid


def get_major_difference_between_the_buy_and_ask_rate(currency: str, n: int) -> tuple:
    url = f"http://api.nbp.pl/api/exchangerates/rates/c/{currency}/last/{n}/"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}: {response.status_code} {response.text}")

    data = response.json()
    quotations = data['rates']

    if not quotations:
        raise Exception(f"No exchange rates found for {currency} on {n} quotations")

    max_difference = 0
    for quotation in quotations:
        difference = quotation["ask"] - quotation["bid"]
        if difference > max_difference:
            max_difference = difference

    return max_difference
