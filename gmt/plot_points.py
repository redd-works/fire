import pandas as pd
import matplotlib.pyplot as plt

files = ['cl_end_points.csv',
         'cl_non_repeating.csv',
         'cl_start_points.csv',
         'outline.csv']
for file in files:
    df = pd.read_csv(file)
    print(df)
    x = list(df['x'])
    y = list(df['y'])

    plt.plot(x, y, 'o')
    plt.show()
