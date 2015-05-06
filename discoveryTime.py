import csv
import pandas as pd
import numpy as np
import scipy
import matplotlib
import seaborn
import pprint
import sys

data = pd.DataFrame.from_csv('fullDataClean.csv', index_col=0, parse_dates=['Boot_Date', 'Discovery_Date'])

deltas = []
deltaSeconds = []
deltaMilliseconds = []

prevTime = None
prevTrial = None
prevPos = None
for index, row in data.iterrows():
	if (index == 0) | (prevTrial != row.Trial_ID) | (prevPos != row.Position):
		prevTime = row.Discovery_Date
		prevTrial = row.Trial_ID
		prevPos = row.Position

		deltas.append(None)
		deltaSeconds.append(None)
		deltaMilliseconds.append(None)

	else:
		discTime = row.Discovery_Date - prevTime
		discSeconds = discTime.seconds
		discMilliseconds = discTime.milliseconds

		discMilliseconds += discSeconds * 1000

		deltas.append(discTime)
		deltaSeconds.append(discSeconds)
		deltaMilliseconds.append(discMilliseconds)

		prevTime = row.Discovery_Date
		prevTrial = row.Trial_ID
		prevPos = row.Position

for index, delta in enumerate(deltas):
	if delta is None:
		deltas[index] = deltas[index + 1]

for index, delta in enumerate(deltaSeconds):
	if delta is None:
		deltaSeconds[index] = deltaSeconds[index + 1]

for index, delta in enumerate(deltaMilliseconds):
	if delta is None:
		deltaMilliseconds[index] = deltaMilliseconds[index + 1]

data['Discovery_Milliseconds'] = pd.Series(deltaMilliseconds, index=data.index)

toDrop = ['Experiment_ID', 'Manufacturer', 'Model_Number', 'Serial_Number', 'Local_Bluetooth_Address', 'Local_UUID', 'Scan_Start_Time', 'Scan_Actual_End_Time', 'Scan_Length',
          'Remote_Bluetooth_Address', 'Scan_Mode',
          'Device_Name', 'Timestamp_Nanos', 'Boot_Timestamp_MS', 'Boot_Date', 'Discovery_Date', 'Batt_Discovery_Charge_Counter', 'Batt_Discovery_Current_Now', 'Batt_Discovery_Current_Average',
          'Batt_Discovery_Current_Capacity', 'Batt_Start_Charge_Counter', 'Batt_Start_Current_Now', 'Batt_Start_Current_Average', 'Batt_Start_Current_Capacity', 'Batt_End_Charge_Counter',
          'Batt_End_Current_Now', 'Batt_End_Current_Average', 'Batt_End_Current_Capacity', 'Tx_Power_Level']

data.drop(toDrop, axis=1, inplace=True)

listenerLatency = []
advertiserLatency = []
advertiserPower = []

for index, row in data.iterrows():
	if row['Trial_ID'] == 1:
		listenerLatency.append('Balanced')
		advertiserLatency.append('Balanced')
		advertiserPower.append('High')
	elif row['Trial_ID'] == 2:
		listenerLatency.append('Balanced')
		advertiserLatency.append('Balanced')
		advertiserPower.append('Medium')
	elif row['Trial_ID'] == 3:
		listenerLatency.append('Balanced')
		advertiserLatency.append('Balanced')
		advertiserPower.append('Low')
	elif row['Trial_ID'] == 4:
		listenerLatency.append('Balanced')
		advertiserLatency.append('Balanced')
		advertiserPower.append('Ultra_Low')
	elif row['Trial_ID'] == 5:
		listenerLatency.append('Balanced')
		advertiserLatency.append('Low_Latency')
		advertiserPower.append('High')
	elif row['Trial_ID'] == 6:
		listenerLatency.append('Balanced')
		advertiserLatency.append('Low_Latency')
		advertiserPower.append('Medium')
	elif row['Trial_ID'] == 7:
		listenerLatency.append('Balanced')
		advertiserLatency.append('Low_Latency')
		advertiserPower.append('Low')
	elif row['Trial_ID'] == 8:
		listenerLatency.append('Balanced')
		advertiserLatency.append('Low_Latency')
		advertiserPower.append('Ultra_Low')
	elif row['Trial_ID'] == 9:
		listenerLatency.append('Balanced')
		advertiserLatency.append('Low_Power')
		advertiserPower.append('High')
	elif row['Trial_ID'] == 10:
		listenerLatency.append('Balanced')
		advertiserLatency.append('Low_Power')
		advertiserPower.append('Medium')
	elif row['Trial_ID'] == 11:
		listenerLatency.append('Balanced')
		advertiserLatency.append('Low_Power')
		advertiserPower.append('Low')
	elif row['Trial_ID'] == 12:
		listenerLatency.append('Balanced')
		advertiserLatency.append('Low_Power')
		advertiserPower.append('Ultra_Low')
	elif row['Trial_ID'] == 13:
		listenerLatency.append('Low_Latency')
		advertiserLatency.append('Balanced')
		advertiserPower.append('High')
	elif row['Trial_ID'] == 14:
		listenerLatency.append('Low_Latency')
		advertiserLatency.append('Balanced')
		advertiserPower.append('Medium')
	elif row['Trial_ID'] == 15:
		listenerLatency.append('Low_Latency')
		advertiserLatency.append('Balanced')
		advertiserPower.append('Low')
	elif row['Trial_ID'] == 16:
		listenerLatency.append('Low_Latency')
		advertiserLatency.append('Balanced')
		advertiserPower.append('Ultra_Low')
	elif row['Trial_ID'] == 17:
		listenerLatency.append('Low_Latency')
		advertiserLatency.append('Low_Latency')
		advertiserPower.append('High')
	elif row['Trial_ID'] == 18:
		listenerLatency.append('Low_Latency')
		advertiserLatency.append('Low_Latency')
		advertiserPower.append('Medium')
	elif row['Trial_ID'] == 19:
		listenerLatency.append('Low_Latency')
		advertiserLatency.append('Low_Latency')
		advertiserPower.append('Low')
	elif row['Trial_ID'] == 20:
		listenerLatency.append('Low_Latency')
		advertiserLatency.append('Low_Latency')
		advertiserPower.append('Ultra_Low')
	elif row['Trial_ID'] == 21:
		listenerLatency.append('Low_Latency')
		advertiserLatency.append('Low_Power')
		advertiserPower.append('High')
	elif row['Trial_ID'] == 22:
		listenerLatency.append('Low_Latency')
		advertiserLatency.append('Low_Power')
		advertiserPower.append('Medium')
	elif row['Trial_ID'] == 23:
		listenerLatency.append('Low_Latency')
		advertiserLatency.append('Low_Power')
		advertiserPower.append('Low')
	elif row['Trial_ID'] == 24:
		listenerLatency.append('Low_Latency')
		advertiserLatency.append('Low_Power')
		advertiserPower.append('Ultra_Low')
	elif row['Trial_ID'] == 25:
		listenerLatency.append('Low_Power')
		advertiserLatency.append('Balanced')
		advertiserPower.append('High')
	elif row['Trial_ID'] == 26:
		listenerLatency.append('Low_Power')
		advertiserLatency.append('Balanced')
		advertiserPower.append('Medium')
	elif row['Trial_ID'] == 27:
		listenerLatency.append('Low_Power')
		advertiserLatency.append('Balanced')
		advertiserPower.append('Low')
	elif row['Trial_ID'] == 28:
		listenerLatency.append('Low_Power')
		advertiserLatency.append('Balanced')
		advertiserPower.append('Ultra_Low')
	elif row['Trial_ID'] == 29:
		listenerLatency.append('Low_Power')
		advertiserLatency.append('Low_Latency')
		advertiserPower.append('High')
	elif row['Trial_ID'] == 30:
		listenerLatency.append('Low_Power')
		advertiserLatency.append('Low_Latency')
		advertiserPower.append('Medium')
	elif row['Trial_ID'] == 31:
		listenerLatency.append('Low_Power')
		advertiserLatency.append('Low_Latency')
		advertiserPower.append('Low')
	elif row['Trial_ID'] == 32:
		listenerLatency.append('Low_Power')
		advertiserLatency.append('Low_Latency')
		advertiserPower.append('Ultra_Low')
	elif row['Trial_ID'] == 33:
		listenerLatency.append('Low_Power')
		advertiserLatency.append('Low_Power')
		advertiserPower.append('High')
	elif row['Trial_ID'] == 34:
		listenerLatency.append('Low_Power')
		advertiserLatency.append('Low_Power')
		advertiserPower.append('Medium')
	elif row['Trial_ID'] == 35:
		listenerLatency.append('Low_Power')
		advertiserLatency.append('Low_Power')
		advertiserPower.append('Low')
	elif row['Trial_ID'] == 36:
		listenerLatency.append('Low_Power')
		advertiserLatency.append('Low_Power')
		advertiserPower.append('Ultra_Low')
	else:
		sys.exit("Encountered an unexpected Trial_ID")


data['Listener_Latency'] = pd.Series(listenerLatency, index=data.index)
data['Advertiser_Latency'] = pd.Series(advertiserLatency, index=data.index)
data['Advertiser_Power'] = pd.Series(advertiserPower, index=data.index)

data.to_csv('listenerData_Clean.csv')

# for trial in trialNumbers:
# 	trialData = data.query('Trial_ID == @trial')
# 	dataByTrial.append(trialData)
#
#
# for df in dataByTrial:
# 	for pos in position:
# 		posData = df.query('scan_record == @pos')
# 		if len(posData.index) != 0:
# 			dataByTrialByPos.append(posData)

# i = 0
# for df in dataByTrialByPos:
# 	print "Iteration number: ", i
# 	lastTime = None
# 	timeDelta = None
# 	deltas = []
# 	if i == 12:
# 		print df
# 		sys.exit("Hit iteration 12")
# 	for index, row in df.iterrows():
# 		if lastTime is None:
# 			lastTime = row.Discovery_Date
# 		else:
# 			timeDelta = row.Discovery_Date - lastTime
# 			lastTime = row.Discovery_Date
# 			deltas.append(timeDelta)
# 	averageTime = reduce(lambda x, y: x + y, deltas) / len(deltas)
# 	deltas.insert(0, averageTime)
# 	discoveryTimes = pd.Series(deltas)
# 	df['discoveryTime'] = discoveryTimes
# 	i += 1
# 	print deltas

# Iterate through the primary DF and compute a timeDelta for each row

# deltas = []
# lastTrial = None
# lastTime = None
# for index, row in data.iterrows():
# 	if (index == 0) | (lastTime != row.Discovery_Date):
# 		discoveryDelta = None
# 		lastTrial = row.Trial_ID
# 		lastTime = row.Discovery_Date
# 		deltas.append(discoveryDelta)
# 	else:
# 		discoveryDelta = row.Discovery_Date - lastTime
# 		lastTrial = row.Trial_ID
# 		lastTime = row.Discovery_Date
# 		deltas.append(discoveryDelta)
#
# seriesDelta = pd.Series(deltas, name='Deltas')
# data.append(seriesDelta)
# print data

# Add calculated discovery time column to dataframe



# arrayDeltas = np.asarray(discoveryDelta)
# trial['discoveryDeltas'] = arrayDeltas

