# 기여 안내

[English](CONTRIBUTING.md) | **한국어**

## 브랜치

- 장기 유지 브랜치는 `main` 하나이며 항상 릴리스 가능한 상태여야 합니다. 강제 푸시하거나 삭제하지 마세요.
- `main` 변경은 필수 `validate` 검사를 통과하도록 Pull Request로만 반영합니다. 최신 `main`에서 시작해 `feat/<slug>`, `fix/<slug>`, `docs/<slug>`, `chore/<slug>`, `ci/<slug>` 중 맞는 이름을 사용합니다.
- 병합 후 작업 브랜치를 삭제합니다. `develop`, `release` 또는 기능 브랜치를 장기 보관하지 않습니다.

`main` 규칙 세트는 GitHub Actions의 `validate` 검사를 요구하고, 강제 푸시와 브랜치 삭제를 막으며 우회 권한을 허용하지 않습니다.

```sh
git switch main
git pull --ff-only
git switch -c feat/skill-install-check
# 변경하고 확인
git push -u origin feat/skill-install-check
# main 대상으로 Pull Request 생성
```

커밋 메시지에는 [Grounded 개발 규칙](grounded/rules/development.md)의 Conventional Commits를 사용합니다. PR 제목과 직접 적용한 릴리스 분류 라벨은 자동 생성 GitHub Release 노트에 사용됩니다. 제목 접두사는 라벨을 자동 지정하지 않습니다. 중요한 설계 결정의 이유, 호환성·마이그레이션 안내 또는 측정 근거를 영구 기록해야 할 때만 [변경 로그](CHANGELOG.md)를 갱신하세요. 일상적인 PR 요약을 두 곳에 복사하지 마세요. PR 템플릿에서 이 맥락을 설명하고 별도 변경 로그 항목이 불필요하면 `None`이라고 적습니다.

## 릴리스

- 최신 `main` 커밋에서만 릴리스 태그를 만듭니다.
- 태그 형식은 `skills-v<MAJOR>.<MINOR>.<PATCH>`입니다. 예: `skills-v0.1.1`.
- 정식 플러그인 버전은 `grounded/plugin.json`에 있습니다. 릴리스 준비 브랜치에서 `python3 grounded/setup/release.py bump <version>`을 실행해 Claude 매니페스트와 버전을 맞추고, `extensions.com.openai.publication.release_notes`가 `Grounded <version>:`으로 시작하게 합니다. PR 템플릿과 Conventional Commit 제목 형식을 사용합니다. 릴리스 분류 라벨은 유지 관리자가 직접 적용합니다. GitHub는 `.github/release.yml` 기준으로 병합된 PR 제목과 카테고리에서 일반 변경을 담은 노트를 생성합니다. 중요한 결정·호환성·마이그레이션·측정 근거만 [변경 로그](CHANGELOG.md)에 남기고 일반 PR 요약은 중복하지 않습니다. README 배지는 최신 `skills-v*` 태그를 자동으로 표시합니다. 호환 수정은 PATCH, 새 기능은 MINOR, 호환되지 않는 변경은 MAJOR를 사용합니다. 1.0 이전의 호환되지 않는 변경에는 MINOR를 사용합니다.
- 병합된 버전 커밋에 태그를 붙입니다. CI는 해당 커밋이 `main`에 속하고 두 매니페스트 버전이 태그와 일치하는지 확인합니다. 불일치하면 릴리스가 중단되며 CI가 태그된 커밋을 수정하지 않습니다.
- 유효한 `skills-v*` 태그를 푸시하면 `grounded-<version>.zip`을 포함한 GitHub Release가 게시됩니다. 게시한 태그를 이동하거나 재사용하지 마세요.
- Codex 커스텀 마켓플레이스는 `main`을 추적하고 Codex 시작 시 Git 원본에서 갱신됩니다. 릴리스 태그가 실행 중인 클라이언트에 즉시 배포되지는 않습니다. Claude Code는 현재 복제된 `grounded/` 디렉터리를 `claude --plugin-dir`로 불러오며 Claude 마켓플레이스 배포는 별도 계획입니다. 호스트 플러그인 원본 갱신 후 Grounded setup을 다시 실행해 공통 규칙, 현재 관리 리비전, 버전 표식을 갱신합니다. 안정 릴리스의 소스와 기본 브랜치 예외는 [소스 정책](grounded/SOURCES.ko.md)에 있습니다.

```sh
# 릴리스 준비 브랜치에서 변경 후 PR로 커밋 및 병합
python3 grounded/setup/release.py bump 0.1.1

# 버전 변경이 main에 병합된 뒤
git switch main
git pull --ff-only
git tag -a skills-v0.1.1 -m "Grounded v0.1.1"
git push origin skills-v0.1.1
```

## GitHub 보호

저장소는 공개되어 누구나 열람하고 포크할 수 있습니다. 쓰기 권한은 명시적으로 부여하며 저장소 공개 설정 변경이나 삭제를 포함한 관리 권한은 소유자와 관리자에게만 있습니다.

활성 규칙 세트는 `refs/heads/main`에 적용되며 강제 푸시와 브랜치 삭제를 차단하고 우회자를 두지 않습니다. 소유자와 관리자는 규칙 세트를 변경하거나 제거할 수 있으므로 신뢰하는 협업자에게만 저장소 권한을 부여합니다.
