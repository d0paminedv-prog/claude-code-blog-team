"""PreToolUse 훅: Bash 명령에 '공개 발행'으로 보이는 패턴이 있으면 막는다(종료 코드 2 → Claude Code 가 실행을 취소하고 사유를 에이전트에게 전달).

지침(발행 담당은 초안만 올린다)이 지켜지지 않아도 마지막에 한 번 더 막는 안전장치다. 내 플랫폼의 공개 API 패턴을 PATTERNS 에 더한다.
시험: echo '{"tool_name":"Bash","tool_input":{"command":"curl -X POST .../posts/123/publish"}}' | python3 .claude/hooks/block_publish.py; echo $?   # 2 가 나와야 한다
"""
import json
import re
import sys

PATTERNS = [
    r"/posts/[^/\s]+/publish\b",        # Blogger API posts.publish
    r"isDraft\s*=\s*false",            # Blogger API posts.insert 를 공개로
    r"[\"']?status[\"']?\s*[:=]\s*[\"']?(publish|future)\b",  # WordPress REST 공개·예약
    r"--publish\b",
    r"\bpublish\s*=\s*true\b",
]


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:  # noqa: BLE001  입력을 못 읽으면 막지 않는다(다른 도구 호출을 방해하지 않게)
        return 0
    command = str((data.get("tool_input") or {}).get("command", ""))
    for pat in PATTERNS:
        if re.search(pat, command, re.I):
            print(f"공개 발행으로 보이는 명령이라 막았습니다(패턴: {pat}). 이 팀은 초안만 올립니다.", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
