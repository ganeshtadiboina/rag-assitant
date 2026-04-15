from openai import OpenAI
from typing import List, Tuple
from configs.settings import settings


class RAGGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.LLM_MODEL

    def _build_context(self, documents: List[str]) -> Tuple[str, List[str]]:
        context_parts = []
        for idx, doc in enumerate(documents, start=1):
            context_parts.append(f"[Doc{idx}] {doc}")
        return "\n\n".join(context_parts)

    def generate(self, query: str, documents: List[str]) -> str:
        if not documents:
            return "I don't know."

        context = self._build_context(documents)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                        Answer the question using only the context below.
                        Include citations like [Doc1], [Doc2].

                        Context:
                        {context}

                        Question: {query}
                        Answer:
                    """,
                }
            ],
            temperature=0,
        )

        return response.choices[0].message.content.strip()