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
Let \[P(x) = (2x^4 - 26x^3 + ax^2 + bx + c)(5x^4 - 80x^3 + dx^2 + ex + f),\]where $a, b, c, d, e, f$ are real numbers. Suppose that the set of all complex roots of $P(x)$ is $\{1, 2, 3, 4, 5\}.$ Find $P(6).$
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
    current_history = run_pipline(exam_question)

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