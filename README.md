# Binance-TradingBot

LLM-powered crypto trading bot that trades based on Donald Trumps posts.

## What it does
- Scrapes Trump's Truth Social posts in real-time
- translates his posts sentiment to trading signals using Groq's API
- Executes trades on Binance when signals are detected
- Tracks performance with trade metrics

## Quick start

```bash
# Clone & configure
git clone https://github.com/juliuspor/Binance-TradingBot.git
cd Binance-TradingBot
cp .env.example .env  # Add your API keys here

# Launch with Docker 
docker-compose up -d
```

## Stack
- Python 3.12
- Selenium for scraping
- Binance API for trading
- Groq API for sentiment analysis (You can choose the LLM)
- Docker for deployment

## Notes
- Runs on Binance testnet by default
- Data persists in ./data directory
- Configurable via environment variables