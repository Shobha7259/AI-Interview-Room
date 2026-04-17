from utils.llm import ask_ai

def get_followup(question):
    prompt = f"Generate a follow-up interview question based on: {question}"
    return ask_ai(prompt)