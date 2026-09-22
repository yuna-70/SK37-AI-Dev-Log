# Module 1 - Git & GitHub

## 📅 2026-09-22 | Git/GitHub 기초 - 버전 관리, Branch, GitHub Flow, 충돌 해결
> 참고: [`git_cheatsheet.md`](./git_cheatsheet.md)

### 개념

**1. 코드 버전 관리의 필요성**
- 코드는 수정이 빈번해서, 원하는 시점(버전)으로 되돌아갈 수 있게 해주는 도구가 필요함 → 버전 관리 시스템

**2. Git과 GitHub**
- Git: 로컬 컴퓨터에 설치하는 버전 관리 시스템, 변경 사항 추적 및 이전 버전으로 되돌리기 가능
- GitHub: 로컬 Git 저장소를 클라우드에 저장·공유·협업할 수 있게 해주는 웹 플랫폼

**3. 로컬 저장소 ↔ 원격 저장소**
- Local Repository: 내 컴퓨터의 `.git` 폴더 (나 혼자만의 기록)
- Remote Repository: GitHub 서버의 저장소 (팀원과 공유하는 공간)
- `push`: 로컬 → 원격 업로드 / `pull`: 원격 → 로컬 다운로드

**4. 코드 저장 및 버전 관리 절차**
- git 설치 → 로컬 저장소 생성 → GitHub 원격 저장소 생성 → git 환경설정(이름/이메일) → add & commit → 원격 연결 후 push → pull

**5. 버전 관리 3단계 흐름 (VS Code)**
- Changes: 아직 commit 안 한 변경 사항 (`U` = Untracked, 한 번도 저장 안 한 파일)
- Staging: `+` 버튼으로 이번 버전에 남길 파일만 선별
- Commit: 메시지 작성 후 확정 → 저장소에 영구 기록

**6. Branch — 원본을 보호하는 안전한 복사본**
- main(원본)을 그대로 둔 채 마음껏 테스트할 수 있는 복사본
- 실패하면 브랜치만 삭제하면 되고, 원본은 안전함
- 브랜치를 바꾸면 그 브랜치에서 작업한 내용만 화면에 나타남

**7. GitHub Flow — 팀 프로젝트 협업 규칙**
- 원칙: "모든 작업은 새 Branch에서 시작하고, 검토 후에 합친다"
- 5단계: 브랜치 생성(Local) → 작업·commit(Local) → push(Network) → Pull Request(GitHub) → Merge(GitHub)

**8. Pull Request(PR)**
- 내 브랜치의 변경 사항을 main에 합쳐도 되는지 검토를 요청하는 "결재 서류"
- Files changed 탭: 빨간색(삭제된 코드) / 초록색(추가된 코드)으로 변경 내역 확인
- Merge 후 다 쓴 브랜치는 Delete branch로 정리

**9. Conflict(충돌) — 에러가 아니라 조율 과정**
- 원인: 내 로컬이 GitHub 최신 변경을 모르는 상태에서 같은 줄을 다르게 수정하고 push → Rejected
- 해결: pull → Merge Editor에서 확인
  - `<<<<<<< HEAD`: 내 코드(Current) / `=======`: 구분선 / `>>>>>>>`: GitHub 코드(Incoming)
  - Accept Current / Accept Incoming / Accept Both Changes 중 선택
- 선택 후 병합 커밋(Merge Commit) → 다시 push

### 왜 이렇게 했는가
- 팀 프로젝트에서 test1 → main을 합칠 때 로컬에서 바로 merge하지 않고 **PR로 합친 이유**
  → GitHub에서 변경 내용(Files changed)을 확인한 뒤 합칠 수 있고, 누가 무엇을 합쳤는지 기록이 남아서 팀원 코드를 실수로 덮어쓰는 일을 막을 수 있음
- Merge 후 **로컬 main에서 다시 Pull**한 이유
  → GitHub의 main은 합쳐졌지만 내 컴퓨터의 main은 아직 옛날 상태라, 동기화하지 않으면 다음 작업 때 충돌이 날 수 있음

### 막혔던 부분 / 이해 포인트
- VS Code가 여러 폴더를 한꺼번에 연 `Untitled (Workspace)` 상태로 열려서, 실습용 workspace 폴더와 기존 폴더들이 섞여 보였음
  → `Open Folder`는 폴더 하나만, `Add Folder to Workspace`는 기존 창에 폴더를 추가하는 방식이라는 차이를 알게 됨
- workspace 폴더에 origin을 새로 설정하면 기존 TIL 저장소에 영향이 있을까 걱정했는데,
  **origin은 각 폴더의 `.git` 안에 따로 저장**되어 서로 독립적이라는 걸 `git remote -v`로 확인함
- 반대로 `git config --global`은 **컴퓨터 전체에 적용**되는 설정이라, 이름/이메일을 바꾸면 모든 저장소의 커밋 작성자가 바뀐다는 점을 알게 됨
  (이메일이 GitHub 계정과 다르면 잔디가 안 채워질 수 있음)
- 합친(Merge) 걸 되돌릴 수 없을까 걱정했는데, **Revert**로 "합친 내용을 반대로 되돌리는 새 커밋"을 만들어 되돌릴 수 있다는 걸 배움
  → 팀이 함께 쓰는 main에서는 기록을 지우는 `reset --hard` + `push --force` 대신 반드시 Revert를 써야 함

---