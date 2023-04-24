import requests


def get_avg_rate(currency: str, date: str) -> float:
    """
    Gets the average exchange rate for a given currency and date.
    """

    url = f"http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{date}/"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}: {response.status_code}")

    data = response.json()
    rates = data.get("rates", [])

    if not rates:
        raise Exception(f"No exchange rates found for {currency} on {date}")

    avg_rate = sum([rate.get("mid", 0) for rate in rates]) / len(rates)
    return avg_rate


def get_max_and_min_average_rate(currency: str, n: int) -> tuple:
    """
    Retrieve the maximum and minimum average exchange rate of a given currency over the last n quotations.
    """
    if not isinstance(n, int) or n <= 0 or n > 255:
        return (
            None,
            None,
            {
                "error": "Invalid value for n: n must be a positive integer less than or equal to 255."
            },
        )

    url = f"http://api.nbp.pl/api/exchangerates/rates/a/{currency}/last/{n}/"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}: {response.status_code}")

    data = response.json()
    quotations = data["rates"]

    if not quotations:
        raise Exception(f"No exchange rates found for {currency} on {n} quotations")
    mid_values = [q["mid"] for q in quotations[:n]]
    min_mid = min(mid_values)
    max_mid = max(mid_values)

    return min_mid, max_mid


def get_max_buy_sell_diff(currency: str, n: int) -> float:
    """
    Given a currency code and the number of last quotations n (n <= 255),
    return the maximum difference between the buy and ask rate.
    """
    url = f"http://api.nbp.pl/api/exchangerates/rates/c/{currency}/last/{n}/"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch data from {url}: {response.status_code}"
        )

    data = response.json()
    quotations = data["rates"]

    if not quotations:
        raise Exception(f"No exchange rates found for {currency} on {n} quotations")

    max_difference = 0
    for quotation in quotations:
        difference = quotation["ask"] - quotation["bid"]
        if difference > max_difference:
            max_difference = difference

    return max_difference
