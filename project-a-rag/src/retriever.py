
from pathlib import Path
import re



def tokenize(text: str) -> set[str]:
    """한국어 조사와 일부 어미를 제거해 핵심 단어를 추출한다."""
    words = re.findall(r"[a-zA-Z0-9가-힣]+", text.lower())

    stopwords = {"루미", "어떻게", "어때", "오늘", "서울"}
    suffixes = (
        "되면", "한다", "하는", "해서", "하면",
        "으로", "에서", "에게",
        "은", "는", "이", "가", "을", "를",
        "의", "에", "와", "과", "도", "만", "로", "다", "해",
    )

    tokens = set()

    for word in words:
        for suffix in suffixes:
            if len(word) > len(suffix) + 1 and word.endswith(suffix):
                word = word[:-len(suffix)]
                break

        if word and word not in stopwords:
            tokens.add(word)

    return tokens



def load_documents(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    sections = re.split(r"(?m)^## ", text)

    return [
        section.strip()
        for section in sections[1:]
        if section.strip()
    ]


def search(query: str, documents: list[str]) -> list[tuple[int, int, str]]:
    query_tokens = tokenize(query)
    results = []

    for index, document in enumerate(documents, start=1):
        document_tokens = tokenize(document)
        score = len(query_tokens & document_tokens)

        if score > 0:
            results.append((index, score, document))

    results.sort(key=lambda item: item[1], reverse=True)
    return results


def generate_answer(document: str) -> str:
    # 현재는 생성형 AI 대신 검색된 문서 내용을 그대로 사용한다.
    lines = document.splitlines()
    content = " ".join(line.strip() for line in lines[1:] if line.strip())
    return content


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    document_path = project_root / "data" / "sample_docs.md"
    documents = load_documents(document_path)

    print("루미 문서 도우미")
    print("종료하려면 q를 입력하세요.")

    while True:
        query = input("\n질문: ").strip()

        if query.lower() == "q":
            break

        results = search(query, documents)

        if not results:
            print("관련 근거를 찾지 못해 답변할 수 없습니다.")
            continue

        print("\n검색 결과 상위 3개:")

        for index, score, document in results[:3]:
            title = document.splitlines()[0]
            print(f"- 문서 {index} | 점수 {score} | {title}")


if __name__ == "__main__":
    main()
