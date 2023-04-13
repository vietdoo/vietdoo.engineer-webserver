from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


analyzer = SentimentIntensityAnalyzer()
sentiment_score = analyzer.polarity_scores('i have some trouble')

print(sentiment_score)