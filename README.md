# Binance-TradingBot

LLM-powered crypto trading bot that trades based on Donald Trump's Truth Social posts.

## What it does
- Scrapes Trump's Truth Social posts using Selenium
- Analyzes the latest post for crypto-related content/sentiment using Groq's LLM API
- Generates trading signals (LONG/SHORT) based on the LLMs analysis
- Executes trades on Binance based on the trading signals
- Runs on a 60-second polling schedule to check for new posts

## Quick start

```bash
# Clone & configure
git clone https://github.com/juliuspor/Binance-TradingBot.git
cd Binance-TradingBot
cp .env.example .env  # Add your API keys here

# Launch with Docker 
docker-compose up -d
```

## Environment Variables
Create a `.env` file with the following variables:

```
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET_KEY=your_binance_secret_key
TRUTHSOCIAL_USERNAME=your_truthsocial_username
TRUTHSOCIAL_PASSWORD=your_truthsocial_password
GROQ_API_KEY=your_groq_api_key
```

## Docker Setup
The application runs in a Docker container with:
- Python 3.12
- Chromium browser for headless scraping
- Persistent data storage in the mounted `./data` directory
- Auto-restart 

## Notes
- Runs on Binance testnet by default
- Data persists in ./data directory between container restarts
- Currently places small (0.01 unit) trades when signals are detected
- Configurable via environment variables
- Posts are tracked to prevent duplicate processing