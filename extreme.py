# Importing libraries
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt

# Get all big dataset with averages files
path = 'Data/Averaging/Big'
big_files = [f for f in listdir(path) if isfile(join(path, f))]

# Allocate datasets for extreme values for all dividend categories
data_xtr_eff = pd.DataFrame(columns=['Company', 'Date', 'Close', 'Delta', 'Delta_3', 'Delta_5', 'Delta_10', 'Delta_25', 'Div_Eff_Val', 'Div_Eff_Delta'])
data_xtr_dec = pd.DataFrame(columns=['Company', 'Date', 'Close', 'Delta', 'Delta_3', 'Delta_5', 'Delta_10', 'Delta_25', 'Div_Dec_Num', 'Div_Dec_Val', 'Div_Dec_Delta'])
data_xtr_rec = pd.DataFrame(columns=['Company', 'Date', 'Close', 'Delta', 'Delta_3', 'Delta_5', 'Delta_10', 'Delta_25', 'Div_Rec_Val', 'Div_Rec_Delta'])
data_xtr_pay = pd.DataFrame(columns=['Company', 'Date', 'Close', 'Delta', 'Delta_3', 'Delta_5', 'Delta_10', 'Delta_25', 'Div_Pay_Val', 'Div_Pay_Delta'])

# Loop through all big datasets
for f in big_files:
    # Read in the dataset
    data_big = pd.read_csv('Data/Averaging/Big/{0}'.format(f))

    # Record effective dividend dates with a change of at least $0.15
    for day in range(0, len(data_big)):
        if abs(data_big['Div_Eff_Delta'][day]) >= 0.15:
            xtr_eff = data_big.loc[data_big.index == day][['Date', 'Close', 'Delta', 'Delta_3', 'Delta_5', 'Delta_10', 'Delta_25', 'Div_Eff_Val', 'Div_Eff_Delta']]
            xtr_eff['Company'] = f.strip('.csv')
            data_xtr_eff = data_xtr_eff.append(xtr_eff, ignore_index=True)

    # Record declared dividend dates with a change of at least $0.15
    for day in range(0, len(data_big)):
        if abs(data_big['Div_Dec_Delta'][day]) >= 0.15:
            xtr_dec = data_big.loc[data_big.index == day][['Date', 'Close', 'Delta', 'Delta_3', 'Delta_5', 'Delta_10', 'Delta_25', 'Div_Dec_Num', 'Div_Dec_Val', 'Div_Dec_Delta']]
            xtr_dec['Company'] = f.strip('.csv')
            data_xtr_dec = data_xtr_dec.append(xtr_dec, ignore_index=True)

    # Record recorded dividend dates with a change of at least $0.15
    for day in range(0, len(data_big)):
        if abs(data_big['Div_Rec_Delta'][day]) >= 0.15:
            xtr_rec = data_big.loc[data_big.index == day][['Date', 'Close', 'Delta', 'Delta_3', 'Delta_5', 'Delta_10', 'Delta_25', 'Div_Rec_Val', 'Div_Rec_Delta']]
            xtr_rec['Company'] = f.strip('.csv')
            data_xtr_rec = data_xtr_rec.append(xtr_rec, ignore_index=True)

    # Record paid dividend dates with a change of at least $0.15
    for day in range(0, len(data_big)):
        if abs(data_big['Div_Pay_Delta'][day]) >= 0.15:
            xtr_pay = data_big.loc[data_big.index == day][['Date', 'Close', 'Delta', 'Delta_3', 'Delta_5', 'Delta_10', 'Delta_25', 'Div_Pay_Val', 'Div_Pay_Delta']]
            xtr_pay['Company'] = f.strip('.csv')
            data_xtr_pay = data_xtr_pay.append(xtr_pay, ignore_index=True)

# Print and save datasets
print(data_xtr_eff)
data_xtr_eff.to_csv('Data/Extreme/Eff.csv')
print(data_xtr_dec)
data_xtr_dec.to_csv('Data/Extreme/Dec.csv')
print(data_xtr_rec)
data_xtr_rec.to_csv('Data/Extreme/Rec.csv')
print(data_xtr_pay)
data_xtr_pay.to_csv('Data/Extreme/Pay.csv')
