import json
from pathlib import Path

from api.evals.metrics import keyword_score, semantic_score
from api.evals.llm_judge import judge_answer
from api.services.rag_services import RAGService
from configs.settings import settings

rag = RAGService()

_EVAL_DIR = Path(__file__).resolve().parent


def evaluate():
    with open(_EVAL_DIR / "eval_dataset.json") as f:
        dataset = json.load(f)

    results = []

    for item in dataset:
        question = item["question"]
        expected = item["expected_answer"]
        keywords = item.get("expected_keywords", [])
        thread_id = item["thread_id"]

        result = rag.query(question, thread_id)
        answer = result["answer"]

        sem = semantic_score(expected, answer)
        kw = keyword_score(keywords, answer)
        judge = judge_answer(question, expected, answer)

        final_score = (sem * 0.4) + (kw * 0.2) + (judge * 0.4)

        print("\n----------------------")
        print("Q:", question)
        print("Answer:", answer)
        print(f"Semantic: {sem:.2f}, Keyword: {kw:.2f}, Judge: {judge:.2f}")
        print(f"Final Score: {final_score:.2f}")

        results.append(final_score)

    avg_score = sum(results) / len(results)
    print("\nFinal Average Score:", avg_score)

    if avg_score < settings.EVAL_THRESHOLD:
        raise Exception("❌ Evaluation failed (CI gate)")
    else:
        print("✅ Evaluation passed")

    return avg_score


if __name__ == "__main__":
    evaluate()