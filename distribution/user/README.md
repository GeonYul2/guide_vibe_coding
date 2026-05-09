# Agent Engineering Guide — User Distribution

이 레포는 **자동화 에이전트를 설계·검증하기 위한 사용자용 helper 배포본**입니다. Maintainer 전용 GitHub radar, technique discovery, publish workflow, generated wiki는 포함하지 않습니다.

## 빠른 사용법

```bash
python3 scripts/new_agent_task.py "internal-doc-report-agent"
python3 scripts/validate_agent_task.py tasks/internal-doc-report-agent
```

에이전트는 `AGENTS.md`, `agent-playbook.yaml`, `workflows/build-agent.md`, `techniques/registry.yaml`, `techniques/taxonomy.yaml`, `templates/`를 기준으로 작업합니다.

## 사용자 경계

- 새 작업은 `tasks/<task-slug>/intake-form.md`부터 작성합니다.
- 구현 전 필수 산출물을 모두 채우고 validator를 통과해야 합니다.
- 이 배포본은 GitHub technique radar를 실행하지 않습니다.
- technique 업데이트/레이더/배포 publish는 source/maintainer 레포에서만 관리합니다.

## 핵심 파일

- `AGENTS.md` — 사용자 배포본용 에이전트 실행 계약
- `agent-playbook.yaml` — 필수 산출물과 게이트의 기계 판독 정의
- `workflows/` — intake, deep interview, build-agent 흐름
- `templates/` — task 산출물 템플릿
- `techniques/` — 선택/거절해야 하는 agent-engineering technique registry
- `scripts/new_agent_task.py` — task scaffold 생성
- `scripts/validate_agent_task.py` — readiness/completion artifact 검증

## 보안 경계

이 배포본은 표준 라이브러리 Python 스크립트와 Markdown/YAML만 포함합니다. GitHub Actions, maintainer radar, 외부 저장소 clone/install/execute 로직은 포함하지 않습니다.
