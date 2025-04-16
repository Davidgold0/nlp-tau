import os
import glob
import pandas as pd
from pipeline import run_pipline, format_history

def main(input_folder, output_folder, n_runs=5):
    """
    Process each Excel file in input_folder.
    For each Excel file, for each row, take the first cell value and run it through process n_runs times.
    The outputs are saved into a structured folder:
    
      output_folder/
         excel_file_name_without_extension/
             Question_1/
                 1.txt, 2.txt, ..., n.txt
             Question_2/
                 1.txt, 2.txt, ..., n.txt
             ...
    
    Parameters:
        input_folder (str): The path where the Excel files are stored.
        output_folder (str): The path where the outputs will be saved.
        n_runs (int): Number of times to run the process for each question.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Find all Excel files (.xlsx and .xls) in the input folder
    excel_files = glob.glob(os.path.join(input_folder, "*.xlsx")) + \
                  glob.glob(os.path.join(input_folder, "*.xls"))

    if not excel_files:
        print("No Excel files found in the specified folder.")
        return
    print(excel_files)
    # Process each Excel file one by one
    for file_path in excel_files:
        file_name = os.path.basename(file_path)
        file_base, _ = os.path.splitext(file_name)
        
        # Create a folder for this Excel file inside the output folder
        excel_output_dir = os.path.join(output_folder, file_base)
        os.makedirs(excel_output_dir, exist_ok=True)

        print(f"Processing file: {file_name}")

        # Read the Excel file (assume no header so every row is a question)
        try:
            df = pd.read_excel(file_path, header=0)
        except Exception as e:
            print(f"Error reading {file_name}: {e}")
            continue

        # Iterate over each row in the DataFrame (excluding header)
        for idx, row in df.iterrows():
            question = row[0]
            if pd.isnull(question):
                continue

            question_index = idx + 1  # Because of header
            question_folder = os.path.join(excel_output_dir, f"Question_{question_index}")
            os.makedirs(question_folder, exist_ok=True)

            for run in range(1, n_runs + 1):
                output_text = run_pipline(question)
                #output_text = question
                output_file_path = os.path.join(question_folder, f"{run}.txt")
                with open(output_file_path, "w", encoding="utf-8") as f:
                    f.write(format_history(output_text))
                     #f.write(output_text)

            print(f"Processed Question {idx+1} from {file_name}")

if __name__ == "__main__":
    # Configuration: adjust these variables as needed
    INPUT_FOLDER = ".//datasets//runable_problems//hide"  # Directory where the Excel files are located
    OUTPUT_FOLDER = "output"            # Directory where the processed files will be saved
    N_RUNS = 5                          # Number of times to run the process for each question

    main(INPUT_FOLDER, OUTPUT_FOLDER, N_RUNS)
