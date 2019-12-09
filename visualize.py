# importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

WMT_daily = pd.read_csv('Data/Values/daily_adjusted_WMT.csv')
print(WMT_daily)
WMT_daily['Date'] = pd.to_datetime(WMT_daily.timestamp, format='%m/%d/%Y')
WMT_daily.index = WMT_daily['Date']
WMT_daily = WMT_daily.sort_index(ascending=True, axis=0)

WMT_vals = pd.DataFrame(index=range(0,len(WMT_daily)), columns=['Date', 'Close'])

for i in range(0, len(WMT_daily)):
    WMT_vals['Date'][i] = WMT_daily['Date'][i]
    WMT_vals['Close'][i] = WMT_daily['close'][i]

print(WMT_vals)
plt.plot_date(WMT_vals['Date'], WMT_vals['Close'], fmt='-', xdate=True)
plt.xlabel('Date')
plt.ylabel('Stock Value')
plt.show()

WMT_dividends = pd.read_csv('Data/Dividends/WMT.csv')
print(WMT_dividends)

WMT_div_eff = WMT_dividends[['EX/EFF DATE', 'TYPE']]
print(WMT_div_eff)
