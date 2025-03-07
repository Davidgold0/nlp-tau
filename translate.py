import pandas as pd
# Load the newly uploaded Excel file
excel_file_path = "Book1.xlsx"

# Read the Excel file
df = pd.read_excel(excel_file_path, sheet_name=None)  # Load all sheets

# Extract the first sheet's name and data
sheet_name = list(df.keys())[0]
data = df[sheet_name]

# Convert each row into a list of strings
rows_as_lists = data.astype(str).values.tolist()

# Format the data into a Python script
python_code = "data = [\n"
for row in rows_as_lists:
    python_code += f"    {row},\n"
python_code += "]"

# Save to a Python file
python_file_path = "/mnt/data/data_as_strings.py"
with open(python_file_path, "w", encoding="utf-8") as file:
    file.write(python_code)

# Provide the download link
python_file_path
