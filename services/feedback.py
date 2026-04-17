from utils.llm import ask_ai

def get_feedback(question, answer):
    prompt = f"""
    You are an AI interviewer.

    Question: {question}
    Answer: {answer}

    Respond EXACTLY in this format:

    Score: <number out of 10>
    Strengths: <points>
    Weakness: <points>
    Communication: <score out of 10>
    """
    return ask_ai(prompt)