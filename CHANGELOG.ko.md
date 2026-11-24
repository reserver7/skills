# 변경 로그 — Grounded

[English](CHANGELOG.md) | **한국어**

이 문서는 PR 제목만으로 알기 어려운 중요한 설계 결정, 호환성·마이그레이션 안내, 측정 결과를 기록합니다. 일반 변경은 자동 생성 GitHub Release 노트에 있으므로 반복 기록하지 않습니다. 형식은 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), 버전은 [Semantic Versioning](https://semver.org/spec/v2.0.0.html)을 따릅니다. 정식 플러그인 버전은 [`grounded/plugin.json`](grounded/plugin.json)에 있고 Git 태그 형식은 `skills-v<version>`입니다.

## [미출시]

### 변경

- 스킬 선택과 역할을 미리 알리고, 경로 변경 시 추가 스킬을 알리는 규칙을 참고 가이드에서 공통 정책으로 올렸습니다. 안내는 승인을 기다리지 않습니다.

## [0.6.0] — 2026-11-24

### 추가

- 작업에 따라 선택하는 CLI-Hub 검색 및 CLI-Anything 하네스를 Grounded setup에서 관리합니다. CLI 설치 전 사용자의 승인을 요구합니다.
- 개인 포트폴리오 레퍼런스 조사에만 명시적으로 사용하는 Craft Anything 워크플로를 추가했습니다. 공식 플랫폼 CLI는 setup이 관리하고 SHA-256으로 확인합니다.
- Anthropic `frontend-design`과 Vercel React 모범 사례·컴포지션 스킬을 추가했습니다. 별도 LICENSE 파일이 없는 저장소는 upstream의 명시적 MIT 선언을 확인합니다.
- 패키지, 적용된 호스트 정책, 설치된 의존성 리비전을 조회하는 전역 `grounded -v` 명령을 추가했습니다.
- 주요 가이드, 변경 로그, 검증 기록을 한국어와 영어로 제공합니다.

### 변경

- 공통 스킬 선택, 승인, 버전별 Context7 fallback, 릴리스 규칙을 다듬고 setup 정책 테스트에 반영했습니다.
- Grounded 관리 스킬 소스로 이전한 뒤 일회성 레거시 보관·비호환 목록을 제거했습니다.

## [0.5.0] — 2026-11-19

### 추가

- Playwright CLI와 Chromium 기반 관리형 웹 QA, Vercel UI 및 접근성 가이드라인.
- 네이티브 Codex·Claude 플러그인의 브라우저 OAuth 기반 Context7 문서 조회와 MCP 서버 개발용 Anthropic 원본 `mcp-builder` 스킬.
- Addy의 API 설계, CI/CD, 관측성, 성능, 보안 안내. ECC의 DB 마이그레이션, MySQL, 점진적 배포, 문서 업데이트, 읽기 전용 문서 감사. 승인된 트래커 게시에 맞춘 Matt Pocock 티켓 워크플로.

### 워크플로 및 업그레이드

- 플러그인 업데이트 후 Grounded setup을 다시 실행합니다. setup은 안정 릴리스와 Vercel UI 규칙, ECC 문서 거버넌스, Anthropic MCP Builder의 기본 브랜치 예외 리비전을 기록합니다.
- Superpowers v7 스킬 15개를 모두 제공합니다. 전체 워크플로는 필요할 때 명시적으로 선택합니다. setup은 시작 훅을 설치하지 않습니다. OpenSpec과 Superpowers를 전환할 때 활성 구현 계획 하나를 유지합니다.
- PRD 요구사항은 OpenSpec 제안서와 연결된 사양에 기록합니다. 요청받은 문서 업데이트와 릴리스 노트에는 ECC `doc-updater`를 사용하고, 별도 감사에는 `docs-governance`를 사용합니다.

## [0.4.0] — 2026-11-05

### 변경

- setup은 안정적인 최신 OpenSpec npm dist-tag와 Superpowers/Ponytail GitHub 릴리스를 조회하고 패키지 무결성 또는 커밋 SHA를 확인해 선택 버전을 기록합니다. 복원은 저장된 영수증과 캐시를 사용하며 새 버전을 조회하지 않습니다.
- `restore` 및 `uninstall` 관리자 명령을 추가했습니다. 편집된 관리 파일은 보존하고 소유자 전용 백업을 유지합니다. 복구가 끝나지 않으면 보류 기록을 남기고 영향을 받은 경로를 알립니다.
- CI는 기존 검증 모음과 `manage.py check`를 유지합니다. Actions는 전체 커밋 SHA로 고정하고 Dependabot 주간 갱신을 사용합니다. 릴리스 분류 PR 라벨은 수동입니다.

setup은 로컬 영수증과 불변 아티팩트 식별자로 재현성을 유지하면서 최신 upstream을 우선합니다. 호스트 상태를 변경하기 전에 후보를 조회합니다. 이전 성공 환경을 복원하거나 변경되지 않은 Grounded 관리 파일을 제거할 수 있으며, 편집된 내용은 남기고 소유자 전용 백업을 유지합니다. Codex CLI에는 오프라인 버전 선택 복원 기능이 없으므로 Codex 마켓플레이스 복원은 설정된 마켓플레이스에 연결할 수 있습니다.

일반 저장소 정비와 릴리스 자동화 변경은 생성된 GitHub Release 노트에 기록합니다. PR 제목만으로 알 수 없는 지속적인 결정 맥락, 호환성·마이그레이션 안내, 측정 근거를 여기에 남깁니다.

## [0.3.0] — 2026-10-16

이 릴리스에서 한 단계 Grounded 환경 설정을 추가하고 Codex 설치를 저장소의 커스텀 마켓플레이스로 옮겼습니다.

### 추가

- 고정된 공통 스킬 설치, 관리형 호스트 규칙 적용, 복구 가능한 백업을 제공하는 setup 진입점.
- Codex 마켓플레이스 설치 안내와 플러그인 패키지.

## [0.2.0] — 2026-10-15

네이티브 Codex 및 Claude 플러그인 설치를 준비하고 스킬과 공통 규칙 설정을 하나의 저장소로 통합했습니다.

### 추가

- Codex 및 Claude Code용 네이티브 플러그인 디렉터리 패키지.
- 공통 규칙 설정과 초기 브랜치·릴리스 절차.

## [0.1.0] — 2026-10-15

공개 저장소의 최초 릴리스.
