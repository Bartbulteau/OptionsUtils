import tkinter as tk
from options import Option

# default values
S0 = 100
K = 100
r = 0.05
T = 1
sigma = 0.2
option_type = 'call'

option = Option(S0, K, r, T, sigma, option_type)

# set up the GUI size
root = tk.Tk()

# first column
S0_label = tk.Label(text='S0')
S0_label.grid(row=0, column=0)
S0_entry = tk.Entry(root)
S0_entry.grid(row=0, column=1)
S0_entry.insert(0, str(S0))

K_label = tk.Label(text='K')
K_label.grid(row=1, column=0)
K_entry = tk.Entry()
K_entry.grid(row=1, column=1)
K_entry.insert(0, str(K))

r_label = tk.Label(text='r')
r_label.grid(row=2, column=0)
r_entry = tk.Entry()
r_entry.grid(row=2, column=1)
r_entry.insert(0, str(r))

T_label = tk.Label(text='T')
T_label.grid(row=3, column=0)
T_entry = tk.Entry()
T_entry.grid(row=3, column=1)
T_entry.insert(0, str(T))

sigma_label = tk.Label(text='sigma')
sigma_label.grid(row=4, column=0)
sigma_entry = tk.Entry()
sigma_entry.grid(row=4, column=1)
sigma_entry.insert(0, str(sigma))

option_type_label = tk.Label(text='option type')
option_type_label.grid(row=5, column=0)
option_type_str = tk.StringVar()
option_type_option_menu = tk.OptionMenu(root, option_type_str, 'call', 'put')
option_type_option_menu.grid(row=5, column=1)
option_type_str.set(option_type)

# second column
price = tk.Label(text='Price')
price.grid(row=0, column=2)
price_value = tk.Label(text='0')
price_value.grid(row=0, column=3)

delta = tk.Label(text='Delta')
delta.grid(row=1, column=2)
delta_value = tk.Label(text='0')
delta_value.grid(row=1, column=3)

gamma = tk.Label(text='Gamma')
gamma.grid(row=2, column=2)
gamma_value = tk.Label(text='0')
gamma_value.grid(row=2, column=3)

theta = tk.Label(text='Theta')
theta.grid(row=3, column=2)
theta_value = tk.Label(text='0')
theta_value.grid(row=3, column=3)

vega = tk.Label(text='Vega')
vega.grid(row=4, column=2)
vega_value = tk.Label(text='0')
vega_value.grid(row=4, column=3)

rho = tk.Label(text='Rho')
rho.grid(row=5, column=2)
rho_value = tk.Label(text='0')
rho_value.grid(row=5, column=3)

# third column
def calculate():
    option.S0 = float(S0_entry.get())
    option.K = float(K_entry.get())
    option.r = float(r_entry.get())
    option.T = float(T_entry.get())
    option.sigma = float(sigma_entry.get())
    option.option_type = option_type_str.get()
    
    price_value.config(text=str(round(option.price(), 3)))
    delta_value.config(text=str(round(option.delta(), 3)))
    gamma_value.config(text=str(round(option.gamma(), 3)))
    theta_value.config(text=str(round(option.theta(), 3)))
    vega_value.config(text=str(round(option.vega(), 3)))
    rho_value.config(text=str(round(option.rho(), 3)))

calculate_button = tk.Button(text='Calculate', command=calculate)
calculate_button.grid(row=6, column=3)

# fourth column

price_label = tk.Label(text='Price')
price_label.grid(row=1, column=4)
price_entry = tk.Entry()
price_entry.grid(row=1, column=5)
price_entry.insert(0, str(round(option.price(), 3)))

implied_volatility = tk.Label(text='Implied Volatility')
implied_volatility.grid(row=2, column=4)
implied_volatility_value = tk.Label(text='0')
implied_volatility_value.grid(row=2, column=5)

def calculate_implied_volatility():
    price = float(price_entry.get())
    implied_volatility_value.config(text=str(round(option.implied_volatility(price), 3)))

calculate_implied_volatility_button = tk.Button(text='Calculate', command=calculate_implied_volatility)
calculate_implied_volatility_button.grid(row=3, column=5)

# adapt window size to the number of widgets
root.grid_rowconfigure(6, minsize=50)
root.grid_columnconfigure(5, minsize=50)

# name the window
root.title('Black-Scholes Pricer')
calculate()
calculate_implied_volatility()

root.mainloop()