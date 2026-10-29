
from pathlib import Path
import re


def tokenize(text: str) -> set[str]:
    """텍스트를 소문자로 바꾸고 단어 단위로 나눈다."""
    return set(re.findall(r"[a-zA-Z0-9가-힣]+", text.lower()))


def load_documents(path: Path) -> list[str]:
    """마크다운 문서를 ## 제목 기준으로 나눈다."""
    text = path.read_text(encoding="utf-8")
    sections = re.split(r"(?m)^## ", text)

    # 첫 번째 부분은 문서 전체 제목이므로 제외한다.
    documents = [
        section.strip()
        for section in sections[1:]
        if section.strip()
    ]
    return documents


def search(query: str, documents: list[str]) -> list[tuple[int, int, str]]:
    """질문과 겹치는 단어 수를 세어 관련 문서를 정렬한다."""
    query_tokens = tokenize(query)
    results = []

    for index, document in enumerate(documents, start=1):
        document_tokens = tokenize(document)
        score = len(query_tokens & document_tokens)

        if score > 0:
            results.append((index, score, document))

    results.sort(key=lambda item: item[1], reverse=True)
    return results


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    document_path = project_root / "data" / "sample_docs.md"
    documents = load_documents(document_path)

    print("문서 검색기")
    print("종료하려면 q를 입력하세요.")

    while True:
        query = input("\n질문: ").strip()

        if query.lower() == "q":
            break

        results = search(query, documents)

        if not results:
            print("일치하는 단어가 있는 문서를 찾지 못했습니다.")
            continue

        for index, score, document in results:
            print(f"\n[문서 {index}] 겹치는 단어 수: {score}")
            print(document)


if __name__ == "__main__":
    main()
