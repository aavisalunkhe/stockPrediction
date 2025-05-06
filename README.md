# Twitter Stock Sentiment Predictor

A pipeline to predict daily stock movement (up/down) for Tesla ($TSLA) by fine-tuning a FinancialBERT sentiment model on finance-specific tweets and combining weighted daily sentiment scores with historical price data in a Random Forest classifier.

---

## 🚀 Features

- **Fine-tune FinancialBERT** on the `zeroshot/twitter-financial-news-sentiment` dataset (bullish/bearish/neutral).  
- **Scrape live tweets** for `$TSLA` using Selenium.
- **Preprocess tweets** (URL→`[URL]`, hashtag cleanup, emoji removal).  
- **Classify tweets** into sentiment scores (–1, 0, +1).  
- **Fetch historical prices** via [yfinance](https://github.com/ranaroussi/yfinance).  
- **Compute weighted sentiment** per day (retweet‐weighted average).  
- **Build lookback features** (lagged sentiment over past N days).  
- **Train & evaluate** a Random Forest to predict next‐day stock direction.

---
## 🙏 Acknowledgments
- Based on the Stanford CS224N custom project “Tweet Sentiment Analysis to Predict Stock Market.”
- Uses FinancialBERT, Hugging Face Datasets, and yfinance.
- Inspiration and methodology from Christian Palomo’s CS224N project report.
