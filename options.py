import numpy as np
import scipy.stats as sps
from scipy.optimize import newton

#######################################
# Option class (European BSM pricing) #
#######################################

class Option:
    def __init__(self, S0, K, r, T, sigma, option_type):
        self.S0 = S0
        self.K = K
        self.r = r
        self.T = T
        self.sigma = sigma
        self.option_type = option_type

    def d1(self):
        return (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
    
    def d2(self):
        return self.d1() - self.sigma * np.sqrt(self.T)
    
    def price(self):
        if self.option_type == 'call':
            return self.S0 * sps.norm.cdf(self.d1()) - self.K * np.exp(-self.r * self.T) * sps.norm.cdf(self.d2())
        elif self.option_type == 'put':
            return self.K * np.exp(-self.r * self.T) * sps.norm.cdf(-self.d2()) - self.S0 * sps.norm.cdf(-self.d1())
        else:
            return None
        
    def delta(self):
        if self.option_type == 'call':
            return sps.norm.cdf(self.d1())
        elif self.option_type == 'put':
            return sps.norm.cdf(self.d1()) - 1
        else:
            return None
        
    def gamma(self):
        return sps.norm.pdf(self.d1()) / (self.S0 * self.sigma * np.sqrt(self.T))
    
    def theta(self):
        if self.option_type == 'call':
            return -self.S0 * sps.norm.pdf(self.d1()) * self.sigma / (2 * np.sqrt(self.T)) - self.r * self.K * np.exp(-self.r * self.T) * sps.norm.cdf(self.d2())
        elif self.option_type == 'put':
            return -self.S0 * sps.norm.pdf(self.d1()) * self.sigma / (2 * np.sqrt(self.T)) + self.r * self.K * np.exp(-self.r * self.T) * sps.norm.cdf(-self.d2())
        else:
            return None
        
    def vega(self):
        return self.S0 * sps.norm.pdf(self.d1()) * np.sqrt(self.T)
    
    def rho(self):
        if self.option_type == 'call':
            return self.K * self.T * np.exp(-self.r * self.T) * sps.norm.cdf(self.d2())
        elif self.option_type == 'put':
            return -self.K * self.T * np.exp(-self.r * self.T) * sps.norm.cdf(-self.d2())
        else:
            return None
        
    def implied_volatility(self, price):
        def f(sigma):
            self.sigma = sigma
            return np.abs(self.price() - price)
        return newton(f, 0.5)
    
    def __str__(self):
        return 'Option(S0={}, K={}, r={}, T={}, sigma={}, option_type={})'.format(self.S0, self.K, self.r, self.T, self.sigma, self.option_type)
    
    def __repr__(self):
        return self.__str__()
    

####################
# OptionData class #
####################

from yahoo_fin import options
import datetime
import pandas as pd
import matplotlib.pyplot as plt

class OptionData:
    def __init__(self, ticker, type='call'):
        self.ticker = ticker
        self.maturities = options.get_expiration_dates(ticker)
        self.data_by_maturity = []
        for maturity in self.maturities:
            if type == 'call':
                data = options.get_calls(ticker, maturity)
            else:
                data = options.get_puts(ticker, maturity)
            self.data_by_maturity.append(data)
        self.df = self._compute_dataframe()
        
    def __str__(self):
        return f'{self.ticker} options data for calls with {len(self.maturities)} maturities'
    
    def __repr__(self):
        return f'{self.ticker} options data for calls with {len(self.maturities)} maturities'
    
    def _compute_dataframe(self):
        # create a dataframe with all the data
        # first get the current date 
        current_date = datetime.datetime.now()
        maturities_dates = [datetime.datetime.strptime(maturity, '%B %d, %Y') for maturity in self.maturities]
        maturities_days = [(maturity_date - current_date).days for maturity_date in maturities_dates]
        df = pd.DataFrame()
        for i in range(len(self.maturities)):
            data = self.data_by_maturity[i]
            data['Days to maturity'] = maturities_days[i]
            df = pd.concat([df, data])

        IV = df['Implied Volatility'].values
        for i in range(len(IV)):
            s = IV[i]
            for c in ['%', ',']:
                s = s.replace(c, '')
            IV[i] = float(s)/100
        df['Implied Volatility'] = IV

        return df
    
    def get_dataframe(self):
        return self.df
    
    def save_to_csv(self, filename):
        self.df.to_csv(filename)
        print(f'Saved to {filename}')

    def load_from_csv(self, filename):
        self.df = pd.read_csv(filename)
        print(f'Loaded from {filename}')

    def plot_smile(self, days_to_maturity):
        data = self.df[self.df['Days to maturity'] == days_to_maturity]
        if len(data) == 0:
            print('No data for this maturity')
            return
        plt.plot(data['Strike'], data['Implied Volatility'])
        plt.xlabel('Strike')
        plt.ylabel('Implied Volatility')
        plt.title(f'{self.ticker} Implied Volatility for maturity of {days_to_maturity} days')
        plt.show()
    
