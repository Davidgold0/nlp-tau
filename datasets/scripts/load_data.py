import pickle
import pandas as pd
import tiktoken  # For token counting

# Replace 'data.pkl' with your pickle file path
filename = 'translated_questions_dataset.pkl'
output_filename = 'data_modified.pkl'  # File to save modified DataFrame

try:
    with open(filename, 'rb') as file:
        df = pickle.load(file)
        print(df[df['question_type'] == "B"]['question_translation_latex'].iloc[0])
    if isinstance(df, pd.DataFrame):
        if 'question_translation_latex' in df.columns and 'question_type' in df.columns:
            # Initialize GPT-4o tokenizer
            enc = tiktoken.encoding_for_model("gpt-4o")

            # Filter out NaN values, exclude "na" strings, and select rows where question_type is 'A'
            valid_entries = df[
                df['question_translation_latex'].notna() &
                (df['question_translation_latex'].astype(str).str.lower() != 'na') &
                (df['question_type'] == 'B')
                ]['question_translation_latex']

            # Count total number of valid entries
            num_entries = len(valid_entries)

            # Count total tokens
            token_count = sum(len(enc.encode(str(value))) for value in valid_entries)

            print(f"Number of valid entries where question_type is 'B': {num_entries}")
            print(f"Total token count (GPT-4o): {token_count}")

            # Delete non-NaN and non-"na" entries with question_type 'A'
            df.loc[
                df['question_translation_latex'].isin(valid_entries) & (df['question_type'] == 'A'),
                'question_translation_latex'
            ] = None

            # Save modified DataFrame
            with open(output_filename, 'wb') as file:
                pickle.dump(df, file)

            print(f"Modified DataFrame saved to {output_filename}")

        else:
            print("Required columns 'question_translation_latex' or 'question_type' not found in the DataFrame.")
    else:
        print("The pickle file does not contain a DataFrame.")
except Exception as e:
    print(f"An error occurred: {e}")
