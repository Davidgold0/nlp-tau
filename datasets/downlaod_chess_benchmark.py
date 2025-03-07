import pandas as pd
import random

# Load the CSV file
file_path = "/mnt/data/puzzles.csv"
df = pd.read_csv(file_path)

# Extract required columns
df_formatted = pd.DataFrame()
df_formatted["problem"] = df["puzzle"]
df_formatted["Solution"] = df["moves"]
df_formatted["Answer"] = df["moves"].apply(lambda x: x.split()[0] if isinstance(x, str) else "")

# Select 50 random rows
df_formatted = df_formatted.sample(n=50, random_state=42).reset_index(drop=True)

# Save the formatted file
output_path = "/mnt/data/formatted_puzzles.csv"
df_formatted.to_csv(output_path, index=False)

# Provide the file to the user
output_path
