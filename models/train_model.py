from datasets import load_dataset, Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import pandas as pd
import torch

# Step 1: Load your data
df = pd.read_csv("labeled_headlines.csv")  # columns: text, label
label_map = {"positive": 0, "neutral": 1, "negative": 2}
df["label"] = df["label"].map(label_map)
dataset = Dataset.from_pandas(df)

# Step 2: Load model and tokenizer
model_name = "yiyanghkust/finbert-tone"  # RoBERTa-based
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)

# Step 3: Tokenize the data
def preprocess(examples):
    return tokenizer(examples["text"], truncation=True, padding=True)

dataset = dataset.train_test_split(test_size=0.2)
tokenized = dataset.map(preprocess, batched=True)

# Step 4: Define training arguments
training_args = TrainingArguments(
    output_dir="./finbert-finetuned",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=4,
    weight_decay=0.01,
    save_total_limit=2,
    logging_dir="./logs",
)

# Step 5: Trainer setup
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["test"],
    tokenizer=tokenizer,
)

# Step 6: Train the model
trainer.train()

# Optional: Save the model
model.save_pretrained("finbert-finetuned")
tokenizer.save_pretrained("finbert-finetuned")