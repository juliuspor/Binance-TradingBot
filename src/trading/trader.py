import json
import os
import time


class Trader:
    def __init__(self, client, symbol="BTCUSDT"):
        self.client = client
        self.symbol = symbol
        self.metrics_path = "data/trade_metrics.json"
        os.makedirs(os.path.dirname(self.metrics_path), exist_ok=True)

    def get_price(self):
        """
        Returns the current price of the specified symbol (currency).
        """
        return float(self.client.get_symbol_ticker(symbol=self.symbol)["price"])

    def place_buy_order(self, quantity):
        """
        Places a market buy order for the instances symbol and quantity.
        """
        order = self.client.order_market_buy(symbol=self.symbol, quantity=quantity)
        print(
            "Buy order executed: ",
            order["symbol"],
            " at ",
            self.get_price(),
            " quantity: ",
            quantity,
        )
        # Log the trade metrics
        self.log_trade_metrics(order)

    def place_sell_order(self, quantity):
        """
        Places a market sell order for the instances symbol and quantity.
        """
        order = self.client.order_market_sell(symbol=self.symbol, quantity=quantity)
        print(
            "Sell order executed: ",
            order["symbol"],
            " at ",
            self.get_price(),
            " quantity: ",
            quantity,
        )
        self.log_trade_metrics(order)

    def log_trade_metrics(self, trade_data):
        """Log trade metrics for monitoring"""
        try:
            with open(self.metrics_path, "a") as f:
                f.write(
                    json.dumps(
                        {
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "trade_id": trade_data["orderId"],
                            "symbol": trade_data["symbol"],
                            "side": trade_data["side"],
                            "price": self.get_price(),
                            "quantity": float(trade_data["executedQty"]),
                            "status": trade_data["status"],
                        },
                        indent=4,
                    )
                    + "\n"
                )
        except Exception as e:
            print(f"Error logging trade metrics: {e}")
