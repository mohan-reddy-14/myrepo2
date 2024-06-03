from flask import Flask, request, jsonify
import requests
import schedule
import time

app = Flask(__name__)
NEWS_API_KEY = '75958ae4079c403491d1e9d5454809fa'

def search_real_estate_news():
    news_sources = ['bloomberg', 'cnbc', 'forbes', 'business-insider']

    all_articles = []

    for source in news_sources:
        news_api_url = f'https://newsapi.org/v2/everything?q=real+estate&sources={source}&apiKey={NEWS_API_KEY}'
        response = requests.get(news_api_url)
        if response.status_code == 200:
            news_data = response.json()
            if 'articles' in news_data:
                all_articles.extend(news_data['articles'])

    return all_articles

@app.route('/search_real_estate_news', methods=['GET'])
def get_real_estate_news():
    real_estate_articles = search_real_estate_news()
    return jsonify({'articles': real_estate_articles, 'totalResults': len(real_estate_articles), 'status': 'ok'})

def daily_job():
    search_real_estate_news()

if __name__ == '__main__':
    schedule.every().day.at("08:00").do(daily_job)
    app.run(debug=True)

    while True:
        schedule.run_pending()
        time.sleep(1)
