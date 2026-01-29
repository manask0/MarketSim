import numpy as np
import matplotlib.pyplot as plt

S0 = 100.0      # initial price
mu = 0.1        # drift / expected annual growth
sigma = 0.2     # volatility
T = 1.0         # time horizon (1 year)
dt = 1/252      # daily steps
n_paths = 10

N = int(T / dt)  # number of time steps
time = np.linspace(0, T, N+1) # Creates numpy array of N+1 entries with gap (T-0)/(N+1-1) = T/N. {0, T/N, 2T/N..... T}

S = np.zeros((n_paths, N+1)) # 2d array filled with zeros, n_paths rows and N+1 columns.
S[:, 0] = S0 #0th column of all rows (initial price of all paths) is set to S0.
for t in range(1, N+1):
    Z = np.random.normal(0, 1, n_paths) #Numpy array of normal distribution having mean 0, std dev 1, and n_paths members
    S[:, t] = S[:, t-1] * np.exp(
        (mu - 0.5 * sigma**2) * dt
        + sigma * np.sqrt(dt) * Z
    )


plt.figure(figsize=(10, 5))
for i in range(n_paths):
    plt.plot(time, S[i])

plt.xlabel("Time (years)")
plt.ylabel("Stock Price")
plt.title("GBM Simulated Price Paths")
plt.grid(True)

plt.savefig('../assets/price_paths.png', dpi=300)


plt.figure(figsize=(7, 5))
plt.hist(S[:, -1], bins=10, edgecolor='black')
plt.xlabel("Final Price $S_T$")
plt.ylabel("Frequency")
plt.title("Histogram of Final Prices")
plt.grid(True)
plt.savefig('../assets/final_prices.png', dpi=300)

