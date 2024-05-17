import requests
from newsapi import NewsApiClient
from twilio.rest import Client
import os
import datetime as dt

STOCK = "TSLA"
COMPANY_NAME = "Tesla"

Percentage = 5

def check_stock():
    stock_parameters = {
        'function':'TIME_SERIES_DAILY',
        'symbol':STOCK,
        'apikey':avantage_key
    }

    avantage_key = os.environ['ALPHAVANTAGE_KEY']
    response = requests.get(url='https://www.alphavantage.co/query',params=stock_parameters)
    response.raise_for_status()
    data = response.json()


    today = dt.date.today()
    target_days = list()
    for i in range(1,3):
        date = today - dt.timedelta(days=i)
        target_days.append(str(date))

    target_data = dict()
    dates = data['Time Series (Daily)']
    for date,val in dates.items():
        if date in target_days:
            target_data[date] = val

    yesterday_open_data = float(target_data[target_days[0]]['1. open'])
    db4yesterday_open_data = float(target_data[target_days[1]]['1. open'])

    percentage_val = round(((yesterday_open_data - db4yesterday_open_data)/db4yesterday_open_data) * 100,2)
    Percentage = percentage_val
    if percentage_val > 5.00 or percentage_val < -5.00:
        return True

##News API Setup
def get_news():
    newsapi_key = os.environ["NEWS_KEY"]
    
    news_parameters = {
    'q':COMPANY_NAME,
    'apiKey':newsapi_key,
    'language':'en',
    "category":"business",
    }
    
    response  = requests.get('https://newsapi.org/v2/top-headlines',params=news_parameters)
    response.raise_for_status()

    data = response.json()

    headlines = dict()
    articles = data.get('articles')
    try:
        for article in articles:
            headlines.update({article['title']:article['description']})
    except IndexError:
        pass
    return headlines

def send_message(headlines):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    twilio_num = os.environ['TWILIO_NUM']
    client = Client(account_sid, auth_token)
    
    text_info=''
    
    percent_string = f"{STOCK}: {Percentage}% \n"
    for key,value in headlines.items():
        text_info += f'Headline:{key} \n Brief:{value} \n'
        

    full_text = percent_string + text_info

    message = client.messages \
        .create(
            body=full_text,
            from_=twilio_num,
            to='+11111111'
        )
    
    print(full_text)
    
    
    
def main():
    val = check_stock
    if (val):
        news = get_news()
        send_message(news)
    
main()
    


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

