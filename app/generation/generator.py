from openai import OpenAI
from configs.settings import settings


class RAGGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.LLM_MODEL

    def generate(self, query: str, documents: list):

        if not documents:
            return {
                "answer": "I don't know.",
                "sources": []
            }

        context = ""
        sources = []

        for i, doc in enumerate(documents, start=1):

            # 🔥 SAFETY FIX (IMPORTANT)
            if isinstance(doc, str):
                text = doc
                metadata = {}
            else:
                text = doc.get("page_content", "")
                metadata = doc.get("metadata", {})

            tag = f"[Doc{i}]"
            context += f"{tag} {text}\n\n"

            sources.append({
                "tag": tag,
                "source": metadata.get("source", "unknown"),
                "document_id": metadata.get("document_id"),
            })

        system = (
            "You answer questions using only the provided context passages. "
            "You must give a direct, substantive reply: include concrete facts, "
            "definitions, rules, steps, rights, obligations, or exceptions actually "
            "stated in the context. Paraphrase clearly; quote short phrases when helpful. "
            "Do not answer with only document pointers (for example, do not say the "
            "information is in [Doc1] or that the user should refer to a document "
            "without explaining what that passage says). "
            "If the context supports an answer, explain it fully. "
            "If it does not, say clearly what is not stated and give only what is supported. "
            "After claims grounded in a passage, add citations like [Doc1] where appropriate."
        )

        user = f"""Context (numbered passages):

{context}

Question: {query}

Write the answer now. Base every substantive point on the context above."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0,
        )

        return {
            "answer": response.choices[0].message.content.strip(),
            "sources": sources
        }