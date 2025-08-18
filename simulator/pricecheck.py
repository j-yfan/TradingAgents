from polygon import RESTClient

client = RESTClient(api_key="6Glepk_hsdQxrNhR6jQuWy9gUAfjc4YU")

ticker = "AAPL"

# List Aggregates (Bars)
aggs = []
for a in client.list_aggs(ticker=ticker, multiplier=1, timespan="days", from_="2025-08-01", to="2025-08-12", limit=50000):
    aggs.append(a)

print(aggs)
