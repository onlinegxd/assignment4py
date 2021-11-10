# Specific Cryptocurrency News Scrapper and Summarizer

### Installation
Copy from source
```bash
git clone https://github.com/onlinegxd/assignment4py
```

### Usage

```python
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
```

### Examples

Write any existing cryptocurrency name to see summarized articles and save them into DataBase

There're two database tables

First one contains information about Coin

Coin
| id | coin_name|
| -- | -------- |

if new Coin is provided add them to database, e.g.

| id | coin_name|
| -- | -------- |
|  1 |  Bitcoin |
|1027|  Ethereum|

Second contains information about articles

| article_id | article_text | coin_id |
| ---------- | ------------ | ------- |

if new Article is provided add them to database

*coin_id provided is taken from coinmarketcap.com

Usage examples:

(/coin) - Only existing route containing text-feild and button, by which you find the articles for provided coin
![image](https://user-images.githubusercontent.com/80266425/141168243-70c4c272-ce28-4b1e-ad0a-a08b608d4d81.png)
If provided coin is not found outputs following text
![image2](https://user-images.githubusercontent.com/80266425/141168395-b47c64f7-2d26-4579-a0b0-b0a7e9062142.png)
View from the database
![image3](https://user-images.githubusercontent.com/80266425/141168551-ad433338-486a-457e-ab6f-ea73b31c0281.png)
![image4](https://user-images.githubusercontent.com/80266425/141168680-5217cdf1-8b33-499d-8359-143d07de0121.png)
If new coin is provided adds them and their articles to database
![image5](https://user-images.githubusercontent.com/80266425/141168850-c01b5407-d227-4f38-a5be-ecaea1057980.png)
![image6](https://user-images.githubusercontent.com/80266425/141168918-f60c3767-b2bb-4bfb-b409-52236da6e4ae.png)
![image7](https://user-images.githubusercontent.com/80266425/141169003-6fff28c6-c400-4f0a-bc36-24fd713a7764.png)
