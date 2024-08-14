import pandas as pd

df = pd.read_excel('data.xlsx')

df.to_csv('102218069-data.csv', index=False)