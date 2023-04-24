## Currency Exchange API

This is a simple REST API built using Flask that exposes endpoints for querying average exchange rates and buy/sell rates for currencies from the Narodowy Bank Polski's public APIs.

### Requirements

To run this project, you'll need to have the following installed:

- Git
- Docker (optional) 

### Installation

1. Clone the repository:

```
git clone https://github.com/kgarczewski/nbp-currency-exchange-api.git
```
[If You don't want to use the docker go here](#alternatively)

2. Build the Docker image:

```
cd nbp-currency-exchange-api
docker build -t currency-exchange-api .
```

3. Run the Docker container:

```
docker run -d -p 5000:5000 --name currency-exchange-api currency-exchange-api
```

4. Run the tests:

```
docker exec -it currency-exchange-api /bin/bash
source env/bin/activate
pytest tests
```
### Alternatively:

1. Clone the repository:

```
git clone https://github.com/kgarczewski/nbp-currency-exchange-api.git
```

2. Activate the virtual environment and install the dependencies:

```
cd nbp-currency-exchange-api
source env/bin/activate
Install the dependencies specified in requirements.txt using pip install -r requirements.txt
```

3. Set the FLASK_APP environment variable:

```
export FLASK_APP=app/api.py
```

4. Run the tests:

```
pytest tests
```

5. Run the application:

```
flask run
```

### Usage

Once the container is running, you can make requests to the following endpoints:

- `GET /exchanges/<currency_code>/<date>`: Returns the average daily exchange rate for a currency.
- `GET /buy-ask-rate/<currency_code>/<quotations>`: Returns the buy and sell rates for a currency.
- `GET /averages/<currency_code>/<quotations>`: Returns the buy and sell rates for a currency.

Replace `<currency_code>`, `<start_date>`, and `<end_date>` with the relevant values for your query.

Alternatively, you can use the Swagger UI to interact with the API. To do this, open your web browser and navigate to http://localhost:5000/. This will bring up the Swagger UI where you can view and test the API endpoints.

### Examples

- To get the average GBP exchange rate for given date:

```
curl http://localhost:5000/exchanges/GBP/2023-01-02
```

- To get the major difference between the buy and ask rate for given currency code and the number of last quotations N (N <= 255):

```
curl http://localhost:5000/buy-ask-rate/GBP/10
```

- To get the max and min average exchange rate for currency code and the number of last quotations N (N <= 255):

```
curl http://localhost:5000/averages/GBP/10
```