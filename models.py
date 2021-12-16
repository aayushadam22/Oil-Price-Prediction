def runArimaAndHwaas(days):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import datetime
    #Reading data and preprocessing
    data=pd.read_csv('data.csv')
    data['Date']=pd.to_datetime(data['Date'])
    data.set_index('Date',inplace=True)
    idx = pd.date_range('2007-07-30', datetime.date.today()-datetime.timedelta(1))
    data = data.reindex(idx, fill_value=0)
    for i in range(len(data)):
        if int(data.iloc[i])==0:
            try:
                data.iloc[i]=(data.iloc[i+1]-data[i-1])/2
            except:
                if i>0:
                    data.iloc[i]=data.iloc[i-1]

    #Fitting HWAAS model
    from atspy import AutomatedModel
    model_list = ["HWAAS"]
    am = AutomatedModel(df = data , model_list=model_list,forecast_len=days)
    forecast_out = am.forecast_outsample()

    #Fitting ARIMA model
    from statsmodels.tsa.arima_model import ARIMA
    model=ARIMA(data,order=(5,1,0))
    result=model.fit(disp=0)
    fc,se,conf=result.forecast(days)
    fc=pd.Series(fc,index=forecast_out.index)
    lower=pd.Series(conf[:,0],index=forecast_out.index)
    upper=pd.Series(conf[:,1],index=forecast_out.index)

    plt.figure(figsize=(16,8))
    plt.plot(data[-30:],label='Past',c='orange')
    plt.plot(forecast_out,label='Forecast',c='r')
    plt.plot([data.index[-1],forecast_out.index[0]],[data.iloc[-1],forecast_out.iloc[0]],c='r')
    plt.plot(fc,label='Trend',c='green')
    plt.fill_between(forecast_out.index,lower,upper,color='k',alpha=0.1)
    plt.title('Forecast')
    plt.legend(loc='upper left')
    plt.savefig('outputs/plot.png')
    plt.savefig('static/plot.png')

    lower.to_csv('outputs/lower.csv')
    upper.to_csv('outputs/upper.csv')
    forecast_out.to_csv('outputs/forecast.csv')
