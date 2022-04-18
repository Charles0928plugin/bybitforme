from logging import warning
import warnings
import pandas as pd
import datetime
import requests
from pybit import HTTP
#from pybit.usdt_perpetual import HTTP
import time
import calendar 
from datetime import datetime, timedelta, timezone
warnings.filterwarnings("ignore")

apiKey='ChcpTfaqSxyxCVRu9G'

apisecret='VvathRxyeHTPFijw8e6cmXleJu5hoTgAi4hq'

#symbol to be traded
symbol='BTCUSD'

#candle in minutes
tick_interval = '1'

#quantity to be traded in USD
qty1=13


while True:

    bybitticker=symbol
    print(symbol)   

    now = datetime.utcnow()
    unixtime = calendar.timegm(now.utctimetuple())
    since = unixtime

    start=str(since-60*60*int(tick_interval))    

    #spot
    url = 'https://api.bybit.com/v2/public/kline/list?symbol='+bybitticker+'&interval='+tick_interval+'&from='+str(start)
    #derivatives
    #url = 'https://api.bybit.com/public/linear/kline?symbol='+bybitticker+'&interval='+tick_interval+'&from='+str(start)
 
    
    data = requests.get(url).json()

    D = pd.DataFrame(data['result'])


    marketprice = 'https://api.bybit.com/v2/public/tickers?symbol=' + symbol
    res = requests.get(marketprice)
    data = res.json()
    lastprice = float(data['result'][0]['last_price'])
    
    price=lastprice
    
    df=D['close']
    
       
    ma9 = df.rolling(window=9).mean()
    ma26 = df.rolling(window=26).mean()
    
    test1=ma9.iloc[-2]-ma26.iloc[-2]
    test2=ma9.iloc[-1]-ma26.iloc[-1]
    
    session = HTTP(
        endpoint='https://api.bybit.com', 
        api_key=apiKey,
        api_secret=apisecret)
    



    positionsize=session.my_position(symbol= symbol)['result']['size']
    
    if session.my_position(symbol= symbol)['result']['side']=='Sell':
       positionsize=positionsize*-1 

        
    lastprice=float(session.latest_information_for_symbol(symbol=symbol)['result'][0]['last_price'])
         
    print(lastprice)
    call='None'
    try:
        if test1>0 and test2<0:
           if positionsize<0:
              print('skip')               
              continue
           call='Dead Cross' 
           qty=qty1 
           if positionsize>0:
              qty=qty1+abs(positionsize)
                
           session.place_active_order( symbol= symbol, order_type= 'Market', side= 'Sell', qty= qty,time_in_force= 'GoodTillCancel')

            
        if test1<0 and test2>0:
           if positionsize>0:
              print('skip')               
              continue  
           call='Golden Cross'  
           qty=qty1           
           if positionsize<0:
              qty=qty1+abs(positionsize)
           
           session.place_active_order( symbol= symbol, order_type= 'Market', side= 'Buy', qty= qty,time_in_force= 'GoodTillCancel')
            
    except:
        pass                
             

    print('MA 9: ', round(ma9.iloc[-1],2))
    print('MA 26: ', round(ma26.iloc[-1],2))
    print('Golden Cross/Dead Cross: ',call)
    print('')    
    

    time.sleep(2)


 



