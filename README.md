# Agent Engineering Guide

이 레포는 사람이 읽는 자료 모음이 아니라, **에이전트가 읽고 바로 실행할 수 있는 자동화 에이전트 제작 가이드/강제 레이어**입니다.

기본 업데이트 루프는 **GitHub-first hot technique repository radar**입니다. YouTube/글/강연은 새로운 기법을 보충 설명하거나 seed로 넣는 보조 경로입니다.

팀원이 새 자동화 에이전트를 만들 때 이 레포를 컨텍스트로 불러오면, 에이전트는 다음을 반드시 수행해야 합니다.

1. Deep Interview로 목적/범위/비목표/성공기준을 정리한다.
2. 적용할 Agent Engineering technique을 `techniques/registry.yaml`에서 선택한다.
3. 구현 전에 PRD, output schema, eval spec, guardrails, tool contract, retrieval/memory, failure memory, token-efficiency hard gate, cost/caching/model-routing, telemetry, security/privacy, release/rollout plan을 만든다.
4. 외부 GitHub 레포는 통째로 vendoring하지 않고 `repos/registry.yaml`에 링크/메타데이터/적용 포인트만 기록한다.
5. 구현 후 실패 케이스를 회귀 테스트와 failure memory로 남긴다.
6. 토큰 사용량을 비용으로 보고 `cost-and-caching.md`에 max token, cache hit target, pruning rule, fallback, token telemetry를 명시한다.
7. 구현 준비도를 `readiness-scorecard.md`로 점수화하고 부족한 항목을 표시한다.
8. 검증 evidence 없이는 완료를 선언하지 않는다.
9. 자세한 설명 요청이 없으면 기본 응답은 1~2문장으로 제한한다.

## 빠른 사용법

새 에이전트 작업 폴더 생성:

```bash
python3 scripts/new_agent_task.py "internal-doc-report-agent"
```

필수 산출물 검증:

```bash
python3 scripts/validate_agent_task.py tasks/internal-doc-report-agent
```

주간 GitHub technique repo 레이더 수동 실행:

```bash
python3 scripts/weekly_repo_radar.py --date "$(date -u +%F)" --limit 10
```

GitHub Actions 자동 실행:

- `.github/workflows/weekly-repo-radar.yml`
- 매주 월요일 00:00 UTC / 09:00 KST
- GitHub Search API로 agent-engineering technique repo 후보를 찾습니다.
- 결과를 `repos/radar/`에 생성하고 review PR을 엽니다.
- 후보를 바로 채택하지 않고 사람이 `repos/registry.yaml`로 승격합니다.
- YouTube/글/강연 source는 `sources/registry.yaml`에 보조 자료로 등록합니다.

## 현재 큰 카테고리

- Intake, Scope, and Readiness
- Agent Operating Contracts
- Schemas and Structured Outputs
- Harness and Runtime Design
- Quality, Evals, and Regression
- Context, Cost, Caching, and Memory
- Observability, Telemetry, and Operations
- Safety, Security, Approval, and Governance
- Discovery and Update Loop

## 핵심 파일

- `AGENTS.md` — 에이전트가 따라야 하는 최상위 실행 계약
- `agent-playbook.yaml` — 강제 게이트와 필수 산출물의 기계 판독용 정의
- `techniques/registry.yaml` — 적용 가능한 에이전트 엔지니어링 기법 목록
- `techniques/taxonomy.yaml` — 기법 카테고리와 에이전트 맥락별 추천 체계
- `workflows/build-agent.md` — 새 자동화 에이전트 제작 표준 흐름
- `workflows/deep-interview.md` — 요구사항 정제 인터뷰 프로토콜
- `workflows/weekly-repo-radar.md` — 주간 GitHub hot technique repo 탐지/요약/채택 프로세스
- `workflows/source-ingestion.md` — 영상/글/강연에서 기법을 안전하게 추출하는 보조 프로세스
- `sources/registry.yaml` — 영상/문서/외부 글 같은 source metadata
- `templates/` — 작업별 산출물 템플릿, including `readiness-scorecard.md`
- `repos/registry.yaml` — 외부 레포 링크/요약/업데이트 추적 레지스트리
- `scripts/` — 작업 스캐폴드/검증 스크립트
- `SECURITY.md` — 회사 레포 클론/CI 활성화 시 보안 경계와 체크리스트

## 강제성의 한계와 보강 장치

LLM은 이 레포가 컨텍스트에 로드되지 않으면 규칙을 따를 수 없습니다. 따라서 강제성은 다음 장치로 확보합니다.

- 루트 `AGENTS.md`에 필수 게이트 선언
- `agent-playbook.yaml`에 기계 판독 가능한 필수 산출물 선언
- `scripts/validate_agent_task.py`로 산출물 존재/핵심 섹션 검증
- CI에서 task artifact 검증
- GitHub hot technique repo radar를 주 1회 자동 실행
- 모든 외부 레포는 복사하지 않고 registry로 추적
