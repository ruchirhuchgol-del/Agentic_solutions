from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

class FinancialSentimentModel:
    def __init__(self, model_path="models/finbert-tone"):
        self.model_path = model_path
        self.tokenizer = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            print(f"Loading existing model from {self.model_path}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
        else:
            print("Downloading FinBERT model...")
            self.tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
            self.model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")
            
            # Save model locally
            os.makedirs(self.model_path, exist_ok=True)
            self.tokenizer.save_pretrained(self.model_path)
            self.model.save_pretrained(self.model_path)
            print(f"Model saved to {self.model_path}")
        
        self.model.to(self.device)
        self.model.eval()

    def predict(self, texts):
        results = []
        for text in texts:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
                scores = predictions[0].cpu().numpy()
                
            sentiment_idx = scores.argmax()
            sentiment = ["positive", "negative", "neutral"][sentiment_idx]
            confidence = float(scores[sentiment_idx])
            
            results.append({
                "text": text,
                "sentiment": sentiment,
                "confidence": confidence,
                "scores": {
                    "positive": float(scores[0]),
                    "negative": float(scores[1]),
                    "neutral": float(scores[2])
                }
            })
        return results

# Singleton instance
_sentiment_model = None

def get_sentiment_model():
    global _sentiment_model
    if _sentiment_model is None:
        _sentiment_model = FinancialSentimentModel()
    return _sentiment_model