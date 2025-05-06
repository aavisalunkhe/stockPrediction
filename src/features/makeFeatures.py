import pandas as pd
tweets= pd.read_csv("../../data/processed/clean_tweets.csv", parse_dates=["date"])
prices= pd.read_csv("../../data/raw/tsla_prices.csv", parse_dates=["Date"], index_col="Date")
#weighted sentiment per day
grp = tweets.groupby(tweets["date"].dt.date).apply(
    lambda g: (g["retweets"] * g["sentiment_score"]).sum() / max(g["retweets"].sum(),1)
).rename("weighted_sentiment")
#merge and lookbacks
df= prices[["Adj Close"]].rename(columns= {"Adj Close":"adj_close"})
df["dir"]= (df["adj_close"].shift(-1)> df["adj_close"]).astype(int)
df["ws"]= df.index.date.map(grp).fillna(0.0)
WINDOW = 7
for i in range(1, WINDOW+1):
    df[f"sent_lag_{i}"]= df["ws"].shift(i)
df.dropna().to_csv("../../data/processed/features.csv")
