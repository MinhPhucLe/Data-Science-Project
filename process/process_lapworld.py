import pandas as pd

df = pd.read_csv('Dai/laptopworld_gamming.csv')

df.insert(df.columns.get_loc('price') + 1, 'old', 0)
df.insert(df.columns.get_loc('old') + 1, 'new', 1)

# Save the updated DataFrame back to the CSV file
df.to_csv('Dai/laptopworld_gamming.csv', index=False)



df = pd.read_csv('Dai/laptopworld_vanphong.csv')

df.insert(df.columns.get_loc('price') + 1, 'old', 0)
df.insert(df.columns.get_loc('old') + 1, 'new', 1)

df.to_csv('Dai/laptopworld_vanphong.csv', index=False)