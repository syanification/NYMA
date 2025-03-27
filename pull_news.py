import finnhub
import config
import json
from datetime import datetime, timedelta

def pull_news():
    company_list = ['META', 'AAPL', 'AMZN', 'NFLX', 'GOOGL']

    date_today = datetime.today().strftime('%Y-%m-%d')
    date_weekago = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')

    finnhub_client = finnhub.Client(api_key=config.FINN_API_KEY)

    for ticker in company_list:
        # Fetch company news
        news_data = finnhub_client.company_news(ticker, _from=date_weekago, to=date_today)

        # Extract only the headline and summary, and limit to 50 objects
        filtered_news_data = [
            {"headline": item["headline"], "summary": item["summary"]}
            for item in news_data
        ][:50]  # Limit to the first 50 items

        rec_data = finnhub_client.recommendation_trends(ticker)

        # Save the filtered news data to a JSON file
        with open(f'news/{ticker}_news.json', 'w') as json_file:
            json.dump(filtered_news_data, json_file, indent=4)

        # Save the recommendation data to a JSON file
        with open(f'recs/{ticker}_recs.json', 'w') as json_file:
            json.dump(rec_data, json_file, indent=4)

    return 1