import pandas as pd
import numpy as np
from scipy import stats
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import glob

'''File Processing Flow Methods'''

# Aggregate the trials across the different experiments into one dataframe each.
def aggregateTrials(tables):
    trialsList = {}
    experiments = {}
    
    # Apparently its better to create the list of trials and then concat them all in one go, hence the two for loops.
    # for frame in tables:
        # if str(tables[frame].iat[0, 0]) not in trialsList:
            # trialsList[str(tables[frame].iat[0, 0])] = [tables[frame][3:]]
        # else:
            # trialsList[str(tables[frame].iat[0, 0])].append(tables[frame][3:])
    
    listener = []
    advertiser = []
    
    for frame in tables:
        listener.append(tables[frame][:3])
        advertiser.append(tables[frame][3:])
        
    
    trialsList['Listener'] = listener
    trialsList['Advertiser'] = advertiser
        

    print trialsList
    for experiment in trialsList:
        experiments[experiment] = pd.concat(trialsList[experiment], ignore_index=True)
    
    # experiments['Experiment 1'].to_csv('Raw_Data.csv', index=False)
    # experiments['Experiment 2'].to_csv('Raw_Data2.csv', index=False)
    experiments['Listener'].to_csv('Raw_Data_Listener.csv', index=False)
    experiments['Advertiser'].to_csv('Raw_Data_Advertiser.csv', index=False)
    
    return experiments

# Use this to work with the raw data after it has been imported. Comment out the method that pulls in a new file so that 
def importData(Experiment):
    if Experiment < 3:
        dataFrames = {}
        dataFrames['Experiment ' +str(Experiment)] = pd.read_csv('Raw_Data' +str(Experiment) + '.csv')
    else:
        dataFrames = {}
        dataFrames['Listener'] = pd.read_csv('Raw_Data_Listener.csv', index=False)
        dataFrames['Advertiser'] = pd.read_csv('Raw_Data_Advertiser.csv', index=False)
        
    return dataFrames
        
def cleanData(dataFrames):
    for frame in dataFrames:
        dataFrames[frame].rename(columns={' scan_record_converted':'pos'}, inplace=True)
        dataFrames[frame]['pos'] = dataFrames[frame]['pos'].apply(lambda x: int(x[4:]) * 1.2)
    
    return dataFrames
    
# Run the analysies(?) on the csv files. No cross file comparisons yet- just describing each of the experiments and trials.
def dataAnalysis(dataFrames):
    percentCaptureResults = analyzePercentCapture(dataFrames['Experiment 2'])
    countResults = analyzeCount(dataFrames['Experiment 2'])
    rssiResults = analyzeRSSI(dataFrames['Experiment 2'])
    discoveryResults = analyzeInitialDiscovery(dataFrames['Experiment 2'])
    
    # print percentCaptureResults
    print countResults
    # print rssiResults
    # print discoveryResults
    
    
    captureStats = pd.concat([countResults, rssiResults, discoveryResults], axis=1)
    captureStats.columns = ['Percent_Captures', 'Capture_Count', 'RSSI', 'Time_to_Discovery']
    return captureStats
    
    #Method to access online one trial of an experiment
    #print captureStats.xs(1, level=' Trial_ID')

def printToCSV(frame):
    frame.to_csv('Preliminary_Results.csv')
    flatFile = pd.read_csv('Preliminary_Results.csv')
    
    experimentRecord = pd.read_csv('Experiment Record.csv')
    experimentFactors = experimentRecord[['Trial', 'Listener Latency', 'Adv Latency', 'Adv Power']]
    
    dataWithFactors = flatFile.merge(experimentFactors, how='outer', left_on=' Trial_ID', right_on='Trial')
    
    dataWithFactors.to_csv('Prelim_Results2.csv')   
    
    return dataWithFactors

def plotStats(frame):
    # Actual plotting
    sns.set_style("ticks", {"xtick.minor.size":  12})
    sns.set_context('paper')
    
    frame.rename(columns={'Capture_Count': 'Discovery_Event_Count'}, inplace=True)
    
    factors = ['Adv Latency','Listener Latency', 'Adv Power', 'pos']
    variables = ['Time_to_Discovery', 'RSSI', 'Discovery_Event_Count', 'Percent_Captures']

    # for factor in factors:
        # for variable in variables:
            # sns.factorplot(factor, y=variable, data=frame.dropna())
            # plt.savefig( factor + ' vs. ' + variable + '.png', dpi=600, bbox_inches='tight')
            
    if True:
        sns.factorplot('Trial', y=variables[0], data=frame.dropna())
        plt.savefig('Trial' + ' vs. ' + variables[0] + '.png', dpi=600, bbox_inches='tight')
        for variable in variables:
            sns.factorplot(factors[2], variable, col=factors[0], row=factors[1], data=frame.dropna(), margin_titles=True, size=3, aspect=.8, x_order=['High','Medium','Low','Ultra_low'], col_order=['Low_Latency', 'Balanced', 'Low_Power'], row_order=['Low_Latency', 'Balanced', 'Low_Power'])
            plt.savefig('Trials' + ' vs. ' + variable + '.png', dpi=600, bbox_inches='tight')
    
    g = sns.factorplot(factors[3], variables[1], data=frame.dropna(), margin_titles=True, size=3, aspect=.8)
    g.set_xticklabels(rotation=90)
    plt.savefig(factors[3] + ' vs. ' + variables[1] + '.png', dpi=600, bbox_inches='tight')
    
        # for factor in factors:
            # sns.factorplot(factor, y=variables[0], data=frame.dropna())
            # plt.savefig(factor + ' vs. ' + variables[0] + '.png', dpi=600, bbox_inches='tight')
    
'''Preliminary Statistical Analysis Methods'''    
    
# Get the percent of capture events per position by trial and position    
def analyzePercentCapture (frame):
    frame[' percent_captures'] = 1
    
    trialByDevice = frame.groupby(' Trial_ID').apply(lambda x: x.groupby('pos').count()/x.count())
    
    return trialByDevice[' percent_captures']

# Get the number of capture events by trial and position
def analyzeCount(frame):
    trialByDevice = frame.groupby(' Trial_ID')
    captureSize = trialByDevice.apply(lambda x: x.groupby('pos').size())
    
    return captureSize

# Get the time of first discovery by trial and position    
def analyzeInitialDiscovery(frame):
    trialByDevice = frame.groupby(' Trial_ID')
    initialDiscovery = trialByDevice.apply(lambda x: x.groupby('pos').apply(findInitialDiscovery).abs())
    
    return initialDiscovery.astype('timedelta64[s]')

# Helper function to get time delta between Discovery_Date column and Scan_Start_Time
def findInitialDiscovery(group):
    try:
        firstDiscovery = pd.to_datetime(group[' Discovery_Date'].min()) + pd.DateOffset(hours=4)
        scanStart = pd.to_datetime(group[' Scan_Start_Time'].min(), unit='ms')

        return (firstDiscovery - scanStart)
    except:
        return None  
    
# Get the mean RSSI value by trial and position
def analyzeRSSI(frame):
    trialByDevice = frame.groupby(' Trial_ID')
    meanRSSITrial = trialByDevice.apply(lambda x: x.groupby('pos')[' rssi'].mean())
    
    return meanRSSITrial

    
'''IN PROGRESS METHODS'''    

def analyzeEnergyConsumption(frame):
    trialByDevice = frame.groupby(' Trial_ID')
    energyConsumption = trialByDevice.apply(lambda x: x.groupby('pos').apply(energyDifference))
    
    return energyConsumption
    
def energyDifference(group):
    return group[' bat_start_current_capacity'].max() - group[' bat_end_current_capacity'].min()

''' Pandas Settings '''    
 
# This makes pandas only display two digits after the decimal. 
def formatFloat(number):
    return "{:+.2f}".format(number)

    
'''MAIN METHOD'''
    
if __name__ == "__main__":
    pd.set_option('display.float_format', formatFloat)
    
    tables = {}
    for filename in glob.glob('Battery Test\**\BATTERY**'):
        tables[filename] = pd.read_csv(filename)
        
    # experiments = aggregateTrials(tables)
    experiments = importData(2)
    cleanedExperiments = cleanData(experiments)
    results = dataAnalysis(cleanedExperiments)
    factorizedResults = printToCSV(results)
    plotStats(factorizedResults)
    
    
'''LEGACY METHOD'''
'''JUST HERE FOR REFERENCE'''   

''' 
# Mostly just counting captures right now. Primarily using groupBy now to combine time periods.
def analyzeCaptures(frame):
    sns.set(style="white")
    frame[" Discovery_Date"] = pd.to_datetime(frame[" Discovery_Date"])
    if debug:
        print frame[" Discovery_Date"]
    
    # sns.distplot(frame[' Discovery_Date'], kde=False, fit=stats.norm);
        
    captures10sPeriod = frame.groupby([' Trial_ID', ' Serial_Number', pd.TimeGrouper(key=' Discovery_Date',freq='10s')])
    captures10sCount = captures10sPeriod.size()
    if debug:
        print captures10sCount
        print captures10sCount.describe()
    
    # g1 = sns.PairGrid(captures10sCount, diag_sharey=False)
    # g1.map_lower(sns.kdeplot, cmap="Blues_d")
    # g1.map_upper(plt.scatter)
    # g1.map_diag(sns.kdeplot, lw=3)
    
    captures5sPeriod = frame.groupby([' Trial_ID', ' Serial_Number', pd.TimeGrouper(key=' Discovery_Date',freq='5s')])
    captures5sCount = captures5sPeriod.size()
    if debug: 
        print captures5sCount
        print captures5sCount.describe()
    
    # g2 = sns.PairGrid(captures5sCount, diag_sharey=False)
    # g2.map_lower(sns.kdeplot, cmap="Blues_d")
    # g2.map_upper(plt.scatter)
    # g2.map_diag(sns.kdeplot, lw=3)

    # return dataframe(captures5sCount), dataframe(captures10sCount)
'''
    

