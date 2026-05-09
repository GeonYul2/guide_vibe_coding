# Workflow: Weekly GitHub Technique Repository Radar

Purpose: keep this guide current by discovering hot GitHub repositories that contain reusable agent-engineering techniques.

This is a **maintainer-only** refresh loop. Ordinary clone users do not need to run it to design an automation agent. YouTube videos, articles, talks, and release notes are supplemental source-ingestion inputs handled by `workflows/source-ingestion.md`.

## Implemented Automation

This repo keeps GitHub Actions as a manual maintainer trigger only:

- Workflow: `.github/workflows/weekly-repo-radar.yml`
- Manual trigger: `workflow_dispatch`
- Script: `maintainer/scripts/weekly_repo_radar.py`
- Config: `maintainer/radar-config.yaml`
- Output:
  - `maintainer/radar/YYYY-MM-DD.md`
  - `maintainer/radar/YYYY-MM-DD-candidates.yaml`
- Review model: create a pull request for human review

This workflow does not run on clone, push, pull request, or a timer. It runs only when a maintainer manually starts `workflow_dispatch`.

## What Counts as a Candidate

Prioritize repositories that teach or implement reusable techniques, such as:

- agent harnesses and runtime loops
- eval, benchmark, regression, and test harness systems
- failed-case memory and feedback loops
- context engineering, compression, deduplication, and caching
- structured output, schema validation, parser/repair, and contract testing
- observability, tracing, telemetry, monitoring, and cost tracking
- MCP, tool registries, permission systems, and sandboxing
- prompt/version/workflow discipline
- memory, RAG, retrieval governance, and state patterns
- model routing, fallback, latency, and budget-control systems
- security, privacy, PII redaction, and data-governance patterns
- deployment, canary, rollout, rollback, and kill-switch patterns
- safety, handoff, policy, guardrail, and tripwire implementations
- concise operating-contract examples for coding agents

Deprioritize domain-specific demo apps unless they clearly expose reusable agent-engineering patterns.

## Guardrails

- Do not vendor external repositories.
- Do not auto-promote candidates into `repos/registry.yaml`.
- Do not auto-add mandatory techniques without human review.
- The manual job only creates review artifacts and opens a PR.

## Discovery Sources

The implementation uses GitHub Search API queries configured in `maintainer/radar-config.yaml`.

Candidate signals:

- recent commits/releases
- stars and forks
- star delta versus the previous generated radar when available
- issue/PR activity proxy via open issues
- technique keyword score
- relevance to automation agents
- license metadata
- language/topics/description match

## Classification Tags

Use tags such as:

- agent-framework
- evals
- harness
- caching
- observability
- telemetry
- structured-output
- schema-validation
- guardrails
- tripwires
- memory
- retrieval-governance
- model-routing
- security-privacy
- rollout-canary
- tool-use
- prompt-engineering
- workflow-orchestration
- browser-automation
- code-agent
- safety

## 처음 시작하는 사람용 프롬프트

레이더 문서를 처음 보는 사람은 아래 프롬프트로 시작합니다. 핵심은 후보 저장소를 바로 설치하지 않고, 가상의 작은 프로젝트에 테크닉 1개만 안전하게 적용해보는 것입니다.

```md
나는 바이브코딩/에이전트 개발을 처음 시작하는 사람이다.
이 레이더 문서의 상위 후보 중에서 내 가상 프로젝트에 적용해볼 만한 테크닉 1개만 골라줘.

가상 프로젝트:
- 개인 TODO 앱을 만드는 작은 TypeScript/Node.js 저장소
- 목표: AI 코딩 에이전트가 안전하게 작업하고 테스트까지 확인하게 만들기
- 금지: 외부 저장소 설치, production 배포, registry 수정, 대량 리팩터링

원하는 답변:
1. 선택한 후보와 선택 이유
2. 왜 다른 후보들은 지금은 보류하는지
3. 30분 안에 할 수 있는 첫 실습 단계
4. 성공 여부를 확인할 테스트/체크리스트
5. 위험하거나 사람이 승인해야 하는 작업

확신이 없으면 구현하지 말고 질문 1개만 해줘.
```

정확도 체크 기준:

- 후보를 1개만 골랐는가
- 외부 저장소 설치, production 배포, registry 수정이 차단됐는가
- 첫 실습 단계가 30분 안에 가능한가
- 테스트/체크리스트가 명확한가
- 위험 작업과 사람 승인 경계가 드러나는가
- 임시 실습 파일을 만들었다면 검증 후 삭제할 수 있는가

## Weekly Review Procedure

1. Review the generated PR.
2. Open `maintainer/radar/YYYY-MM-DD.md` for the ranked overview.
3. Open `maintainer/radar/YYYY-MM-DD-candidates.yaml` for structured metadata.
4. For promising candidates, inspect the source repository manually.
5. Choose one status:
   - `rejected` — not useful, not reusable, or too risky
   - `watch` — revisit later
   - `candidate` — promising but not adopted
   - `adopted` — add to `repos/registry.yaml`
6. If a repository reveals a reusable technique, add the technique to `techniques/registry.yaml` with source refs.
7. If it should become mandatory for all agent tasks, update:
   - `agent-playbook.yaml`
   - `templates/technique-selection.yaml`
   - any required artifact template under `templates/`
   - `techniques/taxonomy.yaml`
   - `scripts/test_agent_guide.py`

## Adoption Output

Update `repos/registry.yaml` only after review:

```yaml
- name:
  url:
  tags: []
  status: candidate|watch|adopted|rejected
  last_checked: YYYY-MM-DD
  update_cadence: weekly|monthly|manual
  why_it_matters:
  local_application:
  risks:
  next_review:
```
