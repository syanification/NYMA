import finnhub
import config
import json
from datetime import datetime, timedelta

def pull_news():
    company_list = ['META', 'AAPL', 'AMZN', 'NFLX', 'GOOGL']

    date_today = datetime.today().strftime('%Y-%m-%d')
    date_weekago = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')

    finnhub_client = finnhub.Client(api_key=config.FINN_API_KEY)

    combined_data = {}

    for ticker in company_list:
        # Fetch company news
        news_data = finnhub_client.company_news(ticker, _from=date_weekago, to=date_today)

        # Extract only the headline and summary, and limit to 50 objects
        filtered_news_data = [
            {"headline": item["headline"], "summary": item["summary"]}
            for item in news_data
        ][:50]  # Limit to the first 50 items

        # Fetch recommendation data
        rec_data = finnhub_client.recommendation_trends(ticker)

        # Combine the news data and recommendation for the company
        combined_data[ticker] = {
            "news": filtered_news_data,
            "recommendation": rec_data
        }

    # Save the combined data to a single JSON file
    with open('combined_news.json', 'w') as json_file:
        json.dump(combined_data, json_file, indent=4)

    return 1

pull_news()