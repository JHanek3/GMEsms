from datetime import datetime
from time import sleep
import pyEX as p
from twilio.rest import Client


import config

account_sid = config.account_sid
auth_token = config.auth_token
client = Client(account_sid, auth_token)

now = datetime.now()
marketOpen = now.replace(hour=8, minute=30, second=0, microsecond=0)
marketClose = now.replace(hour=15, minute=0, second=0, microsecond=0)

c = p.Client(api_token=config.api_token, version='stable')
sym="GME"

def stock(prev, current):
    fivePercent = (prev * .05) + prev
    if fivePercent <= current:
        return True
    else:
        return False


def main():
    calls = 0
    while(marketOpen <= now <= marketClose):
        d = c.quote(symbol=sym)
        
        if calls == 0:
            prevStock = d['previousClose']
            latestStock = d['latestPrice']
        calls += 1

        if stock(prevStock, latestStock):
            client.api.account.messages.create(
                to="+13316252959",
                from_="+17177440787",
                body="GME Current Price ${}, Previous Price ${}".format(latestStock, prevStock))
        
        print("Current Price: {}".format(latestStock))
        prevStock = latestStock
        sleep(300) 
main()
