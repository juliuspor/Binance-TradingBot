class Trader:
    def __init__(self, client, symbol="BTCUSDT"):
        self.client = client
        self.symbol = symbol

    def get_price(self):
        """
        Returns the current price of the specified symbol (currency).

        Returns:
            price as float
        """
        return float(self.client.get_symbol_ticker(symbol=self.symbol)["price"])

    def place_buy_order(self, quantity):
        """
        Places a market buy order for the instances symbol and quantity.

        Args:
            quantity (float): Amount to buy

        Returns:
            dict: Order information returned by Binance API
        """
        order = self.client.order_market_buy(symbol=self.symbol, quantity=quantity)
        print("buy order done: ", order)
