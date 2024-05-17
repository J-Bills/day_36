import requests
import pandas as pd
import json
from twilio.rest import Client
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"


##Twilio Setup
account_sid = os.environ('TWILIO_ACCOUNT_SID')
auth_token = os.environ('TWILIO_AUTH_TOKEN')
client = Client(account_sid=account_sid, auth_token=auth_token)

#Move this down later
# message = client.messages \
#     .create(
#         body='This is the ship that made the Kessel Run in fourteen parsecs?',
#         from_='+15017122661',
#         to='+15558675310'
#     )

##avantage setup
avantage_key = os.environ('ALPHAAVANTAGE_KEY')

print(avantage_key)



## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

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

