# Importing libraries
import sys
import pandas as pd
import matplotlib.pyplot as plt

# Data filenames
company = sys.argv[1]
filename_daily = 'Data/Values/daily_adjusted_{0}.csv'.format(company)
filename_div = 'Data/Dividends/Source/{0}.csv'.format(company)
filename_big = 'Data/Big/{0}.csv'.format(company)
filename_div_eff = 'Data/Dividends/Eff/{0}.csv'.format(company)
filename_div_dec = 'Data/Dividends/Dec/{0}.csv'.format(company)
filename_div_rec = 'Data/Dividends/Rec/{0}.csv'.format(company)
filename_div_pay = 'Data/Dividends/Pay/{0}.csv'.format(company)

# Read in datasets
data_daily = pd.read_csv(filename_daily)
data_div = pd.read_csv(filename_div)

# Mark dates in datasets
data_daily['Date'] = pd.to_datetime(data_daily.timestamp, format='%m/%d/%Y')
data_div['Eff_Date'] = pd.to_datetime(data_div['EX/EFF DATE'], format='%m/%d/%Y')
data_div['Dec_Date'] = pd.to_datetime(data_div['DECLARATION DATE'], format='%m/%d/%Y')
data_div['Rec_Date'] = pd.to_datetime(data_div['RECORD DATE'], format='%m/%d/%Y')
data_div['Pay_Date'] = pd.to_datetime(data_div['PAYMENT DATE'], format='%m/%d/%Y')

# String to float processing
data_div['Amount'] = data_div['CASH AMOUNT'].replace( '[\$,)]', '', regex=True ).astype(float)

# Only consider data from 2014 or later
data_daily = data_daily.loc[data_daily['Date'] > pd.to_datetime('2013-12-31')]
data_div = data_div.loc[data_div['Dec_Date'] > pd.to_datetime('2013-12-31')]

# Create final dataset with daily values and dividends data
data_big = pd.DataFrame(index=range(0, len(data_daily)),
                          columns=['Date', 'Close', 'Delta',
                                   'Div_Eff', 'Div_Eff_Type', 'Div_Eff_Val', 'Div_Eff_Delta',
                                   'Div_Dec', 'Div_Dec_Type', 'Div_Dec_Num', 'Div_Dec_Val', 'Div_Dec_Delta',
                                   'Div_Rec', 'Div_Rec_Type', 'Div_Rec_Val', 'Div_Rec_Delta',
                                   'Div_Pay', 'Div_Pay_Type', 'Div_Pay_Val', 'Div_Pay_Delta'])

# Put values in final dataset
prev_dec_day = None
for day in range(0, len(data_daily)):  # all dates in daily dataset past 2014
    # Basic daily closing stock values
    date = data_daily['Date'][day]
    data_big['Date'][day] = date
    data_big['Close'][day] = data_daily['close'][day]
    if day < len(data_daily)-1:
        data_big['Delta'][day] = data_daily['close'][day] - data_daily['close'][day+1]
    else:
        data_big['Delta'][day] = 0

    # Dividends effective date data

    eff_date_list = pd.to_datetime(data_div['Eff_Date'].values)
    if date in eff_date_list:
        data_big['Div_Eff'][day] = 1
        data_big['Div_Eff_Val'][day] = data_div['Amount'][eff_date_list.get_loc(date)]
        data_big['Div_Eff_Type'][day] = data_div['TYPE'][eff_date_list.get_loc(date)]
        if eff_date_list.get_loc(date) < len(eff_date_list)-1:
            data_big['Div_Eff_Delta'][day] = data_div['Amount'][eff_date_list.get_loc(date)] - data_div['Amount'][eff_date_list.get_loc(date)+1]
        else:
            data_big['Div_Eff_Delta'][day] = 0
    else:
        data_big['Div_Eff'][day] = 0
        data_big['Div_Eff_Val'][day] = 0
        data_big['Div_Eff_Type'][day] = 'None'
        data_big['Div_Eff_Delta'][day] = 0

    # Dividends declared date data (multiple dividends can be declared on the same day)
    dec_date_list = pd.to_datetime(data_div['Dec_Date'].values)
    if date in dec_date_list:
        data_big['Div_Dec'][day] = 1
        data_big['Div_Dec_Val'][day] = data_div['Amount'][dec_date_list.get_loc(date)]
        data_big['Div_Dec_Type'][day] = data_div['TYPE'][dec_date_list.get_loc(date)]
        # print(data_big['Div_Dec_Val'][day].values[0])
        # if prev_dec_day:
            # print('Prev = {0}'.format(data_big['Div_Dec_Val'][prev_dec_day]))
            # print('Delta = {0}'.format(data_big['Div_Dec_Val'][prev_dec_day] - data_big['Div_Dec_Val'][day].values[0]))
        try:
            data_big['Div_Dec_Num'][day] = len(data_big['Div_Dec_Val'][day])
            data_big['Div_Dec_Val'][day] = data_big['Div_Dec_Val'][day].values[0]
            data_big['Div_Dec_Type'][day] = data_big['Div_Dec_Type'][day].values[0]
            if dec_date_list.get_loc(date)[len(dec_date_list)-1]:
                data_big['Div_Dec_Delta'][day] = 0
        except:
            data_big['Div_Dec_Num'][day] = 1
            if dec_date_list.get_loc(date) == len(dec_date_list)-1:
                data_big['Div_Dec_Delta'][day] = 0
        if prev_dec_day:
            data_big['Div_Dec_Delta'][prev_dec_day] = data_big['Div_Dec_Val'][prev_dec_day] - data_big['Div_Dec_Val'][day]
        prev_dec_day = day
    else:
        data_big['Div_Dec'][day] = 0
        data_big['Div_Dec_Num'][day] = 0
        data_big['Div_Dec_Val'][day] = 0
        data_big['Div_Dec_Type'][day] = 'None'
        data_big['Div_Dec_Delta'][day] = 0

    # Dividends recorded date data
    rec_date_list = pd.to_datetime(data_div['Rec_Date'].values)
    if date in rec_date_list:
        data_big['Div_Rec'][day] = 1
        data_big['Div_Rec_Val'][day] = data_div['Amount'][rec_date_list.get_loc(date)]
        data_big['Div_Rec_Type'][day] = data_div['TYPE'][rec_date_list.get_loc(date)]
        if rec_date_list.get_loc(date) < len(rec_date_list)-1:
            data_big['Div_Rec_Delta'][day] = data_div['Amount'][rec_date_list.get_loc(date)] - data_div['Amount'][rec_date_list.get_loc(date)+1]
        else:
            data_big['Div_Rec_Delta'][day] = 0
    else:
        data_big['Div_Rec'][day] = 0
        data_big['Div_Rec_Val'][day] = 0
        data_big['Div_Rec_Type'][day] = 'None'
        data_big['Div_Rec_Delta'][day] = 0

    # Dividends payed date data
    pay_date_list = pd.to_datetime(data_div['Pay_Date'].values)
    if date in pay_date_list:
        data_big['Div_Pay'][day] = 1
        data_big['Div_Pay_Val'][day] = data_div['Amount'][pay_date_list.get_loc(date)]
        data_big['Div_Pay_Type'][day] = data_div['TYPE'][pay_date_list.get_loc(date)]
        if pay_date_list.get_loc(date) < len(pay_date_list)-1:
            data_big['Div_Pay_Delta'][day] = data_div['Amount'][pay_date_list.get_loc(date)] - data_div['Amount'][pay_date_list.get_loc(date)+1]
        else:
            data_big['Div_Pay_Delta'][day] = 0
    else:
        data_big['Div_Pay'][day] = 0
        data_big['Div_Pay_Val'][day] = 0
        data_big['Div_Pay_Type'][day] = 'None'
        data_big['Div_Pay_Delta'][day] = 0

# Write the big dataset to a csv file and print it
print('Overall Dataset:')
print(data_big)
data_big.to_csv(filename_big)

# Partition big dataset into smaller specific dividend datasets, printing and wtiting along the way
print('\nEffective Date Dividends:')
data_eff = data_big.loc[data_big['Div_Eff'] == 1][['Date', 'Close', 'Delta','Div_Eff', 'Div_Eff_Type', 'Div_Eff_Val', 'Div_Eff_Delta']]
print('{0} entries'.format(len(data_eff)))
print(data_eff)
data_eff.to_csv(filename_div_eff)

print('\nDeclared Date Dividends:')
data_dec = data_big.loc[data_big['Div_Dec'] == 1][['Date', 'Close', 'Delta', 'Div_Dec', 'Div_Dec_Num', 'Div_Dec_Type', 'Div_Dec_Val', 'Div_Dec_Delta']]
print('{0} entries'.format(len(data_dec)))
print(data_dec)
data_dec.to_csv(filename_div_dec)

print('\nRecorded Date Dividends:')
data_rec = data_big.loc[data_big['Div_Rec'] == 1][['Date', 'Close', 'Delta', 'Div_Rec', 'Div_Rec_Type', 'Div_Rec_Val', 'Div_Rec_Delta']]
print('{0} entries'.format(len(data_rec)))
print(data_rec)
data_rec.to_csv(filename_div_rec)

print('\nPayed Date Dividends:')
data_pay = data_big.loc[data_big['Div_Pay'] == 1][['Date', 'Close', 'Delta', 'Div_Pay', 'Div_Pay_Type', 'Div_Pay_Val', 'Div_Pay_Delta']]
print('{0} entries'.format(len(data_pay)))
print(data_pay)
data_pay.to_csv(filename_div_pay)

# Plot the closing price and mark dividends days
plt.plot_date(data_big['Date'], data_big['Close'], fmt='-', xdate=True)
eff_dates = data_big.loc[data_big['Div_Eff'] == 1]
plt.plot_date(eff_dates['Date'], eff_dates['Close'], fmt='ro', xdate=True)
dec_dates = data_big.loc[data_big['Div_Dec'] == 1]
plt.plot_date(dec_dates['Date'], dec_dates['Close'], fmt='y*', xdate=True)
rec_dates = data_big.loc[data_big['Div_Rec'] == 1]
plt.plot_date(rec_dates['Date'], rec_dates['Close'], fmt='mx', xdate=True)
pay_dates = data_big.loc[data_big['Div_Pay'] == 1]
plt.plot_date(pay_dates['Date'], pay_dates['Close'], fmt='g+', xdate=True)
plt.xlabel('Date')
plt.ylabel('Stock Value')
plt.legend(('Close', 'Effective Dividend Date', 'Declared Dividend', 'Recorded Dividend', 'Payed Dividend'))
plt.title('{0} Stock Price with Dividend Markers'.format(company))
plt.show()
