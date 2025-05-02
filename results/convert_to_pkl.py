import os
import pandas as pd

def convert_to_pkl(input_root, output_root, txt_delimiter="\t"):
    for subdir, _, files in os.walk(input_root):
        for file in files:
            input_path = os.path.join(subdir, file)
            rel_path = os.path.relpath(subdir, input_root)
            output_subdir = os.path.join(output_root, rel_path)
            os.makedirs(output_subdir, exist_ok=True)

            file_stem, ext = os.path.splitext(file)
            output_path = os.path.join(output_subdir, file_stem + '.pkl')

            try:
                if ext.lower() == '.txt':
                    df = pd.read_csv(input_path, sep=txt_delimiter)
                    df.to_pickle(output_path)
                    print(f"✅ Converted: {input_path} -> {output_path}")
                else:
                    print(f"⏭️ Skipping unsupported file: {input_path}")
            except Exception as e:
                print(f"❌ Failed to convert {input_path}: {e}")

def convert_txt_to_csv(input_root, output_root, txt_delimiter="\t"):
    for subdir, _, files in os.walk(input_root):
        for file in files:
            input_path = os.path.join(subdir, file)
            rel_path = os.path.relpath(subdir, input_root)
            output_subdir = os.path.join(output_root, rel_path)
            os.makedirs(output_subdir, exist_ok=True)

            file_stem, ext = os.path.splitext(file)
            output_path = os.path.join(output_subdir, file_stem + '.csv')

            try:
                if ext.lower() == '.txt':
                    df = pd.read_csv(input_path, sep=txt_delimiter)
                    df.to_csv(output_path, index=False)
                    print(f"✅ Converted: {input_path} -> {output_path}")
                else:
                    print(f"⏭️ Skipping unsupported file: {input_path}")
            except Exception as e:
                print(f"❌ Failed to convert {input_path}: {e}")

def main():
    input_folder = "exam_questions"
    output_folder = "exam_questions_csv"
    convert_txt_to_csv(input_folder, output_folder)

if __name__ == "__main__":
    main()
