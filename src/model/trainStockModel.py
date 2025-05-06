import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

df= pd.read_csv("../../data/processed/features.csv", index_col= "Date", parse_dates= True)
X= df[[c for c in df.columns if c.startswith("sent_lag_")]]
y= df["dir"]
#time-based split
split= int(0.8 * len(df))
X_train, X_test= X.iloc[:split], X.iloc[split:]
y_train, y_test= y.iloc[:split], y.iloc[split:]

clf= RandomForestClassifier(n_estimators= 100, random_state= 42)
clf.fit(X_train, y_train)
pred= clf.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))
print("F1:", f1_score(y_test, pred))
