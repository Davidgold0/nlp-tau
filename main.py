from pipeline import run_pipline, format_history
import os


def load_history(file_path="history.txt"):
    """Load the conversation history from a text file."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.readlines()  # Read lines as a list
    return []

def save_history(history, file_path="history.txt"):
    """Save the conversation history to a text file."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(format_history(history))  # Write list of strings to file



def main():
    history_file = 'history.txt'
    saved_history = load_history(history_file)
    
    current_history = run_pipline("""
\\begin{itemize}
    \\item What is the data structure with the worst-case search time?
    \\item A. A hash table with collision resolution by linked lists.
    \\item B. Perfect Hash
    \\item C. A max heap implemented by an array.
    \\item D. answers A and B
    \\item E. answers A and C
    \\item F. answers A and B and C
\\end{itemize}
""")


    # Print the conversation history
    #print("\n--- Conversation History ---")
    #print("\n".join(current_history))

    saved_history.append(current_history)
    # Save the updated conversation history
    save_history(current_history, history_file)

def count_repetitions():
    history_file = 'history.txt'
    saved_history = load_history(history_file)


if __name__ == '__main__':
    main()