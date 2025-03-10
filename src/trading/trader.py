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

        Returns:
            dict: Order information returned by Binance API
        """
        order = self.client.order_market_buy(symbol=self.symbol, quantity=quantity)
        print("buy order done: ", order)
        # Log the trade metrics
        self.log_trade_metrics(order)
        return order

    def place_sell_order(self, quantity):
        """
        Places a market sell order for the instances symbol and quantity.

        Returns:
            dict: Order information returned by Binance API
        """
        order = self.client.order_market_sell(symbol=self.symbol, quantity=quantity)
        print("sell order done: ", order)
        # Log the trade metrics
        self.log_trade_metrics(order)
        return order

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
                            "price": float(
                                trade_data["price"] or trade_data["fills"][0]["price"]
                            ),
                            "quantity": float(trade_data["executedQty"]),
                            "status": trade_data["status"],
                        }
                    )
                    + "\n"
                )
        except Exception as e:
            print(f"Error logging trade metrics: {e}")
