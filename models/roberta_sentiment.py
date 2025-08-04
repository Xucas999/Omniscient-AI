from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import pandas as pd

# Load a RoBERTa-based financial sentiment model from Hugging Face
model_name = "yiyanghkust/finbert-tone"  # Domain-specific (RoBERTa backbone)

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Set up sentiment pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Load your dataset
input_file = "data/all_headlines.csv"
df = pd.read_csv(input_file)

# Make sure the column exists
if "headline" not in df.columns:
    raise ValueError("Column 'headline' not found in CSV file.")

# Run sentiment analysis
results = sentiment_pipeline(df["headline"].tolist(), truncation=True, padding=True)

# Append results to the DataFrame
df["label"] = [r["label"] for r in results]
df["score"] = [round(r["score"], 4) for r in results]

# Save to new CSV
output_file = "data/all_headlines_with_sentiment.csv"
df.to_csv(output_file, index=False)

print(f"Sentiment results saved to: {output_file}")