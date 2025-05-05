import os
import pandas as pd
import csv

# Path to the folder containing Question_1 to Question_50
main_folder = './results/math_questions'  # <-- Change this

columns = ['question'] + [f'response {i}' for i in range(1, 11)]
data = []

for i in range(1, 51):
    row = [f'question {i}']
    subfolder_name = f'Question_{i}'
    subfolder_path = os.path.join(main_folder, subfolder_name)
    
    if not os.path.isdir(subfolder_path):
        print(f"Missing subfolder: {subfolder_path}")
        row.extend([''] * 10)
        data.append(row)
        continue

    for j in range(1, 11):
        txt_path = os.path.join(subfolder_path, f'{j}.txt')
        if os.path.exists(txt_path):
            with open(txt_path, 'r', encoding='utf-8') as f:
                # Flatten newlines and strip extra whitespace
                content = f.read().replace('\n', ' ').replace('\r', ' ').strip()
                # Optional: replace multiple spaces with a single space
                content = ' '.join(content.split())
        else:
            print(f"Missing file: {txt_path}")
            content = ''
        row.append(content)
    
    data.append(row)

df = pd.DataFrame(data, columns=columns)

# Save CSV with full quoting
df.to_excel('math_questions.xlsx', index=False)

# Save Pickle normally
df.to_pickle('math_questions.pkl')

print("✅ Saved 'output.csv' and 'output.pkl'")
