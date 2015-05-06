import csv
import pandas as pd
import numpy as np
import scipy
import matplotlib
import seaborn
import pprint
import sys

data = pd.DataFrame.from_csv('Raw_Data1.csv', index_col=False)
columns = ['Experiment_ID', 'Trial_ID', 'Manufacturer', 'Model_Number', 'Serial_Number', 'Local_Bluetooth_Address',
		   'Local_UUID', 'Scan_Start_Time', 'Scan_Actual_End_Time', 'Scan_Length', 'Position', 'Scan_Mode',
		   'Remote_Bluetooth_Address', 'Device_Name', 'Timestamp_Nanos', 'Boot_Timestamp_MS', 'Boot_Date',
		   'Discovery_Date', 'Batt_Discovery_Charge_Counter', 'Batt_Discovery_Current_Now',
		   'Batt_Discovery_Current_Average', 'Batt_Discovery_Current_Capacity',
		   'Tx_Power_Level', 'RSSI', 'Batt_Start_Charge_Counter', 'Batt_Start_Current_Now', 'Batt_Start_Current_Average',
		   'Batt_Start_Current_Capacity', 'Batt_End_Charge_Counter', 'Batt_End_Current_Now', 'Batt_End_Current_Average',
		   'Batt_End_Current_Capacity']

data.columns = columns

# Sort the total dataframe into separate dataframes by trial and store in an array

oldPosition = [' Pos1', ' Pos2', ' Pos3', ' Pos4', ' Pos5', ' Pos6', ' Pos7', ' Pos8', ' Pos9', ' Pos10']
newPosition = ['Pos1', 'Pos2', 'Pos3', 'Pos4', 'Pos5', 'Pos6', 'Pos7', 'Pos8', 'Pos9', 'Pos10']

data = data.replace(oldPosition, newPosition)

data.to_csv('fullDataClean.csv')

