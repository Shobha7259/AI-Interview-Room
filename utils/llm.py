from openai import OpenAI

# 🔥 OpenRouter setup
client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

# -------------------------------
# BASE FUNCTION
# -------------------------------
def ask_ai(prompt):
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an interview coach"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# -------------------------------
# GENERATE QUESTION
# -------------------------------
def generate_question():
    prompt = """
    Generate ONE interview question for a computer science student.

    Rules:
    - Ask only one question
    - Mix technical + HR
    - Keep it short

    Output only the question.
    """
    return ask_ai(prompt)


# -------------------------------
# EVALUATE ANSWER
# -------------------------------
def evaluate_answer(question, answer):
    prompt = f"""
    You are a strict interview evaluator.

    Question: {question}
    Candidate Answer: {answer}

    Evaluate and return:

    Score: X/10
    Feedback: 2-3 lines explaining strengths and improvements
    """
    return ask_ai(prompt)