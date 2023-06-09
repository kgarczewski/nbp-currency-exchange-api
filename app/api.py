from flask import Flask, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from app.currency_rate import (
    get_avg_rate,
    get_max_buy_sell_diff,
    get_max_and_min_average_rate,
)
from app.utils import (
    validate_date,
    validate_currency,
    validate_currency_quotes,
    get_currencies,
)
from typing import Union, Tuple

app = Flask(__name__)

"""
Set the global currencies variable to the list of valid currencies.
This function is called only once at the start of the app to reduce the costs of API requests, as currencies are 
not frequently updated.
Updating currencies only once at the start is enough to ensure that they are up-to-date for the duration of the app.
"""
currencies = get_currencies()

CORS(app)


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


SWAGGER_URL = ""
API_URL = "/static/swagger.json"
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "currency-exchange-api",
        "title": "Currency Exchange API Documentation",
    },
)

app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify(
            {
                "error": "Incorrectly formulated enquiries. Please check your spelling and try again."
            }
        ),
        404,
    )

@app.errorhandler(500)
def internal_server_error(error):
    return (
        jsonify(
            {
                "error": "No data for this request. Try again with different data."
            }
        ),
        500,
    )

@app.route("/exchanges/<string:currency>/<string:date>", methods=["GET"])
def get_avg_exchange_rate(currency: str, date: str) -> Union[jsonify, tuple]:
    """
    Get the average exchange rate for a given currency and date.

    Parameters:
    - currency (str): The currency code to look up.
    - date (str): The date to look up, in the format "YYYY-MM-DD".

    Returns:
    - If the exchange rate is found, returns a JSON object with the following keys:
      - "currency": The currency code that was looked up.
      - "date": The date that was looked up.
      - "average_exchange_rate": The average exchange rate for the given currency and date.
    - If an error occurs, a Flask JSON response with an 'error' key will be returned instead.
    """
    currency_error = validate_currency(currency, currencies)
    if currency_error:
        return jsonify({"error": currency_error}), 400

    date_error = validate_date(date)
    if date_error:
        return jsonify({"error": date_error}), 400

    rate = get_avg_rate(currency, date)
    if rate is None:
        return (
            jsonify(
                {"error": f"Exchange rate not found for {currency.upper()} on {date}."}
            ),
            404,
        )

    return jsonify(
        {"currency": currency.upper(), "date": date, "average_exchange_rate": rate}
    )


@app.route("/averages/<string:currency>/<int:quotations>", methods=["GET"])
def max_and_min_average(
    currency: str, quotations: int
) -> Union[jsonify, Tuple[str, int]]:
    """
    Returns the maximum and minimum daily average exchange rates for a given currency over a period of N quotations.

    Parameters:
        currency (str): A string representing the currency code to retrieve the rates for.
        quotations (int): An integer representing the number of quotations to retrieve rates for.

    Returns:
        Union[jsonify, Tuple[str, int]]: A Flask JSON response containing the following keys:
        - 'currency' (str): The currency code in uppercase.
        - 'quotations' (int): The number of quotations used to calculate the averages.
        - 'min_average' (float): The lowest daily average exchange rate.
        - 'max_average' (float): The highest daily average exchange rate.
        If an error occurs, a Flask JSON response with an 'error' key will be returned instead.
    """
    quotations_error = validate_currency_quotes(quotations)
    if quotations_error:
        return jsonify({"error": quotations_error}), 400
    currency_error = validate_currency(currency, currencies)
    if currency_error:
        return jsonify({"error": currency_error}), 400
    try:
        averages = get_max_and_min_average_rate(currency, quotations)
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve data: {str(e)}"}), 500

    if averages is None:
        return (
            jsonify(
                {
                    "error": "Exchange rate not found for the given currency and quotations."
                }
            ),
            404,
        )

    return jsonify(
        {
            "currency": currency.upper(),
            "quotations": quotations,
            "min_average": min(averages),
            "max_average": max(averages),
        }
    )


@app.route("/buy-ask-rate/<string:currency>/<int:quotations>", methods=["GET"])
def major_difference_buy_ask(
    currency: str, quotations: int
) -> Union[jsonify, Tuple[str, int]]:
    """
    Endpoint that returns the difference between the highest buy rate and the lowest sell rate for a given currency and
    number of quotations.

    Parameters:
        currency (str): A string representing the currency code.
        quotations (int): An integer representing the number of quotations to retrieve.

    Returns:
        Union[jsonify, Tuple[str, int]]: A Flask JSON response containing the following keys:
        - 'currency' (str): The currency code in uppercase.
        - 'quotations' (int): The number of quotations used to calculate the averages.
        - 'major_difference' (float): The major difference between the highest buy rate and the lowest sell rate.
        - If an error occurs, a Flask JSON response with an 'error' key will be returned instead.
    """

    currency_error = validate_currency(currency, currencies)
    if currency_error:
        return jsonify({"error": currency_error}), 400
    quotations_error = validate_currency_quotes(quotations)
    if quotations_error:
        return jsonify({"error": quotations_error}), 400
    major_difference = get_max_buy_sell_diff(currency, quotations)
    if major_difference is None:
        return (
            jsonify(
                {
                    "error": "Exchange rate not found for the given currency and quotations."
                }
            ),
            404,
        )

    return jsonify(
        {
            "currency": currency.upper(),
            "quotations": quotations,
            "major difference": major_difference,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
