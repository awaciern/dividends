# Importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler

# Get data from big dataset
data_DUK = pd.read_csv('Data/Big/DUK.csv')
data_DUK['Date'] = pd.to_datetime(data_DUK.Date,format='%Y-%m-%d')
data_DUK.index = data_DUK['Date']
data_DUK = data_DUK.sort_index(ascending=True, axis=0)

# Allocate new dataset for use in creating models
data_DUK_dates = pd.DataFrame(index=range(0, len(data_DUK)),
                              columns=['Date', 'Close', 'Seq',
                                       'Div_Eff', 'Div_Eff_Val', 'Div_Eff_Delta',
                                       'Div_Dec', 'Div_Dec_Num', 'Div_Dec_Val', 'Div_Dec_Delta',
                                       'Div_Rec', 'Div_Rec_Val', 'Div_Rec_Delta',
                                       'Div_Pay', 'Div_Pay_Val', 'Div_Pay_Delta'])

# Copy info from big dataset to new dataset
seq = 0
for day in range (0, len(data_DUK)):
    data_DUK_dates['Seq'][day] = seq
    seq += 1
    for col in data_DUK_dates:
        try:
            data_DUK_dates[col][day] = data_DUK[col][day]
        except KeyError:
            pass

# Divide new dataset into training and validation (all 2019 dates) data
train = data_DUK_dates[0:1258]
valid = data_DUK_dates[1258:]

# Function to perform linear regression for specified input features
def linreg(x_features, title):
    # Seperate input and output features
    x_train = train[x_features]
    y_train = train['Close']
    x_valid = valid[x_features]
    y_valid = valid['Close']

    # Run linear regression
    model = LinearRegression()
    model.fit(x_train, y_train)

    # Make predictions from model and find mean square error
    preds = model.predict(x_valid)
    mse = np.mean(np.power((np.array(y_valid)-np.array(preds)),2))

    # Plot the predictions
    valid['Predictions'] = 0
    valid['Predictions'] = preds
    valid.index = data_DUK_dates[1258:].index
    train.index = data_DUK_dates[:1258].index
    plt.plot_date(train['Date'], train['Close'], fmt='-')
    plt.plot_date(valid['Date'], valid[['Close', 'Predictions']],  fmt='-')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Stock Value')
    plt.show()

    return mse

# Perform linear regression for a variety of dividend input features
title = '(DUK) Linear Regression Using Only Date Sequence'
print('{0} MSE = {1}'.format(title, linreg(['Seq'], title)))
title = '(DUK) Linear Regression Using Date Sequence & Effective Date Dividend Fields'
print('{0} MSE = {1}'.format(title, linreg(['Seq', 'Div_Eff', 'Div_Eff_Val', 'Div_Eff_Delta'], title)))
title = '(DUK) Linear Regression Using Date Sequence & Declaration Date Dividend Fields'
print('{0} MSE = {1}'.format(title, linreg(['Seq','Div_Dec', 'Div_Dec_Num', 'Div_Dec_Val', 'Div_Dec_Delta'], title)))
title = '(DUK) Linear Regression Using Date Sequence & Record Date Dividend Fields'
print('{0} MSE = {1}'.format(title, linreg(['Seq', 'Div_Rec', 'Div_Rec_Val', 'Div_Rec_Delta'], title)))
title = '(DUK) Linear Regression Using Date Sequence & Payment Date Dividend Fields'
print('{0} MSE = {1}'.format(title, linreg(['Seq', 'Div_Pay', 'Div_Pay_Val', 'Div_Pay_Delta'], title)))
title = '(DUK) Linear Regression Using Date Sequence & Declaration, Effective Date Dividend Fields'
print('{0} MSE = {1}'.format(title, linreg(['Seq', 'Div_Pay', 'Div_Pay_Val', 'Div_Pay_Delta',
                                            'Div_Dec', 'Div_Dec_Num', 'Div_Dec_Val', 'Div_Dec_Delta'], title)))
title = 'Linear Regression Using Date Sequence & Declaration, Effective, Payment Date Dividend Fields'
print('{0} MSE = {1}'.format(title, linreg(['Seq', 'Div_Pay', 'Div_Pay_Val', 'Div_Pay_Delta',
                                            'Div_Dec', 'Div_Dec_Num', 'Div_Dec_Val', 'Div_Dec_Delta',
                                            'Div_Pay', 'Div_Pay_Val', 'Div_Pay_Delta'], title)))
title = '(DUK) Linear Regression Using Date Sequence & Declaration, Effective, Record, Payment Date Dividend Fields'
print('{0} MSE = {1}'.format(title, linreg(['Seq', 'Div_Pay', 'Div_Pay_Val', 'Div_Pay_Delta',
                                            'Div_Dec', 'Div_Dec_Num', 'Div_Dec_Val', 'Div_Dec_Delta',
                                            'Div_Rec', 'Div_Rec_Val', 'Div_Rec_Delta',
                                            'Div_Pay', 'Div_Pay_Val', 'Div_Pay_Delta'], title)))


# LTSM
# data_DUK_dates.index = data_DUK_dates.Date
# data_DUK_dates.drop('Date', axis=1, inplace=True)
#
# data_features = data_DUK_dates.values
# # print(data_features)
#
# train = data_features[231:,:]
# valid = data_features[0:231,:]
# print(train[0])
# print(valid[len(valid)-1])
#
# scaler = MinMaxScaler(feature_range=(0, 1))
# scaled_data = scaler.fit_transform(data_features)
# # print(scaled_data)
#
# x_train, y_train = [], []
# for i in range()
