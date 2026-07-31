"""모의고사 마크다운 파서.

파일 I/O 없는 순수 함수라 테스트에서 문자열만 넣어 검증할 수 있다.

- `parse_questions()`  : `*_문제.md`     → 메타 + 문항 목록
- `parse_solutions()`  : `*_정답해설.md` → 정답표 + 문항별 해설/모범답안/채점기준

두 파일 모두 코드 펜스(```)를 포함하므로, 모든 구조 인식은 **펜스 밖에서만** 수행한다.
펜스 안의 `①`, `---`, `**...**` 는 문제 지문의 일부이지 구조가 아니다.
"""

import re
import unicodedata

CIRCLED = "①②③④⑤"
FENCE_RE = re.compile(r"^\s*(```|~~~)")
HR_RE = re.compile(r"^\s*-{3,}\s*$")

# **12. [기초]** 지문…   /  **22.** 지문…
QUESTION_RE = re.compile(r"^\*\*(\d{1,2})\.\s*(?:\[([^\]]+)\])?\*\*\s*(.*)$")
# ## Ⅰ. 객관식 (각 3점, 총 63점)
SECTION_RE = re.compile(r"^##\s*([ⅠⅡⅢIVX]+)\.\s*(\S+)\s*(?:\((.*)\))?")
# **3. 정답 ④** — 해설…
SOLUTION_ANSWER_RE = re.compile(r"^\*\*(\d{1,2})\.\s*정답\s*([①②③④⑤])\*\*\s*(?:—|-|:)?\s*(.*)$")
# **28. (5점)**
ESSAY_HEADER_RE = re.compile(r"^\*\*(\d{1,2})\.\s*\((\d+(?:\.\d+)?)점\)\*\*")
# **22.** …
SHORT_HEADER_RE = re.compile(r"^\*\*(\d{1,2})\.\*\*\s*(.*)$")

SECTION_TYPES = {"객관식": "MC", "주관식": "SHORT", "서술형": "ESSAY"}
DIFFICULTIES = {"기초": "BASIC", "응용": "APPLIED", "심화": "ADVANCED"}


def nfc(text):
    """macOS는 파일명·파일 내용을 NFD로 저장하기도 한다. 비교 전 NFC로 통일."""
    return unicodedata.normalize("NFC", text)


def iter_lines(text):
    """(line, in_fence) 튜플을 순회한다. 펜스 시작/끝 줄 자체는 in_fence=True로 본다."""
    in_fence = False
    for line in nfc(text).splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            yield line, True
            continue
        yield line, in_fence


def _clean_block(lines):
    """문항 본문 정리: 앞뒤 빈 줄과 구분선(---) 제거."""
    out = []
    for line, in_fence in lines:
        if not in_fence and HR_RE.match(line):
            continue
        out.append(line)
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return "\n".join(out)


def _section_points(section_note, qtype):
    """섹션 헤더 괄호 안에서 배점을 읽는다.

    '각 3점, 총 63점'                         → 기본 배점 3
    '28번 5점, 29·30번 각 4점, 총 13점'       → {28: 5, 29: 4, 30: 4}
    """
    default = {"MC": 3, "SHORT": 4, "ESSAY": 4}[qtype]
    per_question = {}
    if not section_note:
        return default, per_question

    note = nfc(section_note)
    each = re.search(r"각\s*(\d+(?:\.\d+)?)\s*점", note)
    if each:
        default = float(each.group(1))

    # "28번 5점" / "29·30번 각 4점"
    for numbers, points in re.findall(r"([\d·,\s]+)번\s*(?:각\s*)?(\d+(?:\.\d+)?)\s*점", note):
        for n in re.findall(r"\d+", numbers):
            per_question[int(n)] = float(points)
    return default, per_question


def _split_choices(body):
    """MC 지문에서 ①~④ 선택지를 분리해 (stem, choices) 반환.

    선택지는 줄마다 하나씩 있을 수도, `① '0'  ② 0  ③ ''  ④ NaN` 처럼 한 줄에 몰려 있을 수도 있다.
    코드 펜스 안의 동그라미 숫자는 건드리지 않는다.
    """
    stem_lines = []
    choice_lines = []
    for line, in_fence in iter_lines(body):
        starts_choice = not in_fence and line.lstrip().startswith(tuple(CIRCLED))
        if starts_choice:
            choice_lines.append(line.strip())
        elif choice_lines:
            # 선택지가 시작된 뒤의 줄은 직전 선택지의 이어지는 내용으로 본다.
            if line.strip():
                choice_lines[-1] += " " + line.strip()
        else:
            stem_lines.append(line)

    if not choice_lines:
        return body.strip(), []

    joined = "\n".join(choice_lines)
    parts = re.split(f"[{CIRCLED}]", joined)[1:]  # 첫 조각은 첫 동그라미 앞의 빈 문자열
    choices = []
    for index, part in enumerate(parts, start=1):
        text = " ".join(part.split()).strip()
        if text:
            choices.append({"number": index, "text": text})

    while stem_lines and not stem_lines[-1].strip():
        stem_lines.pop()
    return "\n".join(stem_lines).strip(), choices


def _strip_scribbled_answer(stem):
    """V1 문제 파일에 사람이 적어 둔 정답 표시(지문 끝의 `3`)를 제거한다."""
    return re.sub(r"\s*`\s*[1-4]\s*`\s*$", "", stem.rstrip(), flags=re.MULTILINE).rstrip()


def parse_questions(md_text):
    """`*_문제.md` → {"meta": {...}, "questions": [...]}"""
    text = nfc(md_text)
    meta = {"round": None, "version": None, "title": "", "scope": "", "time_limit_min": 60, "total_score": 100}

    title_match = re.search(r"^#\s+(.*)$", text, flags=re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
        meta["title"] = title
        round_match = re.search(r"\((\d+)차\)", title)
        version_match = re.search(r"Version\s*(\d+)", title, flags=re.IGNORECASE)
        if round_match:
            meta["round"] = int(round_match.group(1))
        if version_match:
            meta["version"] = int(version_match.group(1))

    scope_match = re.search(r"^>\s*출제 범위\s*:\s*(.*)$", text, flags=re.MULTILINE)
    if scope_match:
        meta["scope"] = scope_match.group(1).strip()
    time_match = re.search(r"권장 시간\s*:\s*\**\s*(\d+)\s*분", text)
    if time_match:
        meta["time_limit_min"] = int(time_match.group(1))
    total_match = re.search(r"총\s*\**\s*(\d+)\s*점\**\s*$", text, flags=re.MULTILINE)
    if total_match:
        meta["total_score"] = int(total_match.group(1))

    questions = []
    current = None
    qtype = None
    default_points = 3
    per_question_points = {}

    def flush():
        if current is None:
            return
        body = _clean_block(current["lines"])
        if current["qtype"] == "MC":
            stem, choices = _split_choices(body)
            current["body"] = _strip_scribbled_answer(stem)
            current["choices"] = choices
        else:
            current["body"] = body
            current["choices"] = []
        del current["lines"]
        questions.append(current)

    for line, in_fence in iter_lines(text):
        if not in_fence:
            section = SECTION_RE.match(line)
            if section:
                label = section.group(2).strip()
                if label in SECTION_TYPES:
                    flush()
                    current = None
                    qtype = SECTION_TYPES[label]
                    default_points, per_question_points = _section_points(section.group(3), qtype)
                continue

            question = QUESTION_RE.match(line)
            if question and qtype:
                flush()
                number = int(question.group(1))
                current = {
                    "number": number,
                    "qtype": qtype,
                    "difficulty": DIFFICULTIES.get((question.group(2) or "").strip(), "BASIC"),
                    "points": per_question_points.get(number, default_points),
                    "lines": [(question.group(3), False)],
                }
                continue

        if current is not None:
            current["lines"].append((line, in_fence))

    flush()
    return {"meta": meta, "questions": questions}


def _parse_answer_table(text):
    """빠른 정답표(`| 1 | 2 | … |` + `| ① | ② | … |`)에서 {번호: 정답} 추출."""
    answers = {}
    header = None
    for line, in_fence in iter_lines(text):
        stripped = line.strip()
        if in_fence or not stripped.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if all(re.fullmatch(r"-{1,}", c or "-") for c in cells):
            continue  # 구분선
        # 주의: '①'.isdigit()도 True다. 문항 번호 행은 ASCII 숫자만으로 판별한다.
        if all(c.isascii() and c.isdigit() for c in cells if c):
            header = [int(c) for c in cells if c]
            continue
        if header and all(c in CIRCLED for c in cells if c):
            picks = [CIRCLED.index(c) + 1 for c in cells if c]
            answers.update(dict(zip(header, picks)))
            header = None
    return answers


def _extract_short_answer_rules(first_line, block):
    """주관식 정답 후보와 키워드 규칙을 1차 추출한다.

    형식이 문항마다 제각각이라(백틱 값 / 굵은 글씨 / 불릿 / 코드블록) 완벽하지 않다.
    확신이 낮으면 needs_review=True로 표시해 admin에서 손보게 한다.
    """
    line = first_line.strip()
    # 답이 여러 불릿/번호 항목에 나뉘어 있으면 첫 줄만으로는 규칙을 만들 수 없다.
    # 불릿 기호 뒤에는 반드시 공백이 온다. `\s+`가 아니면 **굵은 글씨**의 앞 별표를 잘라먹는다.
    is_list_item = bool(re.match(r"^([-*+]|\d+\.)\s+", line))
    is_fence = bool(FENCE_RE.match(line))
    stem = re.sub(r"^([-*+]|\d+\.)\s+", "", line)

    raw_tokens = re.findall(r"`([^`]+)`", stem) + re.findall(r"\*\*([^*]+)\*\*", stem)
    tokens = []
    for token in raw_tokens:
        # `**`undefined`**` 처럼 강조가 중첩되면 마크업 문자가 섞여 들어온다.
        cleaned = token.replace("`", "").replace("*", "").strip()
        if cleaned and cleaned not in tokens:
            tokens.append(cleaned)

    plain = re.sub(r"[`*]", "", stem).strip()
    accepted = []
    if plain and len(plain) <= 60:
        accepted.append(plain)
    for token in tokens:
        if token not in accepted:
            accepted.append(token)

    keywords = [tokens] if tokens else []

    needs_review = (
        is_fence  # 답이 코드블록 안에 있음
        or is_list_item  # 여러 항목으로 나뉜 답
        or not tokens  # 뽑아낼 값이 없음
        or len(plain) > 60  # 서술형에 가까운 답
        or "가지" in plain
        or "정답 인정" in plain
    )
    return accepted, keywords, needs_review


def _parse_rubric(block):
    """`| 2점 | 채점 요소 |` 표를 [{"points": 2, "criteria": "…"}] 로 변환."""
    rubric = []
    for line, in_fence in iter_lines(block):
        stripped = line.strip()
        if in_fence or not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 2:
            continue
        points_match = re.match(r"^(\d+(?:\.\d+)?)\s*점$", cells[0])
        if points_match:
            rubric.append({"points": float(points_match.group(1)), "criteria": cells[1]})
    return rubric


def _parse_model_answer(block):
    """`**모범 답안**` 뒤의 인용문(`> …`)을 모은다."""
    lines = []
    collecting = False
    for line, in_fence in iter_lines(block):
        stripped = line.strip()
        # 표제 줄만 시작 신호로 본다. 인용문 본문에 같은 표현이 나와도 건너뛰면 안 된다.
        if not in_fence and not stripped.startswith(">") and "모범 답안" in stripped:
            collecting = True
            continue
        if not collecting:
            continue
        if stripped.startswith(">"):
            lines.append(re.sub(r"^>\s?", "", stripped).rstrip())
        elif stripped and not stripped.startswith(("|", "-")):
            lines.append(stripped)
    return "\n".join(lines).strip()


def parse_solutions(md_text):
    """`*_정답해설.md` → {"answers", "explanations", "short", "essay", "warnings"}"""
    text = nfc(md_text)
    table_answers = _parse_answer_table(text)

    explanations = {}
    inline_answers = {}
    short = {}
    essay = {}
    warnings = []

    section = None
    current_number = None
    current_lines = []

    def flush():
        if current_number is None:
            return
        block = _clean_block(current_lines)
        if section == "MC":
            explanations[current_number] = block
        elif section == "SHORT":
            first_line = block.splitlines()[0].strip() if block.splitlines() else ""
            accepted, keywords, needs_review = _extract_short_answer_rules(first_line, block)
            short[current_number] = {
                "explanation": block,
                "accepted_answers": accepted,
                "required_keywords": keywords,
                "needs_review": needs_review,
            }
            if needs_review:
                warnings.append(f"{current_number}번 주관식 채점 규칙 검토 필요")
        elif section == "ESSAY":
            essay[current_number] = {
                "explanation": block,
                "rubric": _parse_rubric(block),
                "model_answer": _parse_model_answer(block),
            }

    for line, in_fence in iter_lines(text):
        if not in_fence:
            section_match = SECTION_RE.match(line)
            if section_match:
                label = section_match.group(2).strip()
                if label in SECTION_TYPES:
                    flush()
                    current_number, current_lines = None, []
                    section = SECTION_TYPES[label]
                continue

            if section == "MC":
                match = SOLUTION_ANSWER_RE.match(line)
                if match:
                    flush()
                    current_number = int(match.group(1))
                    inline_answers[current_number] = CIRCLED.index(match.group(2)) + 1
                    current_lines = [(match.group(3), False)]
                    continue
            elif section in ("SHORT", "ESSAY"):
                header = ESSAY_HEADER_RE.match(line) if section == "ESSAY" else SHORT_HEADER_RE.match(line)
                if header:
                    flush()
                    current_number = int(header.group(1))
                    rest = header.group(2) if section == "SHORT" else ""
                    current_lines = [(rest, False)]
                    continue

        if current_number is not None:
            current_lines.append((line, in_fence))

    flush()

    # 빠른 정답표와 개별 해설의 정답이 어긋나면 표를 신뢰하되 경고를 남긴다.
    answers = dict(table_answers)
    for number, pick in inline_answers.items():
        if number in answers and answers[number] != pick:
            warnings.append(
                f"{number}번 정답 불일치: 정답표 {CIRCLED[answers[number] - 1]} vs 해설 {CIRCLED[pick - 1]}"
            )
        answers.setdefault(number, pick)

    return {
        "answers": answers,
        "explanations": explanations,
        "short": short,
        "essay": essay,
        "warnings": warnings,
    }
