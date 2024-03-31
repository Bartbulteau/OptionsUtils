import tkinter as tk
from options import Option
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import yfinance as yf

sns.set()

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

###############
# MAIN WINDOW #
###############

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
def update():
    option.S0 = float(S0_entry.get())
    option.K = float(K_entry.get())
    option.r = float(r_entry.get())
    option.T = float(T_entry.get())
    option.sigma = float(sigma_entry.get())
    option.option_type = option_type_str.get()


def calculate():
    update()
    price_value.config(text=str(round(option.price(), 3)))
    delta_value.config(text=str(round(option.delta(), 3)))
    gamma_value.config(text=str(round(option.gamma(), 3)))
    theta_value.config(text=str(round(option.theta(), 3)))
    vega_value.config(text=str(round(option.vega(), 3)))
    rho_value.config(text=str(round(option.rho(), 3)))

calculate_button = tk.Button(text='Calculate', command=calculate)
calculate_button.grid(row=6, column=3)

# adapt window size to the number of widgets
root.grid_rowconfigure(6, minsize=50)
root.grid_columnconfigure(3, minsize=50)
root.geometry('+%d+%d' % (50, 50))

# make window not resizable
root.resizable(False, False)

# name the window
root.title('Black-Scholes Pricer')
calculate()

#############################
# IMPLIED VOLATILITY WINDOW #
#############################

# create separate window for implied volatility
implied_volatility_window = tk.Toplevel(root)
implied_volatility_window.title('Implied Volatility')

# first column
price_label = tk.Label(implied_volatility_window, text='Price')
price_label.grid(row=0, column=0)

price_entry = tk.Entry(implied_volatility_window)
price_entry.grid(row=0, column=1)
price_entry.insert(0, str(round(option.price(), 3)))

# second column
implied_volatility_label = tk.Label(implied_volatility_window, text='Implied Volatility')
implied_volatility_label.grid(row=1, column=0)

implied_volatility_value = tk.Label(implied_volatility_window, text='0')
implied_volatility_value.grid(row=1, column=1)
implied_volatility_value.config(text=str(round(100*option.implied_volatility(option.price()), 3)) + '%')

# third column
def calculate_implied_volatility():
    update()
    price = float(price_entry.get())
    text = None
    try:
        text = str(round(100*option.implied_volatility(price), 3)) + '%'
        implied_volatility_value.config(text=text)
    except:
        text = 'N/A'
        implied_volatility_value.config(text=text)

calculate_implied_volatility_button = tk.Button(implied_volatility_window, text='Calculate', command=calculate_implied_volatility)
calculate_implied_volatility_button.grid(row=2, column=1)

# adapt window size to the number of widgets
implied_volatility_window.grid_rowconfigure(2, minsize=50)
implied_volatility_window.grid_columnconfigure(3, minsize=50)

# move the implied volatility window to the right of the main window
implied_volatility_window.geometry('+%d+%d' % (50 + 2.2*root.winfo_width(), 50))

# make window not resizable
implied_volatility_window.resizable(False, False)

###############
# PLOT WINDOW #
###############

# create separate window for the plot
plot_window = tk.Toplevel(root)
plot_window.title('Ticker Spot Price')

# first column
ticker_label = tk.Label(plot_window, text='Ticker')
ticker_label.grid(row=0, column=0)

ticker_entry = tk.Entry(plot_window)
ticker_entry.grid(row=0, column=1)
ticker_entry.insert(0, 'AAPL')

time_span_label = tk.Label(plot_window, text='Time Span')
time_span_label.grid(row=1, column=0)

time_span_option_str = tk.StringVar()
time_span_option_menu = tk.OptionMenu(plot_window, time_span_option_str, '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
time_span_option_menu.grid(row=1, column=1)
time_span_option_str.set('1y')

def plot():
    ticker = ticker_entry.get()
    time_span = time_span_option_str.get()
    data = yf.Ticker(ticker).history(period=time_span)
    fig = Figure(figsize=(4, 4))
    ax = fig.add_subplot(111)
    ax.plot(data['Close'])
    ax.set_title(ticker + ' Spot Price')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.draw()
    # add the plot to the window without changing the layout and center the plot
    canvas.get_tk_widget().grid(row=3, column=0, columnspan=3)


plot_button = tk.Button(plot_window, text='Plot', command=plot)
plot_button.grid(row=2, column=1)

# adapt window size to the number of widgets
plot_window.grid_rowconfigure(2, minsize=50)
plot_window.grid_columnconfigure(2, minsize=50)

plot()

# move the plot window below the implied volatility window
plot_window.geometry('+%d+%d' % (50, 50 + 1.3*root.winfo_height()))

# make window not resizable
#plot_window.resizable(False, False)

# start the GUI

root.mainloop()