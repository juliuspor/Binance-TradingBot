# Binance Trading Bot

Automated cryptocurrency trading bot that:
- Scrapes Donald Trump's posts from Truth Social using `truthbrush` or `Selenium` 
- Analyzes trading signal with Groq's API (Different LLMs possible)
- Executes trades on Binance based on sentiment analysis
- Sends notification alerts about trades via email/Telegram

## Requirements
- Python 3.9+
- A `Binance` account with API access enabled
- API key for Groq 

## Installation and Usage
```sh
git clone https://github.com/juliuspor/Binance-TradingBot.git
cd Binance-TradingBot
pip install -r requirements.txt

# Configure API keys in .env file
cp .env.example .env
# Edit .env with your API keys

# Start the bot
python src/main.py
```