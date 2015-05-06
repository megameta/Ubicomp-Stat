import csv
import pandas as pd
import numpy as np
import scipy
import matplotlib
import seaborn as sns
import pprint
import sys

df = pd.DataFrame.from_csv('listenerData_Clean.csv', index_col=0)

plot = sns.factorplot("Trial_ID", "Discovery_Milliseconds", "Position", data=df, kind="bar", palette=sns.color_palette("hls", 10), legend=True, legend_out=True)
plot.despine(left=True)
plot.set_ylabels("Discovery Time")
sns.plt.show()