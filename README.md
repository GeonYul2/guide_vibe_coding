# Agent Engineering Guide

이 레포는 사람이 읽는 자료 모음이 아니라, **에이전트가 읽고 바로 실행할 수 있는 자동화 에이전트 제작 가이드/강제 레이어**입니다.

기본 사용자 경로는 **새 자동화 에이전트 task를 설계하고 검증하는 것**입니다. GitHub technique radar 같은 업데이트 도구는 일반 클론 사용자에게 필요 없는 maintainer 전용 기능으로 `maintainer/`에 분리되어 있습니다.

팀원이 새 자동화 에이전트를 만들 때 이 레포를 컨텍스트로 불러오면, 에이전트는 다음을 반드시 수행해야 합니다.

1. `wiki/index.md`가 있으면 먼저 읽어 토큰을 아끼는 경로를 잡고, 중요한 결정은 원본 파일에서 검증한다.
2. 표준 `intake-form.md`로 첫 입력 품질을 맞추되, 사용자가 한 번에 양식을 채우게 하지 않고 질문-답변으로 한 항목씩 이어간다.
3. 적용할 Agent Engineering technique을 `wiki/technique-map.md`와 `techniques/taxonomy.yaml`로 좁힌 뒤, `techniques/registry.yaml`의 모든 technique을 선택/거절한다.
4. 구현 전에 PRD, output schema, eval spec, guardrails, tool contract, retrieval/memory, failure memory, token-efficiency hard gate, cost/caching/model-routing, telemetry, security/privacy, release/rollout plan을 만든다.
5. 외부 GitHub 레포는 통째로 vendoring하지 않고 `repos/registry.yaml`에 링크/메타데이터/적용 포인트만 기록한다.
6. 구현 후 실패 케이스를 회귀 테스트와 failure memory로 남긴다.
7. 토큰 사용량을 비용으로 보고 `cost-and-caching.md`에 max token, cache hit target, pruning rule, fallback, token telemetry를 명시한다.
8. 구현 준비도를 `readiness-scorecard.md`로 점수화하고 부족한 항목을 표시한다.
9. 검증 evidence 없이는 완료를 선언하지 않는다.
10. 자세한 설명 요청이 없으면 기본 응답은 1~2문장으로 제한한다.

## 사용자 시작 방식

일반 사용자는 스크립트 이름부터 외울 필요가 없습니다. 이 레포를 코딩 에이전트의 작업 폴더로 열고, 아래처럼 자연어로 시작하면 됩니다.

```text
고객 문의 메일을 읽고 답장 초안을 만들어주는 에이전트를 만들고 싶어.
```

그러면 에이전트는 먼저 아래 한 문장으로 시작한 뒤, 한 번에 한 질문씩 필요한 정보를 모읍니다.

```text
토큰 절감모드로 시작할까요?
```

대화가 진행되면 에이전트가 `tasks/<task-slug>/` 아래에 intake, PRD, eval, guardrails, tool contract 같은 산출물을 만들고, 필요할 때 아래 검증을 실행합니다.

```bash
python3 scripts/validate_agent_task.py tasks/<task-slug>
```

일반 사용자의 기본 경로는 “자연어 요청 → 한 질문씩 인터뷰 → 산출물 생성 → validator 검증”입니다. technique 업데이트, GitHub radar, 후보 점수화는 `maintainer/README.md`를 볼 때만 실행합니다.

## 사용자 배포본 분리

이 레포는 **source/maintainer 레포**로 유지하고, 일반 사용자에게는 manifest 기반 subset만 배포합니다.

```bash
python3 maintainer/scripts/export_user_distribution.py \
  --dest /path/to/user-distribution-checkout \
  --prune-excluded \
  --prune-stale
```

- 배포 기준: `distribution/user-export-manifest.yaml`
- 사용자용 override: `distribution/user/`
- publish 절차: `maintainer/workflows/publish-user-distribution.md`
- 수동 PR workflow: `.github/workflows/publish-user-distribution.yml`

사용자 배포본에는 `maintainer/`, GitHub radar workflow, maintainer용 전체 generated wiki, `.omx/`, `.obsidian/`, maintainer test/publish 로직이 포함되지 않습니다.
사용자 배포본에는 대신 `distribution/user/wiki/`에서 관리되는 **curated user wiki**가 `wiki/`로 포함됩니다. 이 wiki는 사용자가 클론했을 때 에이전트가 전체 문서를 한꺼번에 읽지 않고, technique 선택과 작업 흐름을 빠르게 좁히기 위한 토큰 절약용 지도입니다.


## LLM Wiki / Obsidian

이 maintainer/source 레포는 원본 실행 계약을 그대로 유지하면서 `wiki/`를 전체 LLM Wiki 탐색 레이어로 생성합니다. Obsidian으로 보려면 **레포 루트 폴더**를 vault로 열면 됩니다.

```bash
python3 scripts/generate_llm_wiki.py
```

- 시작점: `wiki/index.md`
- 관계 보기: `wiki/graph-links.md`
- Obsidian 설정: `.obsidian/graph.json`
- 주의: `wiki/`는 탐색/시각화/요약 레이어이며, 최종 근거는 항상 `AGENTS.md`, `agent-playbook.yaml`, `techniques/*.yaml`, `workflows/*.md`, `templates/*`, `tasks/*`에서 검증합니다. Maintainer 작업은 `maintainer/*` 원본을 따로 확인합니다.

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
- `workflows/intake.md` — 새 작업의 첫 입력 품질을 표준화하는 접수 흐름
- `workflows/build-agent.md` — 새 자동화 에이전트 제작 표준 흐름
- `workflows/deep-interview.md` — 요구사항 정제 인터뷰 프로토콜
- `workflows/source-ingestion.md` — 영상/글/강연에서 기법을 안전하게 추출하는 보조 프로세스
- `sources/registry.yaml` — 영상/문서/외부 글 같은 source metadata
- `templates/` — 작업별 산출물 템플릿, including `intake-form.md` and `readiness-scorecard.md`
- `repos/registry.yaml` — 외부 레포 링크/요약/업데이트 추적 레지스트리
- `scripts/` — 작업 스캐폴드/검증 스크립트
- `maintainer/` — 선택적 technique 업데이트/radar 도구와 maintainer-only 작업
- `SECURITY.md` — 회사 레포 클론/CI 활성화 시 보안 경계와 체크리스트

## 강제성의 한계와 보강 장치

LLM은 이 레포가 컨텍스트에 로드되지 않으면 규칙을 따를 수 없습니다. 따라서 강제성은 다음 장치로 확보합니다.

- 루트 `AGENTS.md`에 필수 게이트 선언
- `agent-playbook.yaml`에 기계 판독 가능한 필수 산출물 선언
- `scripts/validate_agent_task.py`로 산출물 존재/핵심 섹션 검증
- CI에서 task artifact 검증
- 모든 외부 레포는 복사하지 않고 registry로 추적

## Maintainer 전용 업데이트 루프

playbook 자체를 갱신하는 관리자는 선택적으로 아래를 실행합니다:

```bash
python3 maintainer/scripts/weekly_repo_radar.py --date "$(date -u +%F)" --limit 10
```

- 설정: `maintainer/radar-config.yaml`
- 결과: `maintainer/radar/`
- 절차: `maintainer/workflows/weekly-repo-radar.md`
- 후보는 자동 채택하지 않고 사람이 검토한 뒤 `repos/registry.yaml` 또는 `techniques/registry.yaml`로 승격합니다.
