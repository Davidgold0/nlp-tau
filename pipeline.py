from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import init_chat_model
import os
from typing import List

os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Configure your language model (ensure you have your API key set up)
llm = init_chat_model("gpt-3.5-turbo", model_provider="openai")

# Define prompt templates for each side
student_prompt_template = PromptTemplate(
    input_variables=["question", "history"],
    template="""
You are Prompt A.
Given the following conversation history:
{history}
And a new question:
{question}
Provide your detailed response.
"""
)

teacher_prompt_template = PromptTemplate(
    input_variables=["question", "history"],
    template="""
You are Prompt B.
Using the previous question:
{question}
and the conversation history:
{history}
Generate your follow-up response.
"""
)

def format_history(history: List[str]) -> str:
    return ""


def run_pipline(input_question: str) -> List[str]:
    '''
    the function runs the pipline and return the full history
    '''
    # Initialize conversation history and the initial input question
    history = []
    
    # First, let teacher chain handle the initial question
    teacher_prompt = teacher_prompt_template.invoke({"question": "", "history": format_history(history)}) # inputs placeholders into the prompt
    response_a = llm.invoke(teacher_prompt) # runs the llm 
    history.append(f"Prompt A: {response_a.strip()}")


    while response_a[-1] != "$": # TODO fix this to something smarter
        # student chain takes the latest response from the teacher and the updated history
        student_prompt = student_prompt_template.invoke({"question": "", "history": format_history(history)})
        response_b = llm.invoke(student_prompt)
        history.append(f"Prompt B: {response_b.strip()}")

        # teacher now takes the student's answer as the new question and the updated history
        teacher_prompt = teacher_prompt_template.invoke({"question": "", "history": format_history(history)})
        response_a = llm.invoke(teacher_prompt)
        history.append(f"Prompt A: {response_a.strip()}")
