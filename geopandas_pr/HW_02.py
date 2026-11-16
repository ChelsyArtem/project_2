import pandas as pd
import matplotlib.pyplot as plt

N = 4
k = str(2025 - N)

df = pd.read_excel("final_dataset.xlsx")
df = df[(df['2025 profit'] > 0) & (df[f'{k} profit'] > 0)]

df['rost, %'] = (((df['2025 profit'] - df[f'{k} profit']) / df[f'{k} profit']) * 100).round().astype(int)
counts = df['rost, %'].value_counts()
values = counts[counts > 2].index
df = df[df['rost, %'].isin(values)]

counter = df['rost, %'].value_counts().sort_index()

counter.plot(kind='bar', figsize=(15, 6))
plt.show()