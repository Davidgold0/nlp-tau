from pipeline import run_pipline, format_history, run_pipline_without_history
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
    
    exam_question = """
\\begin{itemize}
    \\item What is the data structure with the worst-case search time?
    \\item A. A hash table with collision resolution by linked lists.
    \\item B. Perfect Hash
    \\item C. A max heap implemented by an array.
    \\item D. answers A and B
    \\item E. answers A and C
    \\item F. answers A and B and C
\\end{itemize}
"""
    chess_question = """
You are a very strong chess engine.

The chess board is in the following state (FEN):
 '8/5p2/P4p1p/1p1k4/8/7P/6PK/8 w - - 1 45'  

What is the best move for white? Answer in the format of UCI for a single best move.

"""

    math_question = r"""
"Because of redistricting, Liberty Middle School\'s enrollment increased to 598 students.
This is an increase of $4\%$ over last year\'s enrollment. What was last year\'s enrollment?"
"""
    current_history = run_pipline(chess_question)

    # Print the conversation history
    #print("\n--- Conversation History ---")
    #print("\n".join(current_history))

    saved_history.append(current_history)
    # Save the updated conversation history
    save_history(current_history, history_file)

def main2():
    math_question = r"""
"Because of redistricting, Liberty Middle School\'s enrollment increased to 598 students.
This is an increase of $4\%$ over last year\'s enrollment. What was last year\'s enrollment?"
"""
    response = run_pipline_without_history(math_question)

def count_repetitions():
    history_file = 'history.txt'
    saved_history = load_history(history_file)


if __name__ == '__main__':
    main()