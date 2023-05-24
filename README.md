## Currency Exchange API

This is a simple API built using Flask that exposes endpoints for querying average exchange rates and buy/sell rates for currencies from the Narodowy Bank Polski's public APIs.

### Requirements

To run this project, you'll need to have the following installed:

- Git
- Docker

### Installation

1. Clone the repository:

```
git clone https://github.com/kgarczewski/nbp-currency-exchange-api.git
```

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
docker exec -it currency-exchange-api pytest tests
```

### Usage

Once the container is running, you can make requests to the following endpoints:

- `GET /exchanges/<currency_code>/<date>`: Returns the average daily exchange rate for a currency for a given date.
- `GET /buy-ask-rate/<currency_code>/<quotations>`: Returns the buy and sell rates for a currency over a specified period of time.
- `GET /averages/<currency_code>/<quotations>`: Returns the max and min average exchange rate for currency over a specified period of time.

Replace `<currency_code>`, `<date>`, and `<quotations>` with the relevant values for your query.

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
