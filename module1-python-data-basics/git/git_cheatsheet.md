# Git 명령어 치트시트 (2026-09-22)

## 최초 설정
git config --global user.name "이름"
git config --global user.email "이메일"

## 설정 확인
git config --global user.name     # 커밋 작성자 이름 확인
git config --global user.email    # 커밋 작성자 이메일 확인 (GitHub 계정 이메일과 같아야 잔디가 채워짐)
git remote -v                     # 이 저장소의 원격 주소 확인

## 저장소 생성/연결
git init                                    # 로컬 저장소 초기화
git remote add origin <저장소 URL>           # 원격 저장소 연결

## 기본 흐름
git add <파일명>          # 특정 파일만 선별 (Staging)
git add .                 # 변경된 파일 전체 선별
git commit -m "메시지"    # 로컬 저장소에 확정 기록
git push -u origin main   # 최초 1회는 -u 옵션으로 추적 브랜치 설정
git push                  # 이후에는 push만
git pull                  # 원격 저장소의 최신 내용 받아오기

## 상태 확인
git status    # 변경 사항 확인
git log       # 커밋 기록 확인
git log --graph   # 브랜치 흐름을 그래프로 확인

## 브랜치
git branch                     # 브랜치 목록 확인
git checkout -b <브랜치명>      # 브랜치 생성 + 이동
git checkout <브랜치명>         # 다른 브랜치로 이동
git checkout main              # main으로 복귀

## 브랜치 합치기 (로컬에서 직접)
git checkout main      # 합칠 대상(main)으로 먼저 이동
git pull               # main 최신화
git merge test1        # 지금 있는 브랜치(main)로 test1을 합침
git push origin main

## 브랜치 정리
git branch -d <브랜치명>              # 내 컴퓨터에서 브랜치 삭제
git push origin --delete <브랜치명>   # GitHub에서 브랜치 삭제

## 합친 것 되돌리기
git revert -m 1 <merge 커밋 해시>   # 합친 내용을 반대로 되돌리는 새 커밋 생성
# ⚠️ 팀이 함께 쓰는 main에서는 reset --hard + push --force 대신 반드시 revert 사용