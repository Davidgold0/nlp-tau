import random
import pandas as pd
from datasets import load_dataset

# Load the dataset
math_dataset = load_dataset("nlile/hendrycks-MATH-benchmark")

# Select 50 random questions from the dataset
sample_questions = random.sample(list(math_dataset['train']), 50)

# Create a DataFrame with 3 columns: problem, solution, answer
df = pd.DataFrame(sample_questions, columns=["problem", "solution", "answer"])

# Save to a CSV file
df.to_csv("math_questions.csv", index=False)

print("File 'math_questions.csv' created successfully!")