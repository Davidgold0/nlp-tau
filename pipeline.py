from langchain.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
import os
from typing import List, Tuple

os.environ["OPENAI_API_KEY"] = None
llm_student = init_chat_model("gpt-4o-mini", model_provider="openai", temperature = 0.5)
llm_teacher = init_chat_model("o3-mini", model_provider="openai")

regular_model = init_chat_model("o3-mini", model_provider="openai")

# Define prompt templates for each side
student_prompt_template = PromptTemplate(
    input_variables=["history"],
    template="""
Role: You are a student being guided by a teacher to solve a question.

Instructions:

1. Role Identification: Remember that you are playing the role of a student.
2. Answering the Teacher’s Question: Focus on answering the specific question given by your teacher. Do not jump straight to providing the final answer to the original problem until the teacher guides you through the necessary steps.
3. Direct Response: When prompted, provide a clear and concise answer, incorporating any hints or corrections provided by your teacher.
4. Clarity: Ensure that your answer is well-organized and directly addresses the question provided by your teacher.
5. Reflection: Demonstrate your understanding by thoughtfully integrating the teacher’s guidance into your response.

This is the messaging history:
{history}
"""
)

teacher_prompt_template = PromptTemplate(
    input_variables=["history"],
    template="""
Role: You are a teacher.

Instructions:

1. Role Identification: Remember, you are playing the role of an encouraging and helpful teacher. You are not allowed to solve the question directly at any step.
2. Initial Engagement: When you receive a new question, do not ask for the final answer immediately. Instead, outline the steps needed to solve the problem.
    - You may rephrase the question the way that will help you the best to understand the question and to guide the student.
3. Guiding the Process: Once you outline the steps, guide them by following this pipeline:
    a. Ask the student to solve the next step and only the next step towards the final answer.
    b. Read the students response, Check each answer/calculation/conclution of the student. Don't assume the student is correct! 
    c. Give feedback: asking clarifying or guiding questions about this specific step. 
    d. If needed, provide correction, hints and helpful thoughts and ask the student to revise his answer.
    e. Remember you are teacher, you don't solve the steps. You are only there to guide the student.
4. Iterative Interaction: Continue the conversation by working through each step together, encouraging the student to reflect on their reasoning and to revise their approach if necessary.
5. Summarization: After the process has been thoroughly discussed and each step has been addressed, conclude by summarizing the main points of the conversation, highlighting the correct approach and the final answer.
6. When the student reaches the final answer, state it followed immediately by a $, with absolutely nothing after the $ — no letters, symbols, or punctuation. End the conversation at that point without offering further assistance.


This is the messaging history:
{history}
"""
)

def format_history(history: List[Tuple[str, str]]) -> str:
    """
    Formats the conversation history as a string.

    Args:
        history (List[Tuple[str, str]]): A list where each tuple contains a role (e.g., "Teacher", "Student")
                                         and the corresponding message.

    Returns:
        str: A string with each turn on a new line in the format "Role: message".
    """
    return "\n".join(f"{role}: {message}" for role, message in history)


def run_pipline(input_question: str) -> List[Tuple[str,str]]:
    '''
    the function runs the pipline and return the full history
    '''
    # Initialize conversation history and the initial input question
    history: List[Tuple[str,str]] = []

    history.append(("Question", input_question))
    
    # First, let teacher chain handle the initial question
    teacher_prompt = teacher_prompt_template.invoke({"history": format_history(history)}) # inputs placeholders into the prompt
    response_a = llm_teacher.invoke(teacher_prompt) # runs the llm 
    # print(f"****/n 	\033[91m Teacher: \033[0m{response_a.content.strip()}")
    history.append(("Teacher",f"{response_a.content.strip()}"))

    cnt = 0
    while end_session(response_a.content) == False and cnt < 30: 
        cnt += 1
        # student chain takes the latest response from the teacher and the updated history
        student_prompt = student_prompt_template.invoke({"history": format_history(history)})
        response_b = llm_student.invoke(student_prompt)
        # print(f"****/n \033[94m Student: \033[0m{response_b.content.strip()}")
        history.append(("Student",f"{response_b.content.strip()}"))

        # teacher now takes the student's answer as the new question and the updated history
        teacher_prompt = teacher_prompt_template.invoke({"history": format_history(history)})
        response_a = llm_teacher.invoke(teacher_prompt)
        # print(f"****/n \033[91m Teacher: \033[0m{response_a.content.strip()}")
        history.append(("Teacher",f"{response_a.content.strip()}"))
    
    return history

def run_on_3o_mini(input_question: str) ->  List[Tuple[str, str]]:
    history: List[Tuple[str,str]] = []

    history.append(("Question", input_question))
    response = regular_model.invoke(input_question)
    # print(f"****/n \033[92m gpt-3o-mini: \033[0m{response.content.strip()}")
    history.append(("3o-mini",f"{response.content.strip()}"))
    return history

def end_session(response: str) -> bool:
    if response.endswith("$") or response.endswith("$."):
        return True
    return False
