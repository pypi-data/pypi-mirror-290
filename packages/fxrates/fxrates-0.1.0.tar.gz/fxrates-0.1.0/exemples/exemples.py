from fxrates import ExchangeRate

# Retrieve most recent exchange rate for JPY/USD
params = {
    "targets_codes": "USD",
    "base_code": "JPY",
    "date_from": None,
    "date_to": None,
    "amount": 1,
}
data = ExchangeRate.convert(**params)


# Get exchange rates of EUR/USD and EUR/CAD for all business days from a date to most recent data
params = {
    "targets_codes": ["USD", "CAD"],
    "base_code": "EUR",
    "date_from": "2023-01-01",
    "date_to": None,
    "amount": 1,
}
data = ExchangeRate.convert(**params)


# Get amount of USD and CAD corresponding to 100.5 EUR for a specific date
params = {
    "targets_codes": ["USD", "CAD"],
    "base_code": "EUR",
    "date_from": None,
    "date_to": "2024-01-01",
    "amount": 100.5,
}
data = ExchangeRate.convert(**params)


# Get amount of USD and CAD corresponding to 100 EUR for all business days between 2 dates
params = {
    "targets_codes": ["USD", "CAD"],
    "base_code": "EUR",
    "date_from": "2022-01-01",
    "date_to": "2024-05-30",
    "amount": 100,
}
data = ExchangeRate.convert(**params)
