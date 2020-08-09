# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import pandas_datareader
import pandas_datareader.data as web
from fbprophet import Prophet
import datetime
from flask import Flask, render_template
from flask import request, redirect
import os
import os.path
import csv
# from itertools import zip_longest
from csv2json import *
import time

import bulbea as bb
from bulbea.learn.evaluation import split
import numpy as np
from bulbea.learn.models import RNN
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as pplt

app = Flask(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
    
@app.route("/")
def first_page():
    """
    original_end = 175
    forecast_start = 200
    stock = "IBM"
    return render_template("plot.html", original = original_end, forecast = forecast_start, stock_tinker = stock)
    """
    tmp = os.path.join(dir_path, "static/prophet.png")
    tmp_csv = os.path.join(dir_path, "static/numbers.csv")
    if os.path.exists(tmp):
        os.remove(tmp)
    if os.path.exists(tmp_csv):
        os.remove(tmp_csv)
    return render_template("index.html")

#function to get stock data
def yahoo_stocks(symbol, start, end):
    while(True):
        try:
            return web.DataReader(symbol, 'yahoo', start, end)
        except pandas_datareader._utils.RemoteDataError:
            print("can't get data, wait 1s...")
            time.sleep(1)

def get_historical_stock_price(stock):
    print ("Getting historical stock prices for stock ", stock)
    
    #get 7 year stock data for Apple
    startDate = datetime.datetime(2010, 1, 4)
    #date = datetime.datetime.now().date()
    #endDate = pd.to_datetime(date)
    endDate = datetime.datetime(2017, 11, 28)
    stockData = yahoo_stocks(stock, startDate, endDate)
    return stockData

def fb_model(stock):
    df_whole = get_historical_stock_price(stock)

    df = df_whole.filter(['Close'])

    df['ds'] = df.index
    # log transform the ‘Close’ variable to convert non-stationary data to stationary.
    df['y'] = np.log(df['Close'])
    original_end = df['Close'][-1]

    model = Prophet()
    model.fit(df)

    # num_days = int(input("Enter no of days to predict stock price for: "))

    num_days = 10
    future = model.make_future_dataframe(periods=num_days)
    forecast = model.predict(future)

    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

    # Prophet plots the observed values of our time series (the black dots), the forecasted values (blue line) and
    # the uncertainty intervalsof our forecasts (the blue shaded regions).

    # forecast_plot = model.plot(forecast)
    # forecast_plot.show()

    # make the vizualization a little better to understand
    df.set_index('ds', inplace=True)
    forecast.set_index('ds', inplace=True)
    # date = df['ds'].tail(plot_num)

    viz_df = df.join(forecast[['yhat', 'yhat_lower', 'yhat_upper']], how='outer')
    viz_df['yhat_scaled'] = np.exp(viz_df['yhat'])

    # close_data = viz_df.Close.tail(plot_num)
    # forecasted_data = viz_df.yhat_scaled.tail(plot_num)
    # date = future['ds'].tail(num_days+plot_num)

    close_data = viz_df.Close
    forecasted_data = viz_df.yhat_scaled
    date = future['ds']
    # date = viz_df.index[-plot_num:-1]
    forecast_start = forecasted_data[-num_days]

    d = [date, close_data, forecasted_data]
    export_data = zip_longest(*d, fillvalue='')
    with open(os.path.join(dir_path, 'static/numbers.csv'), 'w+') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("Date", "Actual", "Forecasted"))
        wr.writerows(export_data)

    stock = stock.lower()
    #csv2json('static/numbers.csv', 'static/data/json/' + stock + '.json', 'Actual')
    csv2json('static/numbers.csv', 'static/data/json/' + stock + '_fbprophet' + '.json', 'Forecasted')

    name_list = [stock + '_fbprophet']
    # myfile.close()

    #return render_template("plot.html", names=name_list, original=round(original_end, 2),
    #                       forecast=round(forecast_start, 2), stock_tinker=stock.upper())
    return name_list

def df2json(df, filepath, y_col):
    ISFIRST=True
    jsonfile = open(filepath, 'w')
    jsonfile.write('[')
    for index, row in df.iterrows():
        x = index
        y = row[y_col]
        if (is_number(y) and not math.isnan(y)):
            if (not ISFIRST):
                jsonfile.write(',\n')
            # x0=datetime.fromtimestamp(x)
            x0 = int(x.strftime("%s")) * 1000
            jsonfile.write("[%s,%s]" % (x0, y))
            ISFIRST = False
    jsonfile.write(']')

def bulbea_model(stock):
    print("fb model...")
    names2 = fb_model(stock)

    print("download data...")
    share = bb.Share('WIKI', stock)
    share.data['Date']=share.data.index
    Xtrain, Xtest, ytrain, ytest = split(share, 'Close', normalize=True)
    _, _, date_train, date_test = split(share, 'Date', normalize=False)
    Xtrain = np.reshape(Xtrain, (Xtrain.shape[0], Xtrain.shape[1], 1))
    Xtest = np.reshape(Xtest, (Xtest.shape[0], Xtest.shape[1], 1))

    print("run RNN...")
    rnn = RNN([1, 10, 10, 1])
    rnn.fit(Xtrain, ytrain)

    p = rnn.predict(Xtest)
    p = p.flatten()
    print(mean_squared_error(ytest, p))

    print("analyzie twitter...")
    sentiment7days, sentiment_date = bb.sentiment(share)
    print(sentiment7days)

    d = {'Date': pd.Series(date_test, index=date_test),
         'Actual': pd.Series(ytest, index=date_test),
         'Forecasted': pd.Series(p, index=date_test)
         }
    d2={'Date': pd.Series(sentiment_date, index=sentiment_date),
        'Sentiment': pd.Series(sentiment7days, index=sentiment_date)
        }

    df = pd.DataFrame(d)
    df2 = pd.DataFrame(d2)
    #df['Sentiment'] = pd.Series(sentiment7days, index=sentiment_date)
    #p['Actual'] = ytest
    #p['Date'] = p.index
    stock = stock.lower()
    csvfile = 'static/'+stock+'_rnn.csv'
    df.to_csv(csvfile, sep=',')

    csv2json(csvfile, 'static/data/json/' + stock + '.json', 'Actual')
    csv2json(csvfile, 'static/data/json/' + stock + '_rnn' + '.json', 'Forecasted')

    df2json(df2, 'static/data/json/' + stock + '_sentiment' + '.json', 'Sentiment')
    #csv2json(csvfile, 'static/data/json/' + stock + '_sentiment' + '.json', 'Sentiment')

    name_list = [stock, stock + '_rnn', stock + '_sentiment']
    # myfile.close()

    return render_template("plot.html", names=name_list, names2=names2)


@app.route("/plot" , methods = ['POST', 'GET'] )
def main():
    if request.method == 'POST':
        stock = request.form['companyname']
        #ret = fb_model(stock)
        ret = bulbea_model(stock)
        return ret
        #return render_template("plot.html", name=name_list)
'''
if __name__ == "__main__":
    main()
'''

if __name__ == "__main__":
    #bulbea_model("AAPL")
    app.run(debug=True, threaded=True)
