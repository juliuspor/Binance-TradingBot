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
        self.trading_pair = None
        self.trade_signal = None
        self.reason = None

    def analyze_signal(self):
        """
        Uses Groq's Llama API to extract a crypto trading pair and determine if the post suggests:

        The result dictionary is stored in the `result` member variable.
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
            '  "trading_pair": "BTCUSDT/ETHUSDT/TRUMPUSDT/IRRELEVANT",'
            '  "trade_signal": "LONG/SHORT/NO TRADE",'
            '  "reason": "<10 word reason explaining the reasoning for the trade signal."'
            "}"
        )

        try:
            chat_completion = client.chat.completions.create(
                model="gemma2-9b-it",
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
                json_response = json.loads(response)
                self.trading_pair = json_response.get("trading_pair", "IRRELEVANT")
                self.trade_signal = json_response.get("trade_signal", "NO TRADE")
                self.reason = json_response.get("reason", "No reason provided.")

            except json.JSONDecodeError as e:
                print("Could not extract structured data from LLM response: ", e)

        except Exception as e:
            print("Error analyzing trading signal: ", e)
