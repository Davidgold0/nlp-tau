from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import init_chat_model
import os
from typing import List, Tuple

os.environ["OPENAI_API_KEY"] = # TODO enter your key
# Configure your language model (ensure you have your API key set up)
llm_student = init_chat_model("gpt-4o-mini", model_provider="openai", temperature = 0.3)
# llm_teacher = init_chat_model("gpt-4o-mini", model_provider="openai", temperature = 0.5)

# llm_student = init_chat_model("o3-mini", model_provider="openai")
llm_teacher = init_chat_model("o3-mini", model_provider="openai")

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

student_prompt_chain_of_thought_template = PromptTemplate(
    input_variables=["question", "history"],
    template="""
Role: You are a student.

Instructions:

1. Role Identification: Keep in mind that you are playing the role of a student.
2. Answering the Teacher’s Question: Begin by addressing the teacher’s guiding question. Focus on detailing your thought process in response to the teacher’s question rather than providing the final answer directly.
3. Step-by-Step Reasoning: Outline the steps needed to solve the problem and provide a detailed explanation of your complete chain of thought:
    - Start with interpreting the question.
    - Break down the solution process into clear, sequential steps (including any calculations, insights, or reasoning).
4. Feedback Integration: Adjust your reasoning by incorporating any corrections or additional hints given by your teacher.
5. Final Answer: Conclude your explanation with the final answer that results from your detailed reasoning, only when prompted by the teacher.

this is the question:
{question}
this is the messaging history:
{history}
"""
)

first_teacher_prompt_template = PromptTemplate(
    input_variables=["history"],
    template="""
Role: You are a teacher.

Instructions:

1. Role Identification: Remember, you are playing the role of an encouraging and helpful teacher.
2. Initial Engagement: When you receive a new question, do not ask for the final answer immediately. Instead, ask the student to outline the steps needed to solve the problem.
3. Guiding the Process: Once the student outlines the steps, guide them step-by-step by:
    -Asking clarifying or guiding questions about each step.
    -Providing correction, hints and helpful thoughts to ensure they are on the right track.
4. Iterative Interaction: Continue the conversation by working through each step together, encouraging the student to reflect on their reasoning and to revise their approach if necessary.
5. Summarization: After the process has been thoroughly discussed and each step has been addressed, conclude by summarizing the main points of the conversation, highlighting the correct approach and the final answer.
6. Tone & Style: Maintain a warm, friendly, and supportive tone throughout the interaction.
7. When you are ready and have a final answer add the $ in the end.

this is the messaging history:
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
6. When the student reaches the final answer, mention it and add the $ in the end without any punctuation marks. Finish the conversation immediatly without offering other help.


This is the messaging history:
{history}
"""
)
# 6. Tone & Style: Maintain a warm, friendly, and supportive tone throughout the interaction.
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
    print(f"****/n 	\033[91m Teacher: \033[0m{response_a.content.strip()}")
    history.append(("Teacher",f"{response_a.content.strip()}"))

    cnt = 0
    while end_session(response_a.content) == False and cnt < 15: # TODO fix this to something smarter
        cnt += 1
        # student chain takes the latest response from the teacher and the updated history
        student_prompt = student_prompt_template.invoke({"history": format_history(history)})
        response_b = llm_student.invoke(student_prompt)
        print(f"****/n \033[94m Student: \033[0m{response_b.content.strip()}")
        history.append(("Student",f"{response_b.content.strip()}"))

        # teacher now takes the student's answer as the new question and the updated history
        teacher_prompt = teacher_prompt_template.invoke({"history": format_history(history)})
        response_a = llm_teacher.invoke(teacher_prompt)
        print(f"****/n \033[91m Teacher: \033[0m{response_a.content.strip()}")
        history.append(("Teacher",f"{response_a.content.strip()}"))
    
    return history

def run_pipline_without_history(input_question: str) -> List[Tuple[str, str]]:
    cnt = 0
    # student chain takes the latest response from the teacher and the updated history
    response_b = llm_student.invoke(input_question)
    print(f"****/n \033[94m Student: \033[0m{response_b.content.strip()}")
    return response_b

def end_session(response: str) -> bool:
    if response.endswith("$") or response.endswith("$."):
        return True
    return False
