# Project A. RAG-based Document Q&A

## Goal

문서에 담긴 정보를 바탕으로 질문에 답하는 질의응답 시스템을 구현하고, 검색 결과의 관련성과 답변의 근거 충실도를 실험으로 확인합니다.

이 프로젝트의 핵심은 처음부터 복잡한 시스템을 만드는 것이 아니라, 최소 기능을 구현한 뒤 실패 사례를 분석하고 개선하는 과정에 있습니다.

## Scope

### Initial MVP

1. 작은 문서 모음 준비
2. 문서를 검색 가능한 단위(chunk)로 나누기
3. 질문과 관련된 문서 조각 검색하기
4. 검색된 근거를 바탕으로 답변 생성하기
5. 답변과 근거를 함께 표시하기

### Evaluation Questions

- 질문과 관련된 문서 조각이 검색되는가?
- 검색된 근거만으로 답변을 뒷받침할 수 있는가?
- 문서에 답이 없을 때 모른다고 답하는가?
- 문서 표현과 질문 표현이 달라져도 관련 정보를 찾는가?
- 검색 방식이나 프롬프트를 바꾸면 결과가 어떻게 달라지는가?

## Planned Experiments

| Experiment | Question |
| --- | --- |
| EXP-01: Baseline retrieval | 기본 키워드 검색은 질문과 관련된 문서를 찾는가? |
| EXP-02: Query wording and retrieval failures | 질문 표현에 따라 검색 결과가 어떻게 달라지는가? |
| EXP-03: Rule-based Korean normalization | 조사·어미 정규화가 검색 결과를 개선하는가? |
| EXP-04: Query paraphrase robustness | 의미가 비슷하지만 표현이 다른 질문도 검색할 수 있는가? |
| EXP-05: Keyword vs. semantic retrieval | 키워드 기반 검색과 의미 기반 검색은 어떤 차이가 있는가? |
| EXP-06: Grounded answers | 답변이 검색 근거를 벗어나지 않도록 할 수 있는가? |
| EXP-07: No-answer questions | 근거가 없는 질문을 적절히 거절하는가? |

실험 순서는 구현 난이도와 실제 관찰 결과에 따라 조정할 수 있습니다.

## Technology Plan

초기에는 Python으로 작게 구현합니다. 먼저 실행 가능한 단순한 기준선을 만들고, 이후 필요에 따라 키워드 검색과 의미 기반 검색을 비교합니다. 답변 생성에 외부 LLM API를 연결할 때는 API 키와 사용 비용을 확인하고, 비밀 키를 저장소에 커밋하지 않습니다.

## Record-Keeping

각 실험은 `experiments/experiment-log.md`에 기록합니다. ChatGPT가 제안한 가설과 직접 실행해 확인한 결과를 구분하며, 아직 실행하지 않은 실험은 결과가 있는 것처럼 작성하지 않습니다.

## Current Status

- [x] Project scope and initial evaluation questions defined
- [x] Development environment confirmed
- [x] Minimal document set prepared
- [x] First retrieval baseline implemented
- [x] EXP-01 baseline retrieval implemented and tested
- [x] EXP-02 query wording and retrieval failures tested
- [x] EXP-03 rule-based Korean normalization tested
- [x] EXP-04 query paraphrase robustness tested
- [ ] Compare keyword-based retrieval with semantic retrieval
