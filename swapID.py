import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import glob

if __name__ == "__main__":
    swapTables = {}
    preSub = len('Experiment ')
    postSub = len('-Trial 1') + 1
    length = len('Experiment 1- Trial 11')
    for folder in glob.glob('**\\'):
        if len(folder) is length and folder[-1] is not 0:
            for file in glob.glob(folder + '**\SCAN**'):
                print file
                temp = pd.read_csv(file)
                if int(temp.iat[1, 1]) < 10:
                    #temp['Swap'] = temp['Experiment_ID']
                    #temp['Experiment_ID'] = temp[' Trial_ID']
                    #temp[' Trial_ID'] = temp['Swap']
                    #del temp['Swap']
                    
                    temp.to_csv(file, index = False)
            