# Nova CRUD

A simple CRUD API written in Flask and Flask-RestX.
It takes in raw data and calculates statistical averages for the data up until that data point. Databases are intially populated with data from `.csv` files in the `/data` folder.

## Development Process
Test-driven development was utilized for the development of this API. The tests were functional, but were tied together to form partial-E2E testing. All the tests were written using [Pytest](https://docs.pytest.org/en/7.2.x/).

## Setup
Solely a `.env` file is needed in the root directory of the project. Its format is the following:
```
MONGO_URI = "<mongodb-link>"
CSV_FILE = "data/Data_1000_id_<csv_id>.csv"
```
Replace all variables in angle brackets with your own values.

## TODOs:
- [ ] Add a UDP/TCP connection to stream data directly to the API

