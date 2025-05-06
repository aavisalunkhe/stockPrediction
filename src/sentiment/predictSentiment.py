import torch
from transformers import pipeline, AutoTokenizer

#inference pipeline
device = 0 if torch.cuda.is_available() else -1
tokenizer = AutoTokenizer.from_pretrained("../../models/finbertFinetuned")
sentiment_pipe = pipeline("text-classification", model="../../models/finbertFinetuned", tokenizer=tokenizer, device=device)

def predict(texts):
    results = sentiment_pipe(texts, batch_size=16)
    label_map = {"LABEL_0": -1, "LABEL_1": 1, "LABEL_2": 0}
    return [label_map[r["label"]] for r in results]
