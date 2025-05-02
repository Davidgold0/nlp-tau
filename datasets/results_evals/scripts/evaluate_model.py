from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel

# Function to compute evaluation metrics
def evaluate_model(df, dataset_name):
    teacher_cols = [col for col in df.columns if "Teacher - Student" in col]
    o3_cols = [col for col in df.columns if "O3-mini" in col]

    # Average accuracy per model
    teacher_acc = df[teacher_cols].mean(axis=1)
    o3_acc = df[o3_cols].mean(axis=1)

    # Overall accuracy
    avg_teacher_acc = teacher_acc.mean()
    avg_o3_acc = o3_acc.mean()

    # Win/Loss/Draw
    wins = (teacher_acc > o3_acc).sum()
    losses = (teacher_acc < o3_acc).sum()
    draws = (teacher_acc == o3_acc).sum()

    return {
        "Dataset": dataset_name,
        "Teacher Avg Accuracy": avg_teacher_acc,
        "O3-mini Avg Accuracy": avg_o3_acc,
        "Wins (Teacher > O3)": wins,
        "Losses (Teacher < O3)": losses,
        "Draws": draws,
        "Total Questions": len(df)
    }



def vizualize_results(math_df, chess_df, exam_df):

    teacher_acc_math = compute_accuracy_distribution(math_df, "Teacher")
    teacher_acc_chess = compute_accuracy_distribution(chess_df, "Teacher")
    teacher_acc_exam = compute_accuracy_distribution(exam_df, "Teacher")

    o3_acc_math = compute_accuracy_distribution(math_df, "O3-mini")
    o3_acc_chess = compute_accuracy_distribution(chess_df, "O3-mini")
    o3_acc_exam = compute_accuracy_distribution(exam_df, "-mini")

    
    # Improved side-by-side bar visualization
    fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)

    datasets = ["Math", "Chess", "Exam"]
    teacher_dfs = [teacher_acc_math, teacher_acc_chess, teacher_acc_exam]
    o3_dfs = [o3_acc_math, o3_acc_chess, o3_acc_exam]

    bins = np.linspace(0, 1, 6)  # bins: [0.0, 0.2, ..., 1.0]
    width = 0.04  # bar width

    for ax, dataset, teacher_data, o3_data in zip(axes, datasets, teacher_dfs, o3_dfs):
        # Get histogram counts
        teacher_counts, _ = np.histogram(teacher_data, bins=bins)
        o3_counts, _ = np.histogram(o3_data, bins=bins)

        # Bin centers for bar positions
        bin_centers = bins[:-1] + (bins[1] - bins[0]) / 2

        # Plot bars side by side
        ax.bar(bin_centers - width/2, teacher_counts, width=width, label='Teacher-Student', color="#AEC6CF", edgecolor='black')
        ax.bar(bin_centers + width/2, o3_counts, width=width, label='O3-mini', color="#FFB347", edgecolor='black')

        ax.set_title(f"{dataset} Accuracy Distribution")
        ax.set_xlabel("Per-question accuracy (correct/5)")
        ax.set_xticks(bins)
        ax.grid(True)

    axes[0].set_ylabel("Number of questions")
    axes[1].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=2)
    fig.suptitle("Side-by-Side Per-Question Accuracy Distribution by Dataset", fontsize=16)
    plt.tight_layout()
    plt.show()

    

def compute_accuracy_distribution(df, model_name):
    if model_name == "Teacher":
        cols = [col for col in df.columns if "Teacher - Student" in col]
    else:
        cols = [col for col in df.columns if "O3-mini" in col]
    return df[cols].mean(axis=1)


# Helper function to compute metrics for a dataset
def compute_additional_metrics(df, dataset_name):
    teacher_cols = [col for col in df.columns if "Teacher - Student" in col]
    o3_cols = [col for col in df.columns if "O3-mini" in col]
    
    teacher_acc = df[teacher_cols].mean(axis=1)
    o3_acc = df[o3_cols].mean(axis=1)
    
    teacher_std = df[teacher_cols].std(axis=1).mean()
    o3_std = df[o3_cols].std(axis=1).mean()
    
    exact_5_teacher = (df[teacher_cols].sum(axis=1) == 5).mean()
    exact_5_o3 = (df[o3_cols].sum(axis=1) == 5).mean()
    
    win_margin = teacher_acc - o3_acc
    
    # Paired t-test
    t_stat, p_value = ttest_rel(teacher_acc, o3_acc)

    return {
        "Dataset": dataset_name,
        "Teacher Std Accuracy": teacher_std,
        "O3 Std Accuracy": o3_std,
        "Teacher Exact 5/5 %": exact_5_teacher,
        "O3 Exact 5/5 %": exact_5_o3,
        "T-statistic": t_stat,
        "P-value": p_value,
        "Win Margin Mean": win_margin.mean(),
        "Win Margin Std": win_margin.std()
    }, win_margin

def evaluate_model_via_additional_metrics(math_df, chess_df, exam_df):
    #Compute metrics and margins
    metrics_math, margin_math = compute_additional_metrics(math_df, "Math")
    metrics_chess, margin_chess = compute_additional_metrics(chess_df, "Chess")
    metrics_exam, margin_exam = compute_additional_metrics(exam_df, "Exam")

    # Combine and display
    additional_metrics_df = pd.DataFrame([metrics_math, metrics_chess, metrics_exam])

    # Save additional evaluation metrics to CSV and Excel
    additional_csv_path = "additional_evaluation_metrics.csv"
    additional_excel_path = "additional_evaluation_metrics.xlsx"

    additional_metrics_df.to_csv(additional_csv_path, index=False)
    additional_metrics_df.to_excel(additional_excel_path, index=False)

    # visualize results
    vizualize_win_margin(margin_math, margin_chess, margin_exam)

    return additional_csv_path, additional_excel_path

def vizualize_win_margin(margin_math, margin_chess, margin_exam):
    # Refactored win margin distribution plot with improved style and separation
    fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)

    dataset_margins = {
        "Math": margin_math,
        "Chess": margin_chess,
        "Exam": margin_exam
    }

    colors = {
        "Math": "#A1D99B",   # green
        "Chess": "#FC9272",  # red
        "Exam": "#9ECAE1"    # blue
    }

    for ax, (name, margin) in zip(axes, dataset_margins.items()):
        sns.histplot(margin, kde=True, bins=10, color=colors[name], ax=ax, edgecolor="black")
        ax.axvline(x=0, color='black', linestyle='--')
        ax.set_title(f"{name} - Win Margin (Teacher - O3)")
        ax.set_xlabel("Accuracy Difference")
        ax.set_ylabel("Number of Questions")
        ax.grid(True)

    fig.suptitle("Distribution of Win Margins per Dataset", fontsize=16)
    plt.tight_layout()
    plt.show()

def visualize_std(math_df, chess_df, exam_df):
    # Calculate per-question standard deviation for each model
    teacher_std_math = math_df[[col for col in math_df.columns if "Teacher - Student" in col]].std(axis=1)
    teacher_std_chess = chess_df[[col for col in chess_df.columns if "Teacher - Student" in col]].std(axis=1)
    teacher_std_exam = exam_df[[col for col in exam_df.columns if "Teacher - Student" in col]].std(axis=1)

    o3_std_math = math_df[[col for col in math_df.columns if "O3-mini" in col]].std(axis=1)
    o3_std_chess = chess_df[[col for col in chess_df.columns if "O3-mini" in col]].std(axis=1)
    o3_std_exam = exam_df[[col for col in exam_df.columns if "O3-mini" in col]].std(axis=1)

    # Plotting standard deviation histograms with side-by-side columns per bin
    fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)

    bar_width = 0.015
    bin_edges = np.linspace(0, 0.5, 11)
    bin_centers = bin_edges[:-1] + (bin_edges[1] - bin_edges[0]) / 2

    std_math = (teacher_std_math, o3_std_math)
    std_chess = (teacher_std_chess, o3_std_chess)
    std_exam = (teacher_std_exam, o3_std_exam)

    # Histogram-based std data
    datasets = ["Math", "Chess", "Exam"]
    std_data = [std_math, std_chess, std_exam]

    for ax, name, (teacher_std, o3_std) in zip(axes, datasets, std_data):
        teacher_counts, _ = np.histogram(teacher_std, bins=bin_edges)
        o3_counts, _ = np.histogram(o3_std, bins=bin_edges)

        # Plot bars side by side
        ax.bar(bin_centers - bar_width/2, teacher_counts, width=bar_width,
            label="Teacher-Student", color="#AEC6CF", edgecolor="black")
        ax.bar(bin_centers + bar_width/2, o3_counts, width=bar_width,
            label="O3-mini", color="#FFB347", edgecolor="black")

        ax.set_title(f"{name} - Std. Dev. of Accuracy Across Runs")
        ax.set_xlabel("Standard Deviation")
        ax.set_xticks(bin_edges)
        ax.set_ylabel("Number of Questions")
        ax.grid(True)

    axes[1].legend(loc="upper center", bbox_to_anchor=(0.5, 1.2), ncol=2)
    fig.suptitle("Side-by-Side Std. Dev. of Accuracy per Question", fontsize=16)
    plt.tight_layout()
    plt.show()

# Recalculate majority vote accuracy after normalizing if values range from 0–5 instead of 0–1

def compute_majority_vote_accuracy_fixed(df, dataset_name):
    teacher_majority_col = [col for col in df.columns if "majority Teacher-Student" in col][0]
    o3_majority_col = [col for col in df.columns if "majority O3" in col][0]

    # Normalize if values are not binary (assume range 0–5)
    teacher_values = df[teacher_majority_col]
    o3_values = df[o3_majority_col]

    if teacher_values.max() > 1:
        teacher_values = teacher_values / 5
    if o3_values.max() > 1:
        o3_values = o3_values / 5

    teacher_majority_acc = teacher_values.mean()
    o3_majority_acc = o3_values.mean()

    return {
        "Dataset": dataset_name,
        "Teacher Majority Accuracy (%)": round(teacher_majority_acc * 100, 2),
        "O3-mini Majority Accuracy (%)": round(o3_majority_acc * 100, 2)
    }



def visualize_majority_vote_accuracy(math_df, chess_df, exam_df):

    # Apply corrected function
    majority_results_fixed = [
        compute_majority_vote_accuracy_fixed(math_df, "Math"),
        compute_majority_vote_accuracy_fixed(chess_df, "Chess"),
        compute_majority_vote_accuracy_fixed(exam_df, "Exam")
    ]

    majority_vote_df_fixed = pd.DataFrame(majority_results_fixed)
    # Re-plot the corrected chart
    fig, ax = plt.subplots(figsize=(8, 5))

    x = majority_vote_df_fixed["Dataset"]
    width = 0.35
    x_pos = np.arange(len(x))

    ax.bar(x_pos - width/2, majority_vote_df_fixed["Teacher Majority Accuracy (%)"], width=width, label="Teacher-Student", color="#AEC6CF", edgecolor="black")
    ax.bar(x_pos + width/2, majority_vote_df_fixed["O3-mini Majority Accuracy (%)"], width=width, label="O3-mini", color="#FFB347", edgecolor="black")

    ax.set_xticks(x_pos)
    ax.set_xticklabels(x)
    ax.set_ylabel("Accuracy (%)")
    ax.set_title("Corrected Majority Vote Accuracy by Dataset")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()

# Prepare the data manually from the earlier average accuracy results
avg_accuracy_data = {
    "Dataset": ["Math", "Chess", "Exam"],
    "Teacher Avg Accuracy (%)": [1.788235294117647 * 20, 0.2196078431372549 * 20, 1.364705882352941 * 20],
    "O3-mini Avg Accuracy (%)": [1.8901960784313727 * 20, 0.4941176470588236 * 20, 1.6235294117647059 * 20]
}

def visualize_scaled_percentage_accuracy():
    avg_accuracy_data = {
    "Dataset": ["Math", "Chess", "Exam"],
    "Teacher Avg Accuracy (%)": [
        1.788235294117647 * 20,  # Math: 1.788 correct out of 5 → ~35.76%
        0.2196078431372549 * 20, # Chess: ~4.39%
        1.364705882352941 * 20   # Exam: ~27.29%
    ],
    "O3-mini Avg Accuracy (%)": [
        1.8901960784313727 * 20, # Math: ~37.80%
        0.4941176470588236 * 20, # Chess: ~9.88%
        1.6235294117647059 * 20  # Exam: ~32.47%
    ]
    }
    # Convert to DataFrame
    avg_accuracy_df = pd.DataFrame(avg_accuracy_data)

    # Display the DataFrame to the user

    # Plot side-by-side bar chart
    fig, ax = plt.subplots(figsize=(8, 5))

    x = avg_accuracy_df["Dataset"]
    x_pos = np.arange(len(x))
    width = 0.35

    ax.bar(x_pos - width/2, avg_accuracy_df["Teacher Avg Accuracy (%)"], width=width, label="Teacher-Student", color="#AEC6CF", edgecolor="black")
    ax.bar(x_pos + width/2, avg_accuracy_df["O3-mini Avg Accuracy (%)"], width=width, label="O3-mini", color="#FFB347", edgecolor="black")

    ax.set_xticks(x_pos)
    ax.set_xticklabels(x)
    ax.set_ylabel("Average Accuracy (%)")
    ax.set_title("Average Accuracy per Dataset (Scaled to 5 Questions)")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    xls = pd.ExcelFile("Results.xlsx")
    math_df = xls.parse("Math")
    chess_df = xls.parse("Chess")
    exam_df = xls.parse("Exam")

    # # Evaluate all datasets
    # results = [
    #     evaluate_model(math_df, "Math"),
    #     evaluate_model(chess_df, "Chess"),
    #     evaluate_model(exam_df, "Exam")
    # ]

    # # Convert to DataFrame for display
    # summary_df = pd.DataFrame(results)

    # # Save the summary DataFrame to both CSV and Excel
    # csv_path = "model_evaluation_summary.csv"
    # excel_path = "model_evaluation_summary.xlsx"

    # summary_df.to_csv(csv_path, index=False)
    # summary_df.to_excel(excel_path, index=False)
    
    # # Add vizualization
    # vizualize_results(math_df, chess_df, exam_df)

    # Compute Standard deviation
    # evaluate_model_via_additional_metrics(math_df, chess_df, exam_df)
    # visualize_std(math_df, chess_df, exam_df)

    # visualize_majority_vote_accuracy(math_df, chess_df, exam_df)

    visualize_scaled_percentage_accuracy()

if __name__ == "__main__":
    main()
