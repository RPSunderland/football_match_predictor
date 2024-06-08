import pandas as pd
import glob
import os

# Wstępny preprocessing danych
data_folder = 'Datasets/seasons'

# Lączenie danych z sezonów
all_files = glob.glob(os.path.join(data_folder, "*.csv"))
df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)

# Usuwanie niepotrzebnych kolumn
end_index = df.columns.get_loc('B365H')
df = df.iloc[:, :end_index]
df.to_csv("Datasets/matches.csv", index=False)

# Usuwanie niepotrzebnych sezonów
df = pd.read_csv("Datasets/standings.csv")
df = df[(df['Season_End_Year'] >= 1999) & (df['Season_End_Year'] <= 2021)]
df.to_csv("Datasets/standings.csv", index=False)