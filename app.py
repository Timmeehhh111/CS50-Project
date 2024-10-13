from flask import Flask, render_template, request, jsonify
import numpy as np
from scipy.stats import norm
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

def black_scholes(S, K, T, r, sigma, option_type="call"):
    # S = current stock price
    # K = strike price
    # T = time to maturity in years
    # r = risk-free interest rate
    # sigma = volatility
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == "call":
        option_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        option_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    return option_price

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    S = float(data['S'])
    K = float(data['K'])
    T = float(data['T'])
    r = float(data['r'])
    sigma = float(data['sigma'])
    option_type = data['optionType']

    price = black_scholes(S, K, T, r, sigma, option_type)
    
    # Create Plotly graph
    S_range = np.linspace(S * 0.5, S * 1.5, 100)
    prices = [black_scholes(s, K, T, r, sigma, option_type) for s in S_range]
    fig = go.Figure(data=[go.Scatter(x=S_range, y=prices, mode='lines', name='Option Price')])
    fig.update_layout(title='Option Price vs Stock Price', xaxis_title='Stock Price', yaxis_title='Option Price')

    graphJSON = pio.to_json(fig)
    
    return jsonify({'price': price, 'graphJSON': graphJSON})

if __name__ == '__main__':
    app.run(debug=True)