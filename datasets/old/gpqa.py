import os
import pandas as pd
from datasets import load_dataset

# Load dataset with a specific config (e.g., 'gpqa_main')
dataset = load_dataset('Idavidrein/gpqa', 'gpqa_diamond', split='train')

# Convert to DataFrame
df = pd.DataFrame(dataset)

# Randomly sample 50 entries
sample_df = df.sample(n=50, random_state=42)

# Select relevant columns and rename them (if they exist in the dataset)
columns_to_keep = ['Question', 'Correct Answer', 'Explanation']
sample_df = sample_df[columns_to_keep].rename(columns={'Correct Answer': 'Answer'})

# Save to CSV
sample_df.to_csv('gpqa_sample.csv', index=False)

print("Saved 50 random samples to gpqa_sample.csv")



