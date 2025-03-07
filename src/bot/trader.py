def get_price(client, symbol):
    """
    Returns the current price of the specified symbol (currency).

    Args:
        client: Binance client instance
        symbol (str): Trading pair symbol (e.g., 'BTCUSDT')

    Returns:
        price as float
    """
    return float(client.get_symbol_ticker(symbol=symbol)["price"])


def place_buy_order(client, symbol, quantity):
    """
    Places a market buy order for the specified symbol and quantity.

    Args:
        client: Binance client instance
        symbol (str): Trading pair symbol (e.g., 'BTCUSDT')
        quantity (float): Amount to buy

    Returns:
        dict: Order information returned by Binance API
    """
    order = client.order_market_buy(symbol=symbol, quantity=quantity)
    print("buy order done: ", order)
