from openai import OpenAI
from configs.settings import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def judge_answer(question, expected, actual):
    prompt = f"""
You are evaluating an AI answer.

Question: {question}
Expected Answer: {expected}
Actual Answer: {actual}

Score from 0 to 1 based on correctness and completeness.
Return ONLY a number.
"""

    response = client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    try:
        return float(response.choices[0].message.content.strip())
    except:
        return 0.0