from transformers import pipeline

class SentimentAgent:
    def __init__(self):
        self.nlp = pipeline("sentiment-analysis")

    def analyze_sentiment(self, messages):
        scores = []
        for msg in messages:
            result = self.nlp(msg)[0]
            score = result['score'] if result['label'] == 'POSITIVE' else -result['score']
            scores.append(score)
        return sum(scores) / len(scores) if scores else 0