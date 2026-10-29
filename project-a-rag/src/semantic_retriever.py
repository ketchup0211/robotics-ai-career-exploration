
from pathlib import Path
import re

from sentence_transformers import SentenceTransformer, util


MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def load_documents(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    sections = re.split(r"(?m)^## ", text)

    return [
        section.strip()
        for section in sections[1:]
        if section.strip()
    ]


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    document_path = project_root / "data" / "sample_docs.md"

    documents = load_documents(document_path)

    print("임베딩 모델을 불러오는 중입니다...")
    model = SentenceTransformer(MODEL_NAME)

    document_embeddings = model.encode(
        documents,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )

    print("루미 의미 기반 검색기")
    print("종료하려면 q를 입력하세요.")

    while True:
        query = input("\n질문: ").strip()

        if query.lower() == "q":
            break

        if not query:
            continue

        query_embedding = model.encode(
            query,
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

        scores = util.cos_sim(
            query_embedding,
            document_embeddings,
        )[0]

        top_results = scores.topk(
            k=min(3, len(documents))
        )

        print("\n검색 결과 상위 3개:")

        for index, score in zip(
            top_results.indices.tolist(),
            top_results.values.tolist(),
        ):
            title = documents[index].splitlines()[0]
            print(
                f"- 문서 {index + 1} | "
                f"유사도 {score:.3f} | {title}"
            )


if __name__ == "__main__":
    main()
