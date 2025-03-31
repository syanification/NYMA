import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax
import torch
import os
from statistics import mean

# Load FinBERT
tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")

def get_sentiment_score(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    probs = softmax(logits, dim=1)
    score = probs[0][2] - probs[0][0]
    return score.item()

def recommendation_score_block(blocks):
    scores = []
    for rec in blocks:
        score = (
            rec['strongBuy'] * 1.0 +
            rec['buy'] * 0.5 -
            rec['sell'] * 0.5 -
            rec['strongSell'] * 1.0
        ) / (rec['strongBuy'] + rec['buy'] + rec['hold'] + rec['sell'] + rec['strongSell'] + 1e-6)
        scores.append(score)
    return mean(scores)

def process_stock(ticker_data):
    news_items = ticker_data['news']
    sentiment_scores = []
    for item in news_items:
        text = f"{item['headline']} {item['summary']}"
        sentiment_scores.append(get_sentiment_score(text))
    avg_sentiment = mean(sentiment_scores) if sentiment_scores else 0
    avg_rec = recommendation_score_block(ticker_data['recommendation'])
    final_score = 0.6 * avg_sentiment + 0.4 * avg_rec
    return final_score

# Load the JSON file
with open("combined_news.json", "r") as f:
    data = json.load(f)

results = {}
for ticker, content in data.items():
    results[ticker] = process_stock(content)

# Output Ranking
ranked = sorted(results.items(), key=lambda x: -x[1])
print("\n📈 Top Buys:")
for t, s in ranked[:5]:
    print(f"{t}: {s:.3f}")
