# Grounded

[English](README.md) | **한국어**

[![최신 릴리스](https://img.shields.io/github/v/release/reserver7/skills?filter=skills-v%2A&sort=semver)](https://github.com/reserver7/skills/releases/latest)

Grounded는 Codex와 Claude Code를 위한 통합 엔지니어링 환경입니다. 각 호스트에서 setup을 한 번 실행하면 관리 대상 스킬과 공통 개발 규칙을 설치합니다. 작업에 맞는 스킬만 사용합니다.

- **계획 및 구현:** 지속적으로 관리할 요구사항에는 OpenSpec, 작은 범위의 구현에는 Ponytail, 디버깅·TDD·코드 리뷰·완료 검증에는 Superpowers를 사용합니다. Superpowers의 15개 스킬을 모두 제공하며, 전체 계획·실행 워크플로는 요청이 있을 때 선택합니다.
- **디자인·검증·배포:** `frontend-design`은 UI 제작, `web-design-guidelines`는 별도의 UI·접근성 검토에 사용합니다. React/Next 작업에는 Vercel의 프레임워크 가이드를 적용하고, 성능 조사는 측정 기준을 정한 뒤 Addy 스킬을 사용합니다. 브라우저 QA에는 관리형 도구를 사용합니다.
- **문서 및 연동:** 문서와 릴리스 노트는 `doc-updater`, 별도 문서 감사는 `docs-governance`, 트래커 이슈 준비는 `to-tickets`를 사용합니다. 네이티브 플러그인은 Context7 OAuth 연결을 제공합니다. MCP 서버는 `mcp-builder`, 기존 앱 CLI 탐색은 CLI-Hub, 적합한 CLI가 없을 때만 CLI-Anything을 사용합니다. Craft Anything은 권한이 있는 포트폴리오 레퍼런스 작업에서 명시적으로 호출합니다.

[전체 스킬 목록](grounded/README.ko.md#스킬-및-도구)과 [Codex·Claude 호출 가이드](grounded/docs/workflow.md#skill-calls)를 확인하세요.

## 빠른 시작

Grounded는 macOS 또는 Linux, Python 3.11+, Git, Node.js 20.19+, npm이 필요합니다. setup을 실행하기 전에 Codex 또는 Claude Code를 설치하고 인증하세요. 자세한 내용은 [설치 안내](grounded/README.ko.md#빠른-시작)를 참고하세요.

### Codex

컴퓨터마다 마켓플레이스를 추가하고 Grounded를 한 번 설치합니다.

```sh
codex plugin marketplace add reserver7/skills --ref main
codex plugin add grounded@grounded
```

새 Codex 대화를 시작하고 `$grounded:setup`을 실행합니다.

### Claude Code

저장소를 한 번 복제한 뒤 프로젝트에서 Grounded 플러그인을 불러옵니다.

```sh
git clone https://github.com/reserver7/skills.git ~/grounded-skills
cd /path/to/your/project
claude --plugin-dir ~/grounded-skills/grounded
```

Claude Code에서 `/grounded:setup`을 실행합니다.

setup 후 새 대화를 시작해 공통 규칙을 불러오세요. 기술 문서를 조회하려면 호스트의 MCP 연결 설정에서 Grounded의 Context7 서버를 연결하고 브라우저 OAuth를 완료합니다. [Context7 설정](grounded/README.ko.md#context7-기술-문서-조회)

## 업데이트 및 복원

PATH에 설치한 뒤 `grounded -v`를 실행하면 어느 디렉터리에서든 호스트 정책 버전과 기록된 의존성 리비전을 볼 수 있습니다. 설치 방법은 [버전 확인](grounded/README.ko.md#버전-확인)을 참고하세요.

- **Codex:** 마켓플레이스는 `main`을 추적합니다. 즉시 갱신하려면 `codex plugin marketplace upgrade grounded`를 실행하고, 새 대화를 시작한 뒤 `$grounded:setup`을 다시 실행합니다.
- **Claude Code:** `git -C ~/grounded-skills pull --ff-only`를 실행하고 같은 `--plugin-dir` 옵션으로 재시작한 뒤 `/grounded:setup`을 다시 실행합니다.

setup을 다시 실행할 때마다 최신 upstream 버전을 확인하고 설치 버전과 커밋을 로컬에 기록합니다. 중복된 관리 대상 스킬과 충돌하는 플러그인을 옮기거나 비활성화하기 전에 백업합니다. [의존성 정책](grounded/SOURCES.ko.md)과 [복원·삭제 안내](grounded/README.ko.md#로컬-설치-및-업데이트)를 참고하세요.

## 저장소 안내

| 문서 | 설명 |
|---|---|
| [Grounded 패키지](grounded/) | 스킬, 공통 규칙, 설치 도구 및 호스트 설정 |
| [워크플로 및 스킬 호출](grounded/docs/workflow.ko.md) | 작업별 책임, 스킬 호출, 계획 인계 |
| [소스 및 호환성 정책](grounded/SOURCES.ko.md) | 외부 소스, 버전 결정, 라이선스와 조정 사항 |
| [변경 로그](CHANGELOG.ko.md) | 릴리스 기록과 업그레이드 안내 |
| [기여 안내](CONTRIBUTING.ko.md) | Pull Request와 릴리스 절차 |

저장소는 [MIT 라이선스](LICENSE)를 따릅니다. 관리형 upstream 스킬은 [각 라이선스](grounded/SOURCES.ko.md)를 유지합니다.
