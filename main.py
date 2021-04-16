from datetime import datetime
from time import sleep
import pyEX as p
from twilio.rest import Client


import config

# Account setup for Twilio msg
account_sid = config.account_sid
auth_token = config.auth_token
client = Client(account_sid, auth_token)

# Setup for Stock API Call
c = p.Client(api_token=config.api_token, version='stable')
sym="GME"

# Current time
now = datetime.now()
# Time the market opens and closes
marketOpenTime = now.replace(hour=8, minute=30, second=0, microsecond=0)
marketCloseTime = now.replace(hour=15, minute=0, second=0, microsecond=0)

# Check if the price from 5 mins ago has jumped 5%
def stock(prev, current):
    fivePercent = (prev * .05) + prev
    if fivePercent <= current:
        return True
    else:
        return False

def main():
    calls = 0
    print("Script started")
    while(True):
        now = datetime.now()
        if (marketOpenTime <= now <= marketCloseTime):
            d = c.quote(symbol=sym)

            # prevents wrong exectuion if the program isn't started before market open
            if calls == 0:
                prevStock = d['previousClose']
            latestStock = d['latestPrice']

            # Sends a text message
            if stock(prevStock, latestStock):
                if (now != marketOpenTime and calls == 1):
                    client.api.account.messages.create(
                        to=config.my_number,
                        from_=config.twilio_number,
                        body="GME Current Price ${}, Previous Price ${}".format(latestStock, prevStock))
            
            print("Current Price: {}".format(latestStock))
        else:
            print("Market Closed")
            break;

        calls = 1
        prevStock = latestStock
        sleep(300)


main()