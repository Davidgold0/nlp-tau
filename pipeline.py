from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import init_chat_model
import os
from typing import List, Tuple

os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Configure your language model (ensure you have your API key set up)
llm = init_chat_model("gpt-3.5-turbo", model_provider="openai")

# Define prompt templates for each side
student_prompt_template = PromptTemplate(
    input_variables=["question", "history"],
    template="""
Role: You are a student.

Instructions:

1. Role Identification: Remember that you are playing the role of a student.
2. Answering the Teacher’s Question: Focus on answering the specific question given by your teacher. Do not jump straight to providing the final answer to the original problem until the teacher guides you through the necessary steps.
3. Direct Response: When prompted, provide a clear and concise final answer, incorporating any hints or corrections provided by your teacher.
4. Clarity: Ensure that your final answer is well-organized and directly addresses the problem as discussed with your teacher.
5. Reflection: Demonstrate your understanding by thoughtfully integrating the teacher’s guidance into your response.

this is the question:
{question}
this is the messaging history:
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

teacher_prompt_template = PromptTemplate(
    input_variables=["question", "history"],
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

this is the question:
{question}
this is the messaging history:
{history}
"""
)


teacher_prompt_template = PromptTemplate(
    input_variables=["question", "history"],
    template="""
Role: You are a teacher.

Instructions:

1. Role Identification: Remember, you are playing the role of an encouraging and helpful teacher.
2. Initial Engagement: When you receive a new question, do not ask for the final answer immediately. Instead, ask the student to outline the steps needed to solve the problem.
3. Guiding the Process: Once the student outlines the steps, guide them step-by-step by:
    -Asking clarifying or guiding questions about each step.
    -If identified incorrect answer, provide corrections for this specific step, and ask the student to reason the answer before moving to the next step.
    - Providing hints and helpful thoughts to ensure they are on the right track.
4. Iterative Interaction: Continue the conversation by working through each step together, encouraging the student to reflect on their reasoning and to revise their approach if necessary.
5. Summarization: After the process has been thoroughly discussed and each step has been addressed, conclude by summarizing the main points of the conversation, highlighting the correct approach and the final answer.
6. Tone & Style: Maintain a warm, friendly, and supportive tone throughout the interaction.
7. When you are ready and have a final answer add the $ in the end.

this is the question:
{question}
this is the messaging history:
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

    history.append("Question", input_question)
    
    # First, let teacher chain handle the initial question
    teacher_prompt = teacher_prompt_template.invoke({"question": "", "history": ""}) # inputs placeholders into the prompt
    response_a = llm.invoke(teacher_prompt) # runs the llm 
    history.append(("Teacher",f"{response_a.strip()}"))


    while response_a[-1] != "$": # TODO fix this to something smarter
        # student chain takes the latest response from the teacher and the updated history
        student_prompt = student_prompt_template.invoke({"question": "", "history": format_history(history)})
        response_b = llm.invoke(student_prompt)
        history.append(("Student",f"{response_b.strip()}"))

        # teacher now takes the student's answer as the new question and the updated history
        teacher_prompt = teacher_prompt_template.invoke({"question": "", "history": format_history(history)})
        response_a = llm.invoke(teacher_prompt)
        history.append(("Teacher",f"{response_a.strip()}"))
    
    return history
