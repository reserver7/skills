# 소스 및 호환성 변경

[English](SOURCES.md) | **한국어**

## 외부 도구

| 소스 | Setup에서 버전 결정 | 설치 콘텐츠 |
|---|---|---|
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) | `registry.npmjs.org`의 안정 `latest` dist-tag, 패키지 무결성 확인 | 버전별 비공개 npm 경로 아래 공식 CLI. 프로젝트별 스킬은 명시적 init 때만 생성 |
| [Context7](https://github.com/upstash/context7/blob/master/docs/howto/oauth.mdx) | 네이티브 플러그인 매니페스트에 선언된 공식 원격 OAuth MCP 엔드포인트 | 문서 도구와 공통 조회 정책. 로그인과 세션 저장은 각 호스트가 담당 |
| [Superpowers](https://github.com/obra/superpowers) | 최신 안정 GitHub Release를 태그에서 전체 커밋 SHA로 확인해 가져옴 | 스크립트와 참조 자료를 포함한 v7 스킬 15개. 작업별 기법 5개와 선택형 스킬 10개 |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | 최신 안정 GitHub Release를 전체 커밋 SHA로 가져옴 | 훅 없는 ponytail 스킬만 설치 |
| [Supabase Agent Skills](https://github.com/supabase/agent-skills) | 최신 안정 GitHub Release와 전체 커밋 SHA 확인. upstream 릴리스의 MIT `LICENSE` 확인 | `supabase`, `supabase-postgres-best-practices` |
| [Addy Osmani Agent Skills](https://github.com/addyosmani/agent-skills) | 최신 안정 GitHub Release와 전체 커밋 SHA 확인. MIT `LICENSE` | 일반 CI/CD용 `ci-cd-and-automation`, 측정 기반 성능 작업용 `performance-optimization`, API 계약 설계용 `api-and-interface-design`, 운영 텔레메트리용 `observability-and-instrumentation`, 신뢰 경계 방어 검토용 `security-and-hardening` |
| [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) | setup 시 기본 브랜치 HEAD를 커밋 SHA로 기록. upstream README의 MIT 선언을 확인하며 별도 LICENSE 전문 파일은 없음 | `react-best-practices`와 `composition-patterns`를 각각 `vercel-react-best-practices`, `vercel-composition-patterns`로 설치합니다. 소스 커밋과 README 라이선스 선언을 기록하며 LICENSE 전문을 만들지 않습니다. |
| [Microsoft Playwright CLI](https://github.com/microsoft/playwright-cli) | 최신 안정 GitHub 릴리스, 루트 Apache-2.0 LICENSE | `playwright-cli`, 일치하는 npm 릴리스, Grounded 상태에 설치하는 Chromium |
| [Vercel Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines) | setup 시 기본 브랜치 HEAD를 커밋 SHA로 기록. 루트 MIT LICENSE | upstream `command.md`와 라이선스, Grounded `web-design-guidelines` 어댑터 |
| [Anthropic Skills](https://github.com/anthropics/skills) | setup 시 기본 브랜치 HEAD를 커밋 SHA로 기록. 스킬별 Apache-2.0 `LICENSE.txt` | 원본 지침과 라이선스를 포함한 upstream `mcp-builder`, `frontend-design` 전체 폴더 |
| [CLI-Anything](https://github.com/HKUDS/CLI-Anything) | 최신 안정 GitHub Release를 전체 커밋 SHA로 가져옴. 루트 Apache-2.0 `LICENSE` | 공식 설치 프로그램이 포함하는 기준 방법론 리소스를 갖춘 upstream Codex `cli-anything` 스킬과 정식 스킬 경로의 `cli-hub-meta-skill`. 둘 다 Grounded 관리 선택형 스킬이며 upstream은 Codex 생성기 연동을 실험적/커뮤니티 기능으로 표시 |
| [Craft Anything](https://github.com/storytold/craft-anything) | 호스트 플랫폼용 최신 안정 GitHub Release 자산과 공식 GitHub 자산의 SHA-256 확인. macOS universal ZIP 또는 Linux x86_64/aarch64 AppImage | Grounded 비공개 버전 캐시의 공식 CLI 바이너리. 명시 호출 전용 `craft-anything` 스킬로만 제공 |
| [Matt Pocock Skills](https://github.com/mattpocock/skills) | 최신 안정 GitHub Release, 루트 MIT LICENSE | `skills/engineering/to-tickets`와 OpenSpec 및 승인된 트래커 게시를 위한 Grounded 어댑터 |
| [Everything Claude Code (ECC)](https://github.com/affaan-m/ecc) | 최신 안정 GitHub Release를 전체 커밋 SHA로 가져옴. MIT `LICENSE` | 복잡한 점진 배포용 `deployment-patterns`, 중요한 DB 변경용 `database-migrations`, MySQL 전용 `mysql-patterns`, 명시 호출 독립 스킬인 `agents/doc-updater.md` |
| [ECC documentation governance](https://github.com/affaan-m/ECC/tree/main/.agents/skills/docs-governance) | setup 시 기본 브랜치 HEAD를 커밋 SHA로 기록. 루트 MIT LICENSE | upstream 감사 스크립트와 참조를 포함한 `docs-governance`. 요구사항과 ADR에는 기존 Grounded 책임자 사용 |
| 로컬 검토 및 ADR 스킬 | `skills/plan-review-ceo/`, `skills/plan-review-eng/`, `skills/adr/` | 이전 로컬 구현에서 분리·조정한 독립 절차. 외부 검토 플러그인을 설치하거나 다운로드하지 않음 |
| [Jev](https://typesafe.ai/) | 패키지 포함/고정하지 않는 선택형 서비스 | 연결 안내만 제공. 현재 공식 제공자 안내에 따라 별도 설정 |

Setup은 검증된 Git 체크아웃에서 외부 스킬 폴더, Vercel 규칙, upstream이 제공한 라이선스 파일을 복사합니다. 라이선스 파일을 우선 확인하고, 파일이 없으면 공식 README의 명시적 라이선스 선언만 허용하며 그 근거를 기록합니다. 없는 라이선스 전문은 만들지 않습니다. 복원 시 새로운 버전을 조회하지 않도록 해결된 버전과 불변 식별자를 로컬에 기록합니다.

새 설치 경로에서는 외부 소스 트리를 이 Git 저장소에 포함하지 않습니다. OpenSpec 설치 lockfile은 버전 캐시에 유지하며 캐시와 백업은 머신 로컬에만 두고 커밋하지 않습니다.

## 의도적인 조정

- 독립 Superpowers 스킬에서는 플러그인 전용 `superpowers:` 접두사를 제거합니다.
- `requesting-code-review`는 upstream `code-reviewer.md`를 보존하면서 [이식 가능한 어댑터](setup/adapters/requesting-code-review.md)를 사용합니다. 미커밋 작업, 기존 OpenSpec/대화 요구사항, 사용 가능한 리뷰어 도구, 독립 리뷰어를 사용할 수 없는 경우의 명시적 처리까지 다룹니다. 사소한 편집에서는 리뷰어 에이전트를 실행하지 않습니다.
- Grounded는 Superpowers 계획·실행·지원 스킬을 명시적 선택형으로 설치하고 계획 인계 기록을 공유합니다. Superpowers와 Ponytail 시작 훅은 setup 대상이 아닙니다.
- 설치된 모든 스킬에는 Codex 호출 메타데이터가 있습니다. 로컬 검토, ADR, Craft Anything 스킬은 두 호스트에서 명시적으로만 호출합니다.
- CLI-Hub 탐색과 CLI-Anything 하네스 생성은 작업별로 선택하는 별도 워크플로입니다. 먼저 검색하고 CLI 패키지 설치나 앱/시스템 상태 변경 전에 허가를 받습니다. 전체 upstream 플러그인을 설치하지 않으며 생성된 하네스가 기존 자격 증명·권한·사용량 한도를 우회하게 하지 않습니다.
- Grounded는 양쪽 호스트를 위해 upstream CLI-Anything 스킬 설명을 조정하고 라우팅/설치 보호를 추가합니다. 방법론 원본 파일은 공식 설치 프로그램에서 가져와 포함합니다.
- Craft Anything은 초기 알파의 포트폴리오 레퍼런스 조사 절차이며 명시적으로만 호출합니다. Setup은 공식 릴리스의 플랫폼 CLI를 다운로드하고 캐시 전에 SHA-256을 확인합니다. 제3자 레퍼런스에는 클린룸 모드를 사용하며 보호된 자산이나 콘텐츠를 복사하지 않습니다.
- `frontend-design`은 시각적 UI 제작, `web-design-guidelines`는 별도 UI/접근성 검토를 담당합니다. Vercel React 모범 사례는 React/Next 구현을 안내하고 컴포지션 패턴은 컴포넌트 API와 아키텍처 작업에 사용합니다. Context7은 버전에 맞는 공식 API 문서를 제공하고 Addy 성능 안내는 측정 기반 조사에 사용합니다.
- CEO 검토는 전제/기존 코드/이상적 상태 도전, 대안 2~3개, 사용자 선택 접근과 범위 모드, 11개 검토 섹션(UX는 조건부), 다이어그램/복구 지도/테스트 범위, 이슈별 상호작용, 판정과 검토 기록을 유지합니다. 상세 섹션·평가표·템플릿은 해당 단계에서 불러옵니다.
- 엔지니어링 검토는 단독/CEO 검토 후 접수, 늦은 변경 감지, 네 기술 섹션, 테스트 목표와 범위 다이어그램, 의존성 표/병렬 작업/순서/충돌 분석, ADR 후보, 판정과 검토 기록을 유지합니다. 이전 CEO 사실과 결정을 재사용하고 기술적 변경점은 별도로 확인합니다.
- ADR은 의도/범위 확인, 여섯 인터뷰 분기, 세 가지 반대 관점, 여섯 기준 중 다섯 통과 및 미해결 자리표시자 차단, 모놀리스 방지 임계값, 필수 본문 섹션, 추가 기록 방식의 대체를 유지합니다. 관문 표기를 정확도 확률로 취급하지 않습니다. 부족한 근거나 결과를 기준 채우기용으로 만들어내지 않습니다.
- 환경별 피치/설정/프로필/카탈로그 의존성은 기존 OpenSpec·대화 입력과 내장 기본값으로 바꿉니다. 호스트별 질문 API는 사용 가능한 호스트 도구 또는 직접 대화를 사용합니다. 자동 인계, 추가 PRD/계획, 중복 코드 리뷰, 별도 메모리 서비스는 제외하되 실질 검토를 토큰 절감 목적으로 제거하지 않습니다.
- 검토 기록은 호스트 중립적인 `.ai/reviews/` 또는 프로젝트 기존 관례를 사용합니다. 이후 검토가 범위 변경을 찾도록 검토한 입력 근거를 남기되 두 번째 계획 문서가 되지 않게 합니다. OpenSpec은 요구사항/작업을 담당합니다. 구현에는 작업에 맞는 Superpowers 절차를 쓰거나 간결한 직접 수정에 Ponytail을 선택하며 기본으로 겹쳐 호출하지 않습니다.
- 공통 정책은 책임과 SDD가 불필요한 조건을 정합니다. 별도 오케스트레이터도, 구현 매뉴얼 복사본도 아닙니다.

이 내용은 기존 로컬 절차와 선택된 Superpowers 스킬의 호환성 조정입니다. 검토 품질이 동등하다거나 측정된 토큰 절감 효과가 있다고 주장하지 않습니다.

기존 검토/ADR 저작권 표시는 루트 [LICENSE](../LICENSE)에 모으고 각 로컬 스킬에는 `LICENSE.review-skills`로 복사해 개별 다운로드도 자체적으로 사용할 수 있게 합니다. 외부 Superpowers와 Ponytail 스킬은 관리형 설치 때 각각 upstream 라이선스 파일을 유지합니다. Michael Nygard의 Context / Decision / Consequences ADR 구조를 인정합니다.
