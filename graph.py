# File to graph telemetry data using matplotlib

import matplotlib.pyplot as plt
import pandas as pd

# Set which column of data to graph -- currently only one variable at a time
# is supported
colToGraph = 'lastY'

# Open the file, grab the column, close the file
file = open('log.txt')
df = pd.read_csv(file, sep='\s+', usecols=[colToGraph])
file.close()

# Convert the column to a list, and plug it into matplotlib
plt.plot(df[colToGraph].tolist())
plt.ylabel(colToGraph)
plt.show()
