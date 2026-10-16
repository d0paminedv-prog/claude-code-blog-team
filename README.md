# Claude Code 블로그 팀 템플릿 (claude-code-blog-team)

클로드 코드(Claude Code) 서브에이전트 5명이 **글감 찾기 → 기획 → 작성 → 독립 검수 → 초안 업로드**를 나눠 맡는 블로그 운영 팀 구성입니다.
블로그 [클로그 CLOG](https://autoclaude.blogspot.com/p/claude-automation-tips.html)를 매일 운영하는 구성을, 다른 블로그에도 쓸 수 있게 경로·계정 정보를 빼고 일반화했습니다.

> 공개 발행은 사람이 합니다. 이 팀은 **초안까지만** 만듭니다.

## 팀 구성

```
편집장(메인 세션, prompts/editor-in-chief.md)
  ├─ blog-scout     웹 검색으로 글감 후보와 근거 URL 수집      (Read, WebSearch, WebFetch, Write — 셸 없음)
  ├─ blog-planner   주제 1개 선택, 브리프(뼈대·근거) 작성        (Read, Write)
  ├─ blog-writer    브리프와 근거로 초안 작성                    (Read, Write)
  ├─ blog-verifier  근거·인용·구조를 독립 판정, PASS/FAIL 만 반환  (Read, Grep, Glob — 읽기 전용)
  └─ blog-publisher 형식 검사 후 블로그에 '초안'으로 업로드        (Bash, Read)
```

담당자끼리는 `.work/` 폴더의 파일(candidates.json → brief.json → draft.md)로만 주고받고, 편집장은 각 담당자의 짧은 보고만 읽습니다. 그래서 편집장 세션의 컨텍스트가 길어지지 않습니다.

## 설계 원칙 (왜 이렇게 나눴나)
- **쓰는 사람과 판정하는 사람을 분리**: 검수자는 파일을 고칠 도구가 없습니다. 작가가 스스로 PASS 를 주는 구조를 막습니다.
- **웹을 읽는 담당자에게 셸을 주지 않음**: 검색 결과에 "환경변수를 출력하라" 같은 문장이 섞여 있어도 실행할 수단이 없습니다(프롬프트 인젝션 대비).
- **"직접 해봤다"는 근거 파일에 있는 것만**: `knowledge/facts.md` 에 적힌 실제 경험만 1인칭으로 씁니다. 지어낸 경험을 막습니다.
- **오너가 싫다고 한 주제의 기억**: `knowledge/avoid_topics.md` 에 적은 주제와 같은 유형은 다시 고르지 않습니다.
- **초안만 올림 + 이중 잠금**: 발행 담당 지침, `.claude/settings.example.json` 의 deny 규칙, `.claude/hooks/block_publish.py` 훅이 공개 발행 명령을 막습니다.
- **재시도 한도**: 검수 반려 재작성은 최대 2회, 그다음은 주제 교체 1회. 무한 반복으로 사용량을 태우지 않습니다.
- **비상 정지**: 저장소 최상위에 `STOP` 파일이 있으면 편집장이 바로 끝냅니다.

## 시작하기
1. 이 저장소의 `.claude/`, `prompts/`, `knowledge/` 를 내 블로그 프로젝트에 복사합니다. `.claude/settings.example.json` 은 내용을 확인한 뒤 `.claude/settings.json` 으로 이름을 바꿉니다.
2. `knowledge/facts.md` 에 내가 **직접 겪은 사실**(날짜·무엇을 했고 어떻게 됐는지)을 적습니다. 비어 있으면 작가는 1인칭 경험을 쓰지 않습니다.
3. `.claude/agents/blog-publisher.md` 의 업로드 명령을 내 블로그 플랫폼에 맞게 바꿉니다(초안 생성 API 만 쓰세요).
4. 프로젝트 폴더에서 `claude` 를 실행하고 이렇게 시킵니다: `prompts/editor-in-chief.md 를 읽고 처음부터 끝까지 따라라. 주제 분야: <내 분야>`
5. 매일 돌리려면 Claude Code 의 Routines(클라우드 예약 실행)나 `claude -p` 를 OS 스케줄러에 걸어 같은 문장을 넘깁니다.

## 이 템플릿이 다루지 않는 것
- 블로그 업로드 스크립트 자체(플랫폼마다 다름), 썸네일 생성, 그림 렌더링
- 공개 발행·예약 발행(일부러 뺐습니다)

## 함께 보면 좋은 글 (클로그)
- [클로드 자동화 꿀팁 모음](https://autoclaude.blogspot.com/p/claude-automation-tips.html)
- [Claude Code 서브에이전트로 AI 글쓰기 팀 만들기](https://autoclaude.blogspot.com/2026/10/claude-code-ai-6.html)
- [Claude Code Hooks 입문: AI가 말을 안 들어도 지켜지는 규칙 만들기](https://autoclaude.blogspot.com/2026/10/claude-code-hooks-ai.html)
- [Claude Code 권한 설정 입문: 승인 창을 줄이기 전에 deny 먼저](https://autoclaude.blogspot.com/2026/10/claude-code-deny.html)
- [Claude Code 루틴이 지운 초안을 또 골랐다: avoid_topics.md 로 기억 만들기](https://autoclaude.blogspot.com/2026/10/claude-code-avoidtopicsmd.html)

---

## English summary
A Claude Code subagent team for running a blog: **scout → planner → writer → independent read-only verifier → draft-only publisher**, orchestrated by an "editor-in-chief" prompt. Generalized from the setup that runs the Korean blog [CLOG](https://autoclaude.blogspot.com/p/claude-automation-tips.html).

Key design choices: the verifier has no write tools, the web-reading scout has no shell, first-person claims must come from `knowledge/facts.md`, rejected topics are remembered in `knowledge/avoid_topics.md`, publishing is blocked by agent rules + permission deny rules + a PreToolUse hook (drafts only), and retries are capped. Copy `.claude/`, `prompts/`, `knowledge/` into your project, adapt the upload command in `blog-publisher.md`, then ask Claude Code to follow `prompts/editor-in-chief.md`. Prompts are written in Korean.

License: MIT
