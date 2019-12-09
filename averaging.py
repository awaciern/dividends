# Importing libraries
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join

# Get all big dataset files
path = 'Data/Big'
big_files = [f for f in listdir(path) if isfile(join(path, f))]

# Loop through all big datasets
for f in big_files:
    # Read in the dataset
    data_big = pd.read_csv('Data/Big/{0}'.format(f))

    # Calculate average difference in stock values over 3 day period
    data_big['Delta_3'] = [float(0) for day in range(0, len(data_big))]
    for day in range(0, len(data_big)):
        if day >= 3 and day < len(data_big)-3:
            data_big['Delta_3'][day] = np.average(data_big['Delta'][day:day+3]) - np.average(data_big['Delta'][day-3:day])

    # Calculate average difference in stock values over 5 day period
    data_big['Delta_5'] = [float(0) for day in range(0, len(data_big))]
    for day in range(0, len(data_big)):
        if day >= 5 and day < len(data_big)-5:
            data_big['Delta_5'][day] = np.average(data_big['Delta'][day:day+5]) - np.average(data_big['Delta'][day-5:day])

    # Calculate average difference in stock values over 10 day period
    data_big['Delta_10'] = [float(0) for day in range(0, len(data_big))]
    for day in range(0, len(data_big)):
        if day >= 10 and day < len(data_big)-10:
            data_big['Delta_10'][day] = np.average(data_big['Delta'][day:day+10]) - np.average(data_big['Delta'][day-10:day])

    # Calculate average difference in stock values over 25 day period
    data_big['Delta_25'] = [float(0) for day in range(0, len(data_big))]
    for day in range(0, len(data_big)):
        if day >= 25 and day < len(data_big)-25:
            data_big['Delta_25'][day] = np.average(data_big['Delta'][day:day+25]) - np.average(data_big['Delta'][day-25:day])

    # Print and save each new big dataset with average differences
    print(data_big)
    data_big.to_csv('Data/Averaging/Big/{0}'.format(f))
