import json
import os

from groq import Groq


class TradingSignalAnalyzer:
    """
    Analyzes a Truth Social post to extract a trading signal.

    Determines if a post mentions a cryptocurrency trading pair and whether
    it implies a LONG (buy), SHORT (sell), or NO TRADE (neutral).
    """

    def __init__(self, post):
        self.post = post
        self.result = None

    def analyze_signal(self):
        """
        Uses Groq's Llama API to extract a crypto trading pair and determine if the post suggests:
        - LONG (bullish sentiment, buy signal)
        - SHORT (bearish sentiment, sell signal)
        - NO TRADE (neutral sentiment or no trade recommendation)
        - IRRELEVANT (if no crypto pair is mentioned)

        The result is stored in the `result` member variable.
        """
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        # Constructing a structured prompt
        prompt = (
            "Analyze the following social media post and extract trading signals related to cryptocurrencies.\n"
            "Determine the trading pair mentioned (BTCUSDT, ETHUSDT, TRUMPUSDT). If no pair is mentioned, return 'IRRELEVANT'.\n"
            "Then, decide if the post implies a LONG (bullish, buy signal), SHORT (bearish, sell signal), or NO TRADE.\n\n"
            f"Post: \"{self.post['content']}\"\n"
            "Respond in the following JSON format:\n"
            "```json\n"
            "{"
            '  "trading_pair": "BTCUSDT/ETHUSD/IRRELEVANT",'
            '  "trade_signal": "LONG/SHORT/NO TRADE",'
            '  "reason": "<10 word reason explaining the reasoning for the trade signal."'
            "}"
        )

        try:
            chat_completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "user", "content": prompt},
                    {
                        "role": "assistant",
                        "content": "```json\n",
                    },  # assistant message, look groq documentation for more info
                ],
                stop="```",
            )

            response = chat_completion.choices[0].message.content.strip()

            # Parse response as JSON
            try:
                signal_data = json.loads(response)
            except json.JSONDecodeError as e:
                print("Could not extract structured data from LLM response: ", e)
                self.result = {
                    "trading_pair": "IRRELEVANT",
                    "trade_signal": "NO TRADE",
                    "reason": "Could not extract structured data.",
                }

            self.result = {
                "trading_pair": signal_data.get("trading_pair", "IRRELEVANT"),
                "trade_signal": signal_data.get("trade_signal", "NO TRADE"),
                "reason": signal_data.get("reason", "No reason provided."),
            }

        except Exception as e:
            print("Error analyzing trading signal: ", e)
            self.result = {
                "trading_pair": "IRRELEVANT",
                "trade_signal": "Error",
                "reason": str(e),
            }
