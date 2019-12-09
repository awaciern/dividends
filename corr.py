# Importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join

# Get all big dataset files
path = 'Data/Big'
big_files = [f for f in listdir(path) if isfile(join(path, f))]

# Allocate data frames for all dividend categories
data_eff_big = pd.DataFrame(columns=['Date', 'Close', 'Delta', 'Div_Eff', 'Div_Eff_Type', 'Div_Eff_Val', 'Div_Eff_Delta'])
data_dec_big = pd.DataFrame(columns=['Date', 'Close', 'Delta', 'Div_Dec', 'Div_Dec_Num', 'Div_Dec_Type', 'Div_Dec_Val', 'Div_Dec_Delta'])
data_rec_big = pd.DataFrame(columns=['Date', 'Close', 'Delta', 'Div_Rec', 'Div_Rec_Type', 'Div_Rec_Val', 'Div_Rec_Delta'])
data_pay_big = pd.DataFrame(columns=['Date', 'Close', 'Delta', 'Div_Pay', 'Div_Pay_Type', 'Div_Pay_Val', 'Div_Pay_Delta'])

# Loop through all big datasets
for f in big_files:
    # Read in the dataset
    data_big = pd.read_csv('Data/Big/{0}'.format(f))

    # Effective data divideds
    data_eff = data_big.loc[data_big['Div_Eff'] == 1][['Date', 'Close', 'Delta', 'Div_Eff', 'Div_Eff_Type', 'Div_Eff_Val', 'Div_Eff_Delta']]
    data_eff_big = data_eff_big.append(data_eff, ignore_index=True)

    # Declared data divideds
    data_dec = data_big.loc[data_big['Div_Dec'] == 1][['Date', 'Close', 'Delta', 'Div_Dec', 'Div_Dec_Num', 'Div_Dec_Type', 'Div_Dec_Val', 'Div_Dec_Delta']]
    data_dec_big = data_dec_big.append(data_dec, ignore_index=True)

    # Recorded data divideds
    data_rec = data_big.loc[data_big['Div_Rec'] == 1][['Date', 'Close', 'Delta','Div_Rec', 'Div_Rec_Type', 'Div_Rec_Val', 'Div_Rec_Delta']]
    data_rec_big = data_rec_big.append(data_rec, ignore_index=True)

    # Payed data divideds
    data_pay = data_big.loc[data_big['Div_Pay'] == 1][['Date', 'Close', 'Delta','Div_Pay', 'Div_Pay_Type', 'Div_Pay_Val', 'Div_Pay_Delta']]
    data_pay_big = data_pay_big.append(data_pay, ignore_index=True)

# Print and save datasets
print(data_eff_big)
data_eff_big.to_csv('Data/Corr/Source/Eff.csv')
print(data_dec_big)
data_dec_big.to_csv('Data/Corr/Source/Dec.csv')
print(data_rec_big)
data_rec_big.to_csv('Data/Corr/Source/Rec.csv')
print(data_pay_big)
data_pay_big.to_csv('Data/Corr/Source/Pay.csv')

# Calculate correlation matrix, print it, save it, and show visual
# Effective date divideds
data_eff_corr = data_eff_big[['Close', 'Delta', 'Div_Eff_Val', 'Div_Eff_Delta']]
data_eff_corr['Date'] = data_eff_corr.index
eff_corr_vals = pd.DataFrame(np.corrcoef([data_eff_corr[col] for col in data_eff_corr]),
                                         columns=['Close', 'Delta', 'Div_Eff_Val', 'Div_Eff_Delta', 'Date'],
                                         index=['Close', 'Delta', 'Div_Eff_Val', 'Div_Eff_Delta', 'Date'])
print(eff_corr_vals)
eff_corr_vals.to_csv('Data/Corr/Results/Eff.csv')
plt.matshow(eff_corr_vals)
plt.xticks(range(len(data_eff_corr.columns)), data_eff_corr.columns)
plt.yticks(range(len(data_eff_corr.columns)), data_eff_corr.columns)
plt.colorbar()
plt.title('Effective Date Dividends Correlation Matix on All Stocks')
plt.show()

# Declared date divideds
data_dec_corr = data_dec_big[['Close', 'Delta', 'Div_Dec_Num', 'Div_Dec_Val', 'Div_Dec_Delta']]
data_dec_corr['Date'] = data_dec_corr.index
data_dec_corr['Div_Dec_Num'] = data_dec_corr['Div_Dec_Num'].astype(float)
dec_corr_vals = pd.DataFrame(np.corrcoef([data_dec_corr[col] for col in data_dec_corr]),
                                         columns=['Close', 'Delta', 'Div_Dec_Num', 'Div_Dec_Val', 'Div_Dec_Delta', 'Date'],
                                         index=['Close', 'Delta', 'Div_Dec_Num', 'Div_Dec_Val', 'Div_Dec_Delta', 'Date'])
print(dec_corr_vals)
dec_corr_vals.to_csv('Data/Corr/Results/Dec.csv')
plt.matshow(dec_corr_vals)
plt.xticks(range(len(data_dec_corr.columns)), data_dec_corr.columns)
plt.yticks(range(len(data_dec_corr.columns)), data_dec_corr.columns)
plt.colorbar()
plt.title('Declared Date Dividends Correlation Matix on All Stocks')
plt.show()

# Recorded date divideds
data_rec_corr = data_rec_big[['Close', 'Delta', 'Div_Rec_Val', 'Div_Rec_Delta']]
data_rec_corr['Date'] = data_rec_corr.index
rec_corr_vals = pd.DataFrame(np.corrcoef([data_rec_corr[col] for col in data_rec_corr]),
                                         columns=['Close', 'Delta', 'Div_Rec_Val', 'Div_Rec_Delta', 'Date'],
                                         index=['Close', 'Delta', 'Div_Rec_Val', 'Div_Rec_Delta', 'Date'])
print(rec_corr_vals)
rec_corr_vals.to_csv('Data/Corr/Results/Rec.csv')
plt.matshow(data_rec_corr.corr())
plt.xticks(range(len(data_rec_corr.columns)), data_rec_corr.columns)
plt.yticks(range(len(data_rec_corr.columns)), data_rec_corr.columns)
plt.colorbar()
plt.title('Recorded Date Dividends Correlation Matix on All Stocks')
plt.show()

# Payed date divideds
data_pay_corr = data_pay_big[['Close', 'Delta', 'Div_Pay_Val', 'Div_Pay_Delta']]
data_pay_corr['Date'] = data_pay_corr.index
pay_corr_vals = pd.DataFrame(np.corrcoef([data_pay_corr[col] for col in data_pay_corr]),
                                         columns=['Close', 'Delta', 'Div_Pay_Val', 'Div_Pay_Delta', 'Date'],
                                         index=['Close', 'Delta', 'Div_Pay_Val', 'Div_Pay_Delta', 'Date'])
print(pay_corr_vals)
pay_corr_vals.to_csv('Data/Corr/Results/Pay.csv')
plt.matshow(data_pay_corr.corr())
plt.xticks(range(len(data_pay_corr.columns)), data_pay_corr.columns)
plt.yticks(range(len(data_pay_corr.columns)), data_pay_corr.columns)
plt.colorbar()
plt.title('Payed Date Dividends Correlation Matix on All Stocks')
plt.show()
