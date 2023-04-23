from flask import Flask, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from app.nbp import (
    get_avg_rate,
    get_major_difference_between_the_buy_and_ask_rate,
    get_max_and_min_average_value,
)
from app.utils import (
    validate_date,
    validate_currency,
    validate_quotations
)

app = Flask(__name__)
CORS(app)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


SWAGGER_URL = ''  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "currency-exchange-api",
        'title': "Currency Exchange API Documentation"
    }
)

app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)


@app.route('/exchanges/<string:currency>/<string:date>', methods=['GET'])
def get_avg_exchange_rate(currency, date):
    currency_error = validate_currency(currency)
    if currency_error:
        return jsonify({'error': currency_error}), 400

    date_error = validate_date(date)
    if date_error:
        return jsonify({'error': date_error}), 400

    rate = get_avg_rate(currency, date)
    if rate is None:
        return jsonify({'error': f'Exchange rate not found for {currency.upper()} on {date}.'}), 404

    return jsonify({'currency': currency.upper(), 'date': date, 'average_exchange_rate': rate})


@app.route('/averages/<string:currency>/<int:quotations>', methods=['GET'])
def max_and_min_average(currency, quotations):
    error = validate_quotations(quotations)
    if error:
        return jsonify({'error': error}), 400
    try:
        averages = get_max_and_min_average_value(currency, quotations)
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve data: {str(e)}'}), 500

    if averages is None:
        return jsonify({'error': 'Exchange rate not found for the given currency and quotations.'}), 404

    return jsonify(
        {
            'currency': currency.upper(),
            'quotations': quotations,
            'min_average': min(averages),
            'max_average': max(averages),
            'message': 'Values of min_average and max_average represent daily averages over the requested '
                       'period of N quotations.'
        }
    )


@app.route('/buy-ask-rate/<string:currency>/<int:quotations>', methods=['GET'])
def major_difference_buy_ask(currency, quotations):
    currency_error = validate_currency(currency)
    if currency_error:
        return jsonify({'error': currency_error}), 400

    major_difference = get_major_difference_between_the_buy_and_ask_rate(currency, quotations)
    if major_difference is None:
        return jsonify({'error': 'Exchange rate not found for the given currency and quotations.'}), 404

    return jsonify({'currency': currency.upper(), 'quotations': quotations, 'major difference': major_difference})


if __name__ == '__main__':
    app.run(debug=True)
