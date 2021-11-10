from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from requests import Session
import json
# For article summary
import nltk
from newspaper import Article
# For news extract
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123321@localhost/Assignment4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '54027113-f309-4184-8950-3d1f53aca5dd'
}

get_id_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
get_news_url = 'https://api.coinmarketcap.com/content/v3/news?coins='

nltk.download('punkt')

session = Session()
session.headers.update(headers)


class Coin(db.Model):
    __tablename__ = 'Coin'
    id = db.Column('id', db.Integer, primary_key=True)
    coin_name = db.Column('coin_name', db.Unicode)

    def __init__(self, id, coin_name):
        self.id = id,
        self.coin_name = coin_name


class Articles(db.Model):
    __tablename__ = 'Articles'
    article_id = db.Column('article_id', db.Integer, primary_key=True, autoincrement=True)
    article_text = db.Column('article_text', db.UnicodeText)
    coin_id = db.Column('coin_id', db.Integer)

    def __init__(self, article_id, article_text, coin_id):
        self.article_id = article_id,
        self.article_text = article_text,
        self.coin_id = coin_id


def get_coin_id(coin):
    parameters = {
        'slug': coin
    }
    response = session.get(get_id_url, params=parameters)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return 0
    for x in json.loads(response.content)['data']:
        id = json.loads(response.content)['data'][x]['id']
    return id


def get_coin_news(coin_id):
    page = requests.get(get_news_url+str(coin_id))
    urls = []
    for url in json.loads(page.content)['data']:
        urls.append(url['meta']['sourceUrl'])
    return urls


def get_coin_article(coin_news_url):
    article = Article(coin_news_url)
    article.download()
    article.parse()
    article.nlp()
    return article.summary


@app.route('/coin', methods=['GET', 'POST'])
def form():
    coin = request.form.get('coin')
    coin_id = get_coin_id(coin.lower())
    print(coin_id)
    if coin_id == 0:
        return '''
            <form method="POST">
                <div>
                    <label>Coin: <input type="text" name="coin"></label>
                    <input type="submit" value="Submit">
                </div>
            </form>

            <h2>Bad Request, given coin not found</h2>'''
    row = Coin.query.filter_by(id=coin_id).first()

    if row is None:
        new_coin = Coin(coin_id, coin)
        db.session.add(new_coin)
        db.session.commit()

    coin_news = get_coin_news(coin_id)
    articles = ""
    for coin_news_url in coin_news:
        article = get_coin_article(coin_news_url)
        row = Articles.query.filter_by(article_text=article).first()

        if row is None:
            max_id = db.session.query(func.max(Articles.article_id)).scalar()
            if max_id is None:
                new_article = Articles(1, article, coin_id)
            else:
                new_article = Articles(max_id+1, article, coin_id)
            db.session.add(new_article)
            db.session.commit()

        articles += '<p>' + article + '</p>' + '\n'
    return '''
        <form method="POST">
               <div>
                    <label>Coin: <input type="text" name="coin"></label>
                    <input type="submit" value="Submit">
               </div>
        </form>

        <h2>Related articles:</h2> {}'''.format(articles)


if __name__ == '__main__':
    app.run(debug=True)
