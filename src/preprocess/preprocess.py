import re, emoji
import pandas as pd

def preprocess(text):
    text= re.sub(r"http\S+", "[URL]", text)
    text= re.sub(r"#(\w+)", r"\1", text)
    text= re.sub(r"\s+", " ", text)
    text= emoji.get_emoji_regexp().sub("", text)
    text= re.sub(r"[^\w\s\[\]\(\)\.\,!?;:%]", "", text)
    return text.strip()

if __name__== "__main__":
    df= pd.read_json("../../data/raw/tweets.json")
    df["clean_text"]= df["text"].apply(preprocess)
    df.to_csv("../../data/processed/clean_tweets.csv", index=False)
