import numpy as np
import scipy.stats as sps
from scipy.optimize import newton

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