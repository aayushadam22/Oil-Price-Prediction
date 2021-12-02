from flask import Flask, render_template, url_for, request, redirect
import numpy as np
import pandas as pd
import models

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        days = request.form['days']
        try:
            days=int(days)
            if days>30:
                days=30
        except:
            return "Enter an integer"

        models.runArimaAndHwaas(days)
        forecasts=pd.read_csv('outputs/forecast.csv')
        forecasts=forecasts['HWAAS'].values.tolist()
        lower=pd.read_csv('outputs/lower.csv')
        lower=lower['0'].values.tolist()
        upper=pd.read_csv('outputs/upper.csv')
        upper=upper['0'].values.tolist()
        return render_template('prediction.html',forecasts=forecasts,lower=lower,upper=upper,days=days)
    else:
        return render_template('index.html')

def download_data():
    import yfinance as yf
    from yahoofinancials import YahooFinancials
    data = yf.download('BZ=F', start='2007-07-30', end='2021-11-30', progress=False)
    data=data.drop(['Open','High','Low','Close','Volume'],axis=1)
    data.columns=['Price']
    data.to_csv('data.csv')

if __name__=="__main__":
    try:
        download_data()
    except:
        data=pd.read_csv('data.csv')
    app.run(debug=True)
