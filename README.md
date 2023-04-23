Sure! Here's an example of what you could include in your README.md file to help users run your project with Docker:

## Currency Exchange API

This is a simple REST API built using Flask that exposes endpoints for querying average exchange rates and buy/sell rates for currencies from the Narodowy Bank Polski's public APIs.

### Requirements

To run this project, you'll need to have the following installed:

- Docker
- Git

### Installation

1. Clone the repository:

```
git clone git@github.com:kgarczewski/nbp-currency-exchange-api.git
```

2. Build the Docker image:

```
cd nbp-currency-exchange-api
docker build -t currency-exchange-api .
```

3. Run the Docker container:

```
docker run -p 5000:5000 currency-exchange-api
```

### Usage

Once the container is running, you can make requests to the following endpoints:

- `GET /average?currency=<currency_code>&start_date=<start_date>&end_date=<end_date>`: Returns the average exchange rate for a currency between two dates.
- `GET /buy-sell?currency=<currency_code>`: Returns the buy and sell rates for a currency.

Replace `<currency_code>`, `<start_date>`, and `<end_date>` with the relevant values for your query.

### Examples

- To get the average exchange rate for USD between January 1, 2022 and January 31, 2022:

```
http://localhost:5000/average?currency=USD&start_date=2022-01-01&end_date=2022-01-31
```

- To get the buy and sell rates for EUR:

```
http://localhost:5000/buy-sell?currency=EUR
```

That's it! You should now be able to use the Currency Exchange API with Docker. Let me know if you have any questions or need further assistance.