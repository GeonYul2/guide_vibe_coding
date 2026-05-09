# Agent Intake Form: github-technique-radar-agent

## Agent Idea

GitHub API 기반으로 에이전트 엔지니어링에 재사용 가능한 외부 저장소 후보를 주기적으로 찾고, 사람이 검토할 수 있는 Markdown/YAML 레이더 산출물을 만든다.

## Primary User

이 레포를 유지보수하는 에이전트 엔지니어, 바이브코딩 가이드 작성자, 그리고 새 테크닉을 안전하게 검토하려는 리뷰어가 사용한다.

## Workflow Pain

수동으로 GitHub 트렌드와 개별 저장소를 찾으면 검색어 편향, 누락, 후보 품질 편차가 크고, 금지된 크롤링 소스에 의존할 위험이 있다.

## Input

`maintainer/radar-config.yaml`의 정적/동적 검색 설정, GitHub Search API 응답, 이전 `maintainer/radar/*-candidates.yaml`의 star baseline, 로컬 technique registry와 taxonomy를 입력으로 사용한다.

## Output

`maintainer/radar/YYYY-MM-DD.md`와 `maintainer/radar/YYYY-MM-DD-candidates.yaml` 후보 보고서를 생성하고, 후보별 점수, 발견 출처, 토픽, 라이선스, 리뷰 이유를 기록한다.

## Allowed Actions

로컬 설정과 스크립트를 읽고, GitHub API에서 공개 저장소 메타데이터를 조회하며, `maintainer/radar/` 아래에 후보 산출물을 생성할 수 있다.

## Human Approval Required

후보를 `repos/registry.yaml`에 승격하거나 `techniques/registry.yaml`에 새 필수 테크닉을 추가하거나 GitHub Actions 권한과 배포 동작을 바꾸는 일은 사람 검토가 필요하다.

## Forbidden / Non-Goals

크롤링 금지 사이트를 직접 사용하지 않고, 외부 저장소를 vendoring하지 않으며, 후보를 자동 채택하거나 필수 테크닉으로 자동 승격하지 않는다.

## Success Examples

상위 후보에 agent harness, eval, context engineering, MCP, telemetry, guardrails 같은 재사용 가능한 레포가 포함된다. Rate limit 상황에서는 partial 상태와 안전한 오류 요약을 남긴다. 사람이 후보 파일만 보고 검토 우선순위를 정할 수 있다.

## Failure / Edge Cases

GitHub API rate limit, 빈 후보 결과, 도메인 데모 앱 과다 포함, 라이선스 누락, 비허용 URL 또는 토큰/개인정보가 오류 로그에 섞이는 상황을 안전하게 처리해야 한다.

## Tools / Data Access

허용 도구는 로컬 Python 스크립트, GitHub Search API, GitHub Actions 기본 토큰, 로컬 Markdown/YAML 파일이다. 외부 웹사이트 크롤링, 후보 저장소 코드 실행, 개인 토큰 기록은 금지된다.

## Evidence of Success

`python3 scripts/test_agent_guide.py`, `python3 scripts/validate_agent_task.py tasks/github-technique-radar-agent`, `python3 -m py_compile scripts/*.py`, 그리고 제한된 실제 GitHub API 스모크 결과로 검증한다.
