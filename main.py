from pipeline import run_pipline
import pickle
import os


def load_history(file_path="history.pkl"):
    """Load the conversation history from a pickle file."""
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return pickle.load(f)
    return []

def save_history(history, file_path="history.pkl"):
    """Save the conversation history to a pickle file."""
    with open(file_path, "wb") as f:
        pickle.dump(history, f)


def main():
    history_file = 'history.pkl'
    saved_history = load_history(history_file)
    
    current_history = run_pipline("The deterministic \"select\" algorithm, which we studied in class, works as follows:\
a. The array is divided into groups of size 5\
b. Sort each group\
c. Choose a pivot as the median of the medians (recursively)\
d. Perform \"partition\" with the chosen pivot\
e. Recursively apply the algorithm on the relevant part.\
Assume that instead of groups of size 5, we take groups of size 3. \
In this question, we will deal with the running time of the new algorithm with groups of size 3.\
What is the cost of step b? \
Cost:\
Explanation:")

    # Print the conversation history
    print("\n--- Conversation History ---")
    print("\n".join(current_history))

    saved_history.append(current_history)
    # Save the updated conversation history
    save_history(current_history, history_file)

if __name__ == '__main__':
    main()