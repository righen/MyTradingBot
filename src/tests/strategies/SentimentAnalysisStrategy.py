import backtrader as bt
import requests
import json


class SentimentAnalysisStrategy(bt.Strategy):
    params = (
        ('sentiment_api_url', 'https://api.edenai.run/v2/text/sentiment_analysis'),
        ('api_key',
         'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiODhiZDQ2ZGYtNTA5MS00ZTQ5LWExZjktN2JkYjdmYWQ2OTI2IiwidHlwZSI6ImFwaV90b2tlbiJ9.JzU17i11IImas3dggBlN-jNdmhXdGyGO1n6dLrR-gCk'),
        # Replace with your actual API key
        ('sentiment_threshold', 0.1),  # Adjust based on your needs
    )

    def __init__(self):
        self.sentiment = 0

    def get_sentiment(self, text):
        headers = {"Authorization": self.params.api_key}
        payload = {
            "providers": "google,amazon",
            "language": "en",
            "text": text,
        }
        try:
            response = requests.post(self.params.sentiment_api_url, json=payload, headers=headers)
            data = response.json()
            # Assuming you are using Google's sentiment score
            if 'google' in data and 'items' in data['google']:
                sentiment_scores = [self.map_sentiment_label_to_score(item['sentiment']) for item in
                                    data['google']['items']]
                # Calculate the average sentiment score
                self.sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
            else:
                self.sentiment = 0
        except Exception as e:
            self.sentiment = 0
            print(f"Error fetching sentiment: {e}")

    def map_sentiment_label_to_score(self, label):
        if label == 'Positive':
            return 1.0
        elif label == 'Negative':
            return -1.0
        else:
            return 0.0

    def next(self):
        # Use the close price as the text for sentiment analysis (for demonstration purposes)
        text = f"The stock price is {self.data.close[0]}"
        self.get_sentiment(text)

        if self.sentiment > self.params.sentiment_threshold:
            self.buy()
        elif self.sentiment < -self.params.sentiment_threshold:
            self.sell()
