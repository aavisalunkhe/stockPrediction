from datasets import load_dataset
from transformers import AutoTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

#11,932 finance-related tweets labeled as bearish, bullish, or neutral (9,938 train, 2,486 validation), zeroshot dataset from huggingface
#load the tweet sentiment dataset (finance-related tweets, labels 0=Bearish,1=Bullish,2=Neutral)
dataset= load_dataset("zeroshot/twitter-financial-news-sentiment")
print(dataset)


# # Load model directly
# from transformers import AutoTokenizer, AutoModelForMaskedLM
# tokenizer = AutoTokenizer.from_pretrained("ahmedrachid/FinancialBERT")
# model = AutoModelForMaskedLM.from_pretrained("ahmedrachid/FinancialBERT")

#Tokenizing the text for bert (3-class task)
#since the original model is MaskedLM, i have used BertForSequenceClassification to add a classification head
tokenizer= AutoTokenizer.from_pretrained("ahmedrachid/FinancialBERT")
model= BertForSequenceClassification.from_pretrained(
    "ahmedrachid/FinancialBERT",
    num_labels= 3
)

#applying tokenizing function on the dataset
def tokenize_function(examples):
    return tokenizer(examples["text"], padding= "max_length", truncation= True, max_length= 128)

tokenized= dataset.map(tokenize_function, batched=True)
train_dataset= tokenized["train"]
val_dataset= tokenized["validation"]

#training arguments: 2 epochs, LR 2e-5, batch size 16
training_args= TrainingArguments(
    output_dir= "./finetuned_finbert",
    num_train_epochs= 3,
    per_device_train_batch_size= 16,
    per_device_eval_batch_size= 16,
    learning_rate= 2e-5,
    evaluation_strategy= "epoch",
    weight_decay= 0.01,
    logging_steps= 50,
    save_total_limit= 1
)
#finetune
trainer= Trainer(
    model= model,
    args= training_args,
    train_dataset= train_dataset,
    eval_dataset= val_dataset,
    tokenizer= tokenizer
)
trainer.train()
trainer.save_model("../../models/finbertFinetuned.py")
#model is capable of giving argmax= sentiment label; label 0=Bearish (negative), 1=Bullish (positive), 2=Neutral