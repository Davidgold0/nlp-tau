import pandas as pd

def convert_xlsx_to_python_list(xlsx_path, output_py_path):
    # Load the Excel file
    df = pd.read_excel(xlsx_path, sheet_name=None)  # Load all sheets
    
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
    with open(output_py_path, "w", encoding="utf-8") as file:
        file.write(python_code)
    
    print(f"Data has been successfully written to {output_py_path}")

# Example usage
xlsx_path = "Book1.xlsx"  # Replace with your actual file path
output_py_path = "output_data.py"  # Output Python file
convert_xlsx_to_python_list(xlsx_path, output_py_path)
