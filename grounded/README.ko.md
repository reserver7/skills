# Grounded

[English](README.md) | **한국어**

[![최신 릴리스](https://img.shields.io/github/v/release/reserver7/skills?filter=skills-v%2A&sort=semver)](https://github.com/reserver7/skills/releases/latest)

Codex와 Claude Code를 위한 개발 스킬 및 설치 도구 모음입니다.

요구사항을 합의하고 추적해야 할 때는 **OpenSpec**, 집중적인 기법이나 명시적으로 선택한 전체 워크플로에는 **Superpowers**를 사용합니다. **Ponytail**은 간결한 직접 수정에 선택적으로 활용하는 지침이며, 선택한 Superpowers 절차가 구현을 맡으면 Ponytail 없이 진행할 수 있습니다. 일반 CI/CD와 조건부 API·성능 작업에는 **Addy**, 복잡한 점진적 배포와 관련 데이터베이스 작업에는 **ECC**, Supabase나 PostgreSQL 작업에는 **Supabase Agent Skills**를 사용합니다. CEO 계획 검토, 엔지니어링 검토, ADR 작성, Jev 평가는 필요한 경우에만 선택합니다.

이 저장소는 upstream 리비전, 공통 규칙, 독립 스킬을 관리하여 같은 환경을 다른 컴퓨터에서도 구성합니다. Codex는 커스텀 마켓플레이스에서 Grounded를 설치합니다. Claude Code는 현재 로컬 클론을 `--plugin-dir`로 불러옵니다. Claude 마켓플레이스 배포는 추후 지원할 예정입니다. setup은 공통 정책을 적용하고 작업별 스킬을 사용할 수 있게 합니다.

## 스킬 및 도구

| 구성 | 스킬 또는 진입점 | 용도 |
|---|---|---|
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) | 호스트별 공식 CLI 워크플로 | 요구사항, 설계, 작업, 검증, 변경 이력 관리 |
| [Context7](https://github.com/upstash/context7/blob/master/docs/howto/oauth.mdx) | `resolve-library-id`, `query-docs` | 네이티브 플러그인의 원격 OAuth 연결을 통한 최신 기술 문서 조회 |
| [Anthropic Skills](https://github.com/anthropics/skills) | `mcp-builder`, `frontend-design` | MCP 서버 엔지니어링과 차별화된 시각적 UI 설계. UI·접근성 검토는 별도 스킬이 담당 |
| [CLI-Anything](https://github.com/HKUDS/CLI-Anything) | `cli-hub-meta-skill`, `cli-anything` | 기존 CLI를 먼저 탐색하고 적합한 CLI가 없을 때 하네스를 생성·개선합니다. 패키지 설치는 사용자 승인이 필요하며 Codex 생성기 연동은 upstream에서 실험적·커뮤니티 통합으로 표시합니다. |
| [Craft Anything](https://github.com/storytold/craft-anything) | `craft-anything` | 허가된 개인 포트폴리오 웹사이트·앱·게임 레퍼런스를 조사하고 재현하는 명시적 선택 기능. 초기 알파이며 setup이 공식 CLI를 Grounded 전용 캐시에 받고 SHA-256을 확인합니다. |
| [Superpowers](https://github.com/obra/superpowers) | v7 스킬 15개 전체 | 작업별 기법 5개와 선택형 워크플로·지원 스킬 10개 |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | `ponytail` | 기존 코드를 재사용하고 가장 작은 완결 변경을 구현 |
| [Supabase Agent Skills](https://github.com/supabase/agent-skills) | `supabase`, `supabase-postgres-best-practices` | Supabase 제품과 PostgreSQL 설계·보안·성능 지침 |
| [Addy Osmani Agent Skills](https://github.com/addyosmani/agent-skills) | `ci-cd-and-automation`, `api-and-interface-design`, `performance-optimization`, `observability-and-instrumentation`, `security-and-hardening` | 일반 CI/CD 기본 지침과 조건부 API 계약, 측정 기반 성능 조사, 운영 텔레메트리, 신뢰 경계 검토 |
| [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) | `vercel-react-best-practices`, `vercel-composition-patterns` | React/Next 구현 및 컴포넌트 구성 지침. upstream README는 MIT로 선언하지만 해당 리비전에 별도 LICENSE 전문 파일은 없음 |
| [ECC](https://github.com/affaan-m/ecc) | `deployment-patterns`, `database-migrations`, `mysql-patterns`, `doc-updater`, `docs-governance` | 복잡한 점진적 배포와 비단순 마이그레이션, MySQL 전용 지침, 선택형 문서 업데이트·무결성 감사 |
| Microsoft Playwright CLI | `playwright-cli`, Chromium | Grounded가 관리하는 실행 파일을 이용한 브라우저 QA |
| Vercel Web Interface Guidelines | `web-design-guidelines` | 요청에 따른 UI·접근성 검토. setup이 upstream 규칙을 갱신하고 커밋을 기록 |
| Matt Pocock Skills | `to-tickets`와 Grounded 어댑터 | 확인된 트래커에 티켓을 준비하고 승인된 경우 게시 |
| [CEO 검토](skills/plan-review-ceo/) | Codex `$grounded:plan-review-ceo`(네이티브) 또는 `$plan-review-ceo`(관리형); Claude `/grounded:plan-review-ceo` 또는 `/plan-review-ceo` | 범위 검토, 대안 비교, 11개 항목 계획 검토 |
| [엔지니어링 검토](skills/plan-review-eng/) | Codex `$grounded:plan-review-eng` 또는 `$plan-review-eng`; Claude `/grounded:plan-review-eng` 또는 `/plan-review-eng` | 4개 항목 기술 검토, 테스트 커버리지, 실행 의존성 |
| [ADR](skills/adr/) | Codex `$grounded:adr` 또는 `$adr`; Claude `/grounded:adr` 또는 `/adr` | 반대 관점 검토와 완결성 기준을 포함한 아키텍처 결정 기록 |
| [Jev](docs/jev.ko.md) | 별도 구성하는 평가 기능 | 명시적으로 허가된 작업에서만 사용하는 선택형 의사결정 지원 |

`$name`은 Codex 스킬 호출, `/name`은 Claude Code 스킬 호출입니다. 네이티브 플러그인의 이름은 `grounded`라서 `/grounded:<name>` 및 `$grounded:<name>` 형식을 사용합니다. 전체 setup은 접두어 없는 독립 스킬 이름을 설치합니다. 각 스킬의 선택 조건은 [워크플로 및 호출 안내](docs/workflow.ko.md)를 참고하세요.

## 빠른 시작

### Grounded 설치 및 실행

네이티브 플러그인은 setup, ADR, 계획 검토, Context7 OAuth 연결을 제공합니다. 호스트별로 setup을 한 번 실행해 관리형 의존성, 공통 개발 규칙, 알려진 충돌 백업을 구성합니다. 설치 항목은 [스킬 목록](#스킬-및-도구)과 [소스 정책](SOURCES.ko.md)에 정리되어 있습니다.

**Codex:** 컴퓨터마다 마켓플레이스를 추가하고 플러그인을 설치합니다.

```sh
codex plugin marketplace add reserver7/skills --ref main
codex plugin add grounded@grounded
```

호스트는 저장소를 관리형 마켓플레이스 캐시에 내려받고 `grounded/`에서 플러그인을 설치합니다. 사용자가 별도 클론이나 소스 체크아웃을 유지할 필요는 없습니다. 새 Codex 대화를 시작하고 `/plugins`에서 설치된 플러그인을 관리하세요.

설치 후 `$grounded:setup`을 실행합니다. 플러그인 온보딩으로도 실행할 수 있습니다. setup에는 macOS/Linux, Python 3.11+, Git, Node.js 20.19+, npm이 필요합니다. upstream 릴리스 SHA와 선언된 라이선스를 확인하고, 호스트 설정과 중복되는 전역 스킬을 백업하며, `superpowers`, `ponytail`, `supabase` Codex 플러그인 충돌을 제거하고, 관리형 구현 스킬과 공통 규칙을 설치합니다. 새 대화를 시작한 뒤 필요할 때 `$grounded:adr`, `$grounded:plan-review-ceo`, `$grounded:plan-review-eng`을 호출하세요.

**Claude Code(로컬 클론):** 저장소를 클론한 뒤 작업할 프로젝트에서 플러그인 디렉터리를 불러옵니다. Claude 마켓플레이스 설치는 아직 지원하지 않습니다.

```sh
git clone https://github.com/reserver7/skills.git ~/grounded-skills
cd /path/to/your/project
claude --plugin-dir ~/grounded-skills/grounded
```

플러그인을 불러온 뒤 `/grounded:setup`을 실행합니다. Claude에도 동일한 관리형 구현 스킬을 설치하고, 설정을 백업한 뒤 충돌하는 사용자 범위 플러그인을 비활성화하고 공통 규칙을 연결합니다. 새 대화를 시작한 뒤 필요하면 `/grounded:adr`, `/grounded:plan-review-ceo`, `/grounded:plan-review-eng`을 호출하세요.

Claude를 업데이트하려면 `git -C ~/grounded-skills pull --ff-only`를 실행하고 같은 `--plugin-dir` 옵션으로 새 세션을 연 뒤 `/grounded:setup`을 다시 실행합니다. Codex는 설정된 Git 마켓플레이스를 시작 시 갱신합니다. 즉시 업데이트하려면 `codex plugin marketplace upgrade grounded`를 실행한 뒤 새 대화에서 `$grounded:setup`을 다시 실행합니다. `codex plugin add grounded@grounded`는 최초 설치에만 사용합니다.

마켓플레이스 설치가 권장 경로입니다. 네이티브 플러그인은 Grounded 자체 스킬을 제공하고 공유 의존성만 사용자 스킬로 설치합니다. 아래의 독립 설치는 마켓플레이스 플러그인을 쓰지 않는 유지관리자를 위한 경로입니다. 같은 호스트에서 두 설치 경로를 함께 사용하지 마세요.

### 선택형 유지관리자 환경 설치

이 경로는 관리형 의존성, 공통 정책, 로컬 스킬을 설치합니다. macOS/Linux, Python 3.11+, Git, Node.js 20.19+, npm이 필요합니다. Codex 및/또는 Claude Code를 먼저 설치하고 인증하세요.

```sh
# 1. 환경 저장소 복제
git clone https://github.com/reserver7/skills.git
cd skills/grounded

# 2. 다운로드나 파일 변경 없이 설치 계획 확인
python3 setup/manage.py install --dry-run

# 3. Codex와 Claude Code 모두에 설치
python3 setup/manage.py install

# 4. 대상 프로젝트의 알려진 충돌 확인
python3 setup/manage.py doctor --project /path/to/project
```

설치한 호스트를 재시작하세요. 한 호스트만 설치할 때는 설치와 doctor 명령 모두에 `--host codex` 또는 `--host claude`를 추가합니다.

단순 변경에는 OpenSpec 초기화가 필요하지 않습니다. SDD가 필요한 프로젝트에서는 다음을 실행합니다.

```sh
python3 setup/manage.py openspec --project /path/to/project -- init --tools codex,claude --profile core
```

기존 프로젝트에서 재초기화하기 전에는 OpenSpec 파일을 확인하고 백업하세요. upstream CLI가 기존 파일을 정리할 수 있습니다. setup은 프로젝트를 자동 초기화하지 않습니다.

```text
저장 실패를 수정하세요. 변경 범위를 이 동작으로 제한하고 관련 동작을 검증하세요.

활성 OpenSpec 변경의 다음 작업을 구현하세요.
```

선택형 검토는 별도로 요청합니다. 독립 설치는 접두어 없는 스킬 이름을 사용하고, 네이티브 플러그인은 `grounded` 접두어를 사용합니다.

```text
# Codex 독립 설치
$plan-review-ceo review-request
$plan-review-eng review-request
$adr record the authentication strategy

# Claude Code 독립 설치
/plan-review-ceo review-request
/plan-review-eng review-request
/adr record the authentication strategy
```

검토 하나를 호출해도 다른 검토, ADR, 구현, Jev 평가가 자동으로 시작되지 않습니다.

## Context7 기술 문서 조회

네이티브 Grounded 플러그인은 Codex와 Claude에 Context7을 제공합니다. 호스트의 MCP 연결 설정에서 Grounded의 Context7 서버를 선택하고 요청에 따라 브라우저 로그인을 완료하세요. 다시 인증하라는 메시지가 나오면 같은 호스트 설정을 사용합니다. 엔드포인트와 조회 정책은 Grounded가 제공하고 OAuth 세션은 호스트가 저장합니다. 프로젝트 설정, 로컬 MCP 런타임, API 키는 필요하지 않습니다.

선택형 독립 설치에서도 같은 문서 정책을 적용합니다. MCP 도구를 사용하려면 호스트가 제공하는 Context7 연결이 필요하며, 연결이 없으면 upstream 공식 문서를 사용합니다.

## 스킬

### `setup` — 플러그인 설치 후 전역 Grounded 환경 구성

현재 호스트에서 `$grounded:setup` 또는 `/grounded:setup`을 한 번 실행합니다. 다운로드한 플러그인에 포함된 관리 도구를 사용하므로 수동 Git 클론은 필요하지 않습니다. 공식 릴리스의 최신 안정 OpenSpec 패키지와 라이선스를 확인한 구현 스킬을 선택해 설치합니다. 여기에는 Chromium이 포함된 Playwright CLI와 티켓 어댑터가 포함됩니다. setup은 `~/.codex/AGENTS.md` 또는 `~/.claude/CLAUDE.md`에 관리형 정책 블록 하나를 추가·갱신하면서 개인 지침을 보존합니다. 일반 파이프라인 변경에는 Addy CI/CD를 기본으로 사용하고 API/인터페이스 및 성능 스킬은 해당 작업에서만 선택합니다. ECC의 마이그레이션·MySQL 스킬은 해당 데이터베이스 작업에만, `deployment-patterns`는 복잡한 점진적 배포에만 사용합니다. setup은 중복 관리 스킬과 충돌 플러그인을 백업하며, 무관한 스킬 및 프로젝트 파일은 그대로 둡니다.

Python 3.11+, Git, Node.js 20.19+, npm이 필요합니다. 사용자 전용 백업과 영수증은 `~/.local/share/skills-environment/`, 마이그레이션 백업은 `~/.local/share/grounded/migration-backups/`에 보관합니다. setup 후 새 대화를 시작하세요. 플러그인 업데이트 후 setup을 다시 실행하면 `grounded-version` 표식이 있는 저장된 정책을 갱신합니다. 이전 설치를 미리 확인하고 복원하려면 `python3 <plugin-root>/setup/manage.py restore --host <codex|claude> --dry-run`을 실행하고, `--dry-run`을 빼고 적용합니다. 변경되지 않은 관리 스킬과 정책은 같은 방식의 `uninstall` 명령으로 제거할 수 있습니다. Grounded 의존성 버전은 로컬 영수증과 캐시를 사용합니다. 제거한 호스트 마켓플레이스 플러그인을 복구할 때는 호스트 CLI와 설정된 마켓플레이스를 사용할 수 있습니다. 두 명령 모두 백업을 보존하고 수정된 파일·정책 블록을 보호합니다. 플러그인을 비활성화하거나 제거해도 공유 setup은 제거되지 않으므로 관리 도구의 `uninstall`을 사용하세요.

검토 스킬은 호스트 문맥에 공통 정책이 이미 없을 때 번들 정책도 읽습니다. 독립 설치에서는 호스트 지침을 사용합니다. 상세 문서는 필요한 단계에서만 참고하며 자동으로 전체 문맥에 넣지 않습니다.

### `plan-review-ceo` — 범위 검토 및 11개 항목 계획 검토

현재 시스템, 전제, 기존 코드 재사용, 목표 상태를 점검하고 최소 2~3개의 구현 대안을 비교합니다. 선택한 접근과 EXPANSION / SELECTIVE / HOLD / REDUCTION 범위를 확정한 뒤 다음을 검토합니다.

아키텍처, 오류·복구, 보안, 데이터 흐름, 코드 품질, 테스트, 성능, 관측성, 배포, 장기 방향, 조건부 디자인·UX.

항목별 상호작용, 필수 다이어그램과 복구 맵, 요구사항 업데이트·ADR 후보, APPROVE / REVISE / REJECT 최종 판정을 유지합니다. 전체 검토를 짧은 체크리스트로 대체하지 않습니다.

```text
$plan-review-ceo add review requests to the cart
/plan-review-ceo add review requests to the cart
```

입력은 기존 OpenSpec 제안·명세·설계·작업, 관련 코드, 적용 가능한 ADR입니다. SDD가 없어도 명확한 요청이나 채팅 계획으로 진행할 수 있습니다.

출력은 `.ai/reviews/<slug>-ceo.md` 또는 프로젝트에서 이미 사용하는 검토 위치입니다. 이 문서는 검토 근거이며 별도 PRD나 구현 계획이 아닙니다. 자동으로 gitignore 처리되지 않으므로 프로젝트 저장 정책을 따릅니다.

### `plan-review-eng` — 엔지니어링 검토

현재 유효한 CEO 승인이 있으면 **ceo-reviewed**, 없으면 간단한 범위 확인을 포함한 **standalone** 모드로 실행합니다. 입력이 바뀌거나 뒤늦게 범위가 추가되면 오래된 승인을 그대로 적용하지 않고 감지합니다.

아키텍처, 코드 품질, 테스트 커버리지, 성능의 네 항목을 검토합니다. 커버리지 다이어그램, 행별 테스트 판단, 테스트 목표 질문, 의존성 표, 병렬 작업 레인, 실행 순서, 충돌 표시, ADR 후보와 최종 판정을 포함합니다.

```text
$plan-review-eng review-request
/plan-review-eng review-request
```

출력은 `.ai/reviews/<slug>-eng.md` 또는 프로젝트에서 정한 위치입니다. 확정된 CEO 근거를 재사용하고 기술적 공백을 살핍니다. 같은 인터뷰를 반복하거나 별도 작업 목록을 만들거나 worktree·에이전트를 시작하지 않습니다.

### `adr` — 아키텍처 결정 기록 작성

지속적으로 영향을 주거나 되돌리기 어려운 선택을 기록합니다. 의도와 범위 확인, 6개 인터뷰 분기, 신규 엔지니어·유지관리자·제품 책임자의 세 관점 검토를 포함합니다.

맥락, 하나의 선언적 결정, 균형 잡힌 결과, 대안, 재검토 조건, 참고 자료를 확인합니다. 6개 기준 중 5개 이상을 통과해야 하며 미해결 `[TBD]`, 차단 이슈, 필수 구조·링크 오류, 안티모놀리스 기준 위반이 없어야 합니다. 이 기준은 정확성 확률을 뜻하지 않습니다.

```text
$adr record the authentication strategy
/adr record the authentication strategy
```

출력은 기존 프로젝트 ADR 위치 또는 `docs/adr/YYYY-MM-DD-<slug>.md`입니다. 대체 결정은 이전 근거를 보존하며 새 기록으로 남깁니다. 기능 내부의 구현 선택은 보통 기존 설계 문서에 둡니다.

### 구현 및 CI/CD 지침

설치 대상에는 Superpowers v7 스킬 15개, Ponytail, Supabase 스킬 2개, Addy 스킬 5개, ECC 워크플로 4개, Playwright CLI, Matt Pocock 티켓 스킬, CLI-Anything의 탐색·하네스 작성 스킬, Craft Anything CLI, Anthropic의 `mcp-builder`·`frontend-design`, Vercel UI/React 스킬이 포함됩니다. setup은 소스 커밋, 라이선스 파일 또는 upstream의 명시적 라이선스 선언, Craft Anything 바이너리 SHA-256을 확인합니다. Vercel UI·React 스킬, ECC 문서 거버넌스, Anthropic 스킬 리비전을 기록합니다. upstream이 제공한 라이선스 파일은 보존하며, 없는 라이선스 전문을 만들지 않습니다. 전체 플러그인과 시작 훅은 설치하지 않습니다.

Addy CI/CD는 기본이며, 측정 기반 성능 조사, React/Next 구현과 공식 문서 조회, UI 제작·검토, 컴포넌트 구성, 보안, 마이그레이션, MySQL, 점진적 배포, CLI-Anything, Craft Anything은 해당 작업에서만 선택합니다. 예상치 못한 동작에는 디버깅, 적절한 동작 변경에는 TDD, 완료 주장 전에는 검증, 중요하거나 위험한 변경에는 하나의 코드 리뷰 절차를 사용합니다. Ponytail의 재사용·최소 완결 변경 원칙은 일반적으로 유용하지만, 다른 선택 절차가 구현을 이미 이끄는 경우 Ponytail 스킬 호출은 선택 사항입니다.

기본적으로 합의된 채팅 범위나 활성 OpenSpec 작업을 사용합니다. 브레인스토밍, 계획 작성, 실행 워크플로는 요청이 있을 때 사용합니다. 워크플로를 바꿀 때는 인계 내용을 기록하고 활성 계획을 하나로 유지합니다. [워크플로 선택](docs/workflow.ko.md)

### Jev — 선택형 평가

Jev는 setup으로 설치하거나 자동 호출하지 않습니다. 공식 제공자를 호스트별로 따로 설정하고 인증정보를 Git 밖에 보관하며, 실제 사용 가능한 도구 스키마를 따릅니다.

요청되었거나 해당 작업에 대해 허가되었고 구체적인 대안과 기준이 있을 때만 호출합니다. 매 변경을 평가하거나 동일한 평가를 반복하지 않으며, 점수를 테스트나 승인 대신 사용하지 않습니다. [Jev 사용 안내](docs/jev.ko.md)를 참고하세요.

## 아키텍처

### 공통 규칙

[rules/development.md](rules/development.md)가 공통 정책 원본입니다. 마켓플레이스 설치자는 번들된 `setup` 스킬을 한 번 실행합니다. 독립 환경 설치도 같은 정책을 연결합니다. 두 방식 모두 호스트가 자동으로 읽는 지침 파일의 관리 블록 하나를 재사용하고, 그 바깥의 내용을 보존합니다.

| 작업 | 계획의 기준 | 구현 |
|---|---|---|
| 명확하고 국소적인 변경 | 사용자 요청 | 직접 수정 및 관련 검증 |
| 여러 부분의 명확한 작업 | 채팅의 간단한 범위·인수 조건 | 선택한 구현 스킬 |
| 중요한 요구사항·설계 불확실성 | OpenSpec | 기존 작업을 따르고, 필요한 경우 맞는 Superpowers 절차 또는 직접 수정용 Ponytail을 선택 |

저장소에 OpenSpec 디렉터리가 있다는 이유만으로 SDD를 강제하지 않습니다. 동작이 바뀌면 기존 명세를 최신 상태로 유지합니다. 조사 중 중요한 불확실성이 드러나면 워크플로를 강화합니다.

### 중복 책임 방지

- SDD를 사용할 때 요구사항·설계·작업의 기준은 하나의 OpenSpec입니다.
- 기본 구현 코드 리뷰 절차는 Superpowers 하나입니다.
- Ponytail은 직접 수정에 선택적으로 쓰며, 선택한 Superpowers 절차가 구현을 맡으면 필수로 추가하지 않습니다.
- 계획 검토는 제안된 작업을, 코드 리뷰는 구현 결과를 검토합니다.
- 검토 간 확정된 답변·근거·다이어그램·결과를 재사용합니다.
- 선택 단계는 자동으로 이어지지 않습니다.
- 단계를 줄여도 선택한 검토의 핵심 점검을 줄이지 않습니다.

[워크플로](docs/workflow.ko.md)와 [검토 절차 매핑](docs/review-procedures.ko.md)을 참고하세요.

### 의존성 및 설치

[manifest.json](manifest.json)은 공식 OpenSpec npm 패키지, 외부 Git 저장소, 선택 스킬, 라이선스, 충돌하는 전체 플러그인을 선언합니다. setup은 지원되는 안정 릴리스와 문서화된 기본 브랜치 예외를 확인합니다. 호스트 파일을 바꾸기 전에 패키지 무결성, Git 커밋 SHA, 라이선스 파일 또는 upstream README의 명시적 선언을 확인하고 로컬 영수증을 기록합니다. 소스 스냅샷을 캐시하고 manifest의 항목만 설치합니다. 중복 관리 스킬을 옮기거나 충돌 플러그인을 비활성화하기 전에 비공개 백업을 만듭니다. [소스 및 라이선스 정책](SOURCES.ko.md)

[setup/manage.py](setup/manage.py)는 선택된 콘텐츠 설치, 호스트별 호출 메타데이터 생성, 공통 규칙 적용, 설치 파일 해시 기록을 담당합니다.

| 콘텐츠 | 위치 |
|---|---|
| Codex 스킬 | `~/.agents/skills/` |
| Codex 규칙 | `~/.codex/AGENTS.md`의 관리 블록 |
| Claude 스킬 | `~/.claude/skills/` |
| Claude 규칙 | `~/.claude/CLAUDE.md`의 관리 블록 |
| 소스, 비공개 OpenSpec 설치, 백업, 영수증 | `~/.local/share/skills-environment/` |

로컬 검토·ADR·Craft Anything 스킬은 명시적으로 호출해야 합니다. setup에는 GitHub와 npm 접근이 필요합니다. 복원과 삭제는 로컬 영수증·캐시를 사용합니다. 제거했던 호스트 플러그인을 복원할 때는 마켓플레이스에 연결될 수 있습니다.

## 검증

```sh
# 정적 manifest, 스킬 이름, 지침 크기 확인
python3 setup/manage.py check

# 관리형 설치와 알려진 충돌 확인
python3 setup/manage.py doctor --project /path/to/project
```

doctor는 알려진 이름, 일반적인 스킬 위치, 활성 중복 플러그인, 관리 파일 해시, 정책 블록, 영수증의 OpenSpec 버전·무결성·lockfile 해시를 확인합니다. 임의의 프로젝트 문구, 이름을 바꾼 도구, 비표준 경로까지 모두 탐지할 수는 없습니다.

정적 검사는 새 컴퓨터 호환성, 에이전트 준수, 결함 탐지 품질 동등성, 토큰 절감을 증명하지 않습니다. 자세한 한계는 [런타임 검증 기록 요약](docs/validation.ko.md)과 [영문 원본 기록](docs/validation.md)에 있습니다.

## 로컬 설치 및 업데이트

`setup`은 실행할 때마다 upstream 버전을 확인합니다. 버전과 무결성 식별자는 로컬 영수증에 저장하며, 소스 체크아웃은 커밋별, OpenSpec은 버전별로 캐시합니다. restore는 Grounded 의존성을 다시 조회하지 않습니다. 복원 작업이 제거된 호스트 마켓플레이스 플러그인을 되돌리는 경우 호스트 CLI가 마켓플레이스에 연결될 수 있습니다.

```sh
python3 setup/manage.py restore --host codex --dry-run
python3 setup/manage.py restore --host codex
```

Claude에는 `--host claude`를 사용합니다. 변경되지 않은 관리 스킬과 정책을 제거하려면 같은 `--dry-run` 미리보기를 거쳐 `uninstall`을 실행합니다. 두 명령은 수정된 파일을 보존하고, 비공개 백업을 유지하며, 수동 확인이 필요한 경로를 보고합니다. 백업은 자동 삭제하지 않습니다. 출력된 위치를 확인하고 더 이상 필요하지 않을 때 직접 정리하세요.

호스트 하나만 설치하거나 별도 설치 홈을 사용할 수 있습니다.

```sh
python3 setup/manage.py install --host codex
python3 setup/manage.py install --host claude
python3 setup/manage.py install --home /absolute/path/to/home --dry-run
```

별도 홈 옵션은 설치 경로만 바꾸며 호스트 프로세스가 해당 홈을 사용하도록 설정하지 않습니다. 기본이 아닌 `CODEX_HOME`, `CLAUDE_CONFIG_DIR` 레이아웃은 자동 지원하지 않습니다.

업데이트할 때는 다음을 실행합니다.

```sh
git pull --ff-only
python3 setup/manage.py install --dry-run
python3 setup/manage.py install
python3 setup/manage.py doctor --project /path/to/project
```

마켓플레이스 `setup`은 최신 관리 리비전을 확인하고 이름이 정확히 일치하는 중복 전역 스킬을 백업한 뒤 충돌 플러그인을 비활성화하거나 제거하고 설치합니다. 무관한 개인 스킬과 프로젝트 파일은 그대로 둡니다. 독립 `install`은 관리되지 않거나 수정된 설치 경로가 있으면 중단합니다. 독립 설치가 이전에 관리했던 항목 중 현재 manifest에서 빠진 스킬은 변경되지 않은 경우 업데이트 중 백업한 뒤 제거합니다.

백업에는 이전 지침 파일, 옮긴 전역 스킬, Codex 플러그인 캐시·마켓플레이스 소스가 포함될 수 있습니다. 백업 디렉터리 권한은 `0700`, 파일 권한은 `0600`이며 자동 삭제하지 않습니다. 설치가 실패하면 옮긴 스킬과 비활성화된 플러그인의 복원을 시도합니다. 다운로드한 소스와 npm 캐시는 남을 수 있습니다. setup은 셸 시작 파일을 수정하거나 호스트 앱을 설치하지 않습니다.

관리형 OpenSpec 버전을 실행하려면 다음을 사용합니다.

```sh
python3 /path/to/skills/grounded/setup/manage.py openspec --project /path/to/project -- <arguments>
```

일반 `openspec` 명령은 PATH에서 다른 버전을 선택할 수 있습니다.

## 버전 확인

어느 디렉터리에서든 사용할 터미널 명령을 만들려면 저장소 루트에서 다음 두 명령을 한 번 실행해 버전 조회기를 사용자 bin 디렉터리에 설치합니다.

```sh
mkdir -p ~/.local/bin
install -m 755 grounded/setup/version_report.py ~/.local/bin/grounded
```

`grounded -v`를 실행합니다. `--host codex` 또는 `--host claude`를 추가하면 해당 호스트 정책만 표시합니다. 이 명령은 로컬 파일을 읽고 가장 최근 setup 영수증에 기록된 의존성 리비전을 보여줍니다. 호스트 정책이 더 오래되었다면 실제 호스트별 의존성은 영수증과 다를 수 있습니다. 저장소 루트에서는 `python3 grounded/setup/manage.py version`으로 체크아웃된 패키지 버전을 확인할 수 있습니다.

정식 플러그인 버전은 [plugin.json](plugin.json)에 있습니다. 릴리스 PR 전에 저장소 루트에서 `python3 setup/release.py bump <MAJOR.MINOR.PATCH>`를 실행하면 Codex와 Claude manifest 버전을 함께 갱신합니다. GitHub Release 노트는 병합된 PR 제목과 분류를 사용하며, 릴리스 분류 라벨은 직접 지정해야 합니다. 일반 변경은 저장소 [변경 로그](../CHANGELOG.md)에 반복해서 기록하지 않습니다. README 배지는 최신 `skills-v*` 릴리스를 표시하므로 버전을 직접 수정할 필요가 없습니다. 병합된 커밋에 `skills-v<version>` 태그를 붙입니다. 릴리스 CI는 태그·버전 일치, main 브랜치 포함 여부, setup 검사를 확인하고 일치하는 `grounded-<version>.zip`을 Release에 첨부합니다.

공통 정책 블록에도 동일한 버전이 기록됩니다. 플러그인을 업데이트해도 사용자 지침은 자동으로 바뀌지 않으므로 setup을 다시 실행해야 합니다. Codex 커스텀 마켓플레이스는 `main`을 추적하며 릴리스 태그만으로 실행 중인 호스트가 갱신되지는 않습니다. Claude는 현재 로컬 클론에서 업데이트합니다.

Git 리비전은 규칙, 설치 도구, 로컬 스킬을 식별합니다. [manifest.json](manifest.json)은 공식 upstream 저장소와 npm registry를 선언합니다. setup은 최신 안정 의존성 버전과 Vercel, ECC 문서 거버넌스, Anthropic 스킬의 기본 브랜치 리비전을 확인해 로컬에 기록합니다. `restore`는 upstream을 다시 조회하지 않고 이전에 기록된 Grounded 설정으로 돌아갑니다.

릴리스 태그는 `skills-v*` 형식을 사용합니다. OpenSpec은 안정 버전과 패키지 무결성을 확인한 뒤 npm `latest`에서 설치합니다. 버전별 lockfile은 로컬 캐시에 보관하며, 컴퓨터별 영수증과 캐시는 Git에 커밋하지 않습니다.

브랜치, Pull Request, 커밋, 릴리스 절차는 [CONTRIBUTING.md](../CONTRIBUTING.md)를 참고하세요.

## 라이선스

MIT — [LICENSE](../LICENSE)를 확인하세요. 각 로컬 스킬은 단독 설치에 필요한 라이선스 고지를 포함하며, 외부 스킬 설치본은 upstream 라이선스 파일을 보존합니다.

## 감사의 말

- [OpenSpec](https://github.com/Fission-AI/OpenSpec) — SDD 절차와 산출물.
- [Superpowers](https://github.com/obra/superpowers) — 디버깅, TDD, 리뷰, 검증 기법.
- [Ponytail](https://github.com/DietrichGebert/ponytail) — 재사용과 최소 완결 변경 원칙.
- Michael Nygard의 ADR 구조 — Context, Decision, Consequences.

소스 선택 정책과 호환성 조정은 [소스 정책](SOURCES.ko.md)에 기록되어 있습니다.
