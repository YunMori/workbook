"""모의고사 마크다운 파서.

파일 I/O 없는 순수 함수라 테스트에서 문자열만 넣어 검증할 수 있다.

- `parse_questions()`  : `*_문제.md` / `*_문제지.md`     → 메타 + 문항 목록
- `parse_solutions()`  : `*_정답해설.md` / `*_정답지.md` → 정답표 + 문항별 해설/모범답안/채점기준

원본 마크다운은 회차마다 표기가 조금씩 다르다. 아래 두 계열을 모두 받는다.

    2차 계열      `## Ⅰ. 객관식 (각 3점, 총 63점)` / `**12. [기초]** 지문`
    1차(round 01) `## 객관식`                      / `**12.** 지문` 또는 `### 12. 지문`

두 파일 모두 코드 펜스(```)를 포함하므로, 모든 구조 인식은 **펜스 밖에서만** 수행한다.
펜스 안의 `①`, `---`, `**...**` 는 문제 지문의 일부이지 구조가 아니다.
"""

import re
import unicodedata

CIRCLED = "①②③④⑤"
FENCE_RE = re.compile(r"^\s*(```|~~~)")
HR_RE = re.compile(r"^\s*-{3,}\s*$")

# **12. [기초]** 지문…   /  **22.** 지문…
QUESTION_RE = re.compile(r"^\*\*(\d{1,3})\.\s*(?:\[([^\]]+)\])?\*\*\s*(.*)$")
# ### 12. 지문…
QUESTION_HEADING_RE = re.compile(r"^###\s*(\d{1,3})\.\s*(?:\[([^\]]+)\]\s*)?(.*)$")
# ## Ⅰ. 객관식 (각 3점, 총 63점) / ## 객관식 / ## 주관식 해설 / ## 서술형 채점 기준
SECTION_RE = re.compile(
    r"^##\s*(?:[ⅠⅡⅢⅣⅤIVX]+\.\s*)?(객관식|주관식|서술형)"
    r"(?:\s*(?:해설|채점\s*기준))?\s*(?:\((.*)\))?\s*$"
)
# **3. 정답 ④** — 해설…
SOLUTION_ANSWER_RE = re.compile(r"^\*\*(\d{1,3})\.\s*정답\s*([①②③④⑤])\*\*\s*(?:—|-|:)?\s*(.*)$")
# **28. (5점)**  /  **61**  /  **61.**
ESSAY_BOLD_HEADER_RE = re.compile(r"^\*\*(\d{1,3})\.?(?:\s*\((\d+(?:\.\d+)?)점\))?\*\*\s*$")
# ### 61. 제목… (4점)
ESSAY_HEADING_RE = re.compile(r"^###\s*(\d{1,3})\.\s*.*?(?:\((\d+(?:\.\d+)?)점\))?\s*$")
# **22.** …  /  - **41.** …
SHORT_HEADER_RE = re.compile(r"^(?:[-*+]\s+)?\*\*(\d{1,3})\.?\*\*\s*(.*)$")
# 지문 끝의 배점 표기 — `… 설명하시오. (4점)`
TRAILING_POINTS_RE = re.compile(r"\s*\((\d+(?:\.\d+)?)\s*점\)\s*$")

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


def _match_question_header(line):
    """`**12. [기초]** 지문` 과 `### 12. 지문` 두 표기를 모두 받는다.

    (번호, 난이도 표기, 첫 줄 지문) 또는 None.
    """
    match = QUESTION_RE.match(line) or QUESTION_HEADING_RE.match(line)
    if not match:
        return None
    return int(match.group(1)), (match.group(2) or "").strip(), match.group(3)


def _match_essay_header(line):
    """정답지의 서술형 문항 머리글. `**28. (5점)**` / `**61**` / `### 61. 제목 (4점)`."""
    match = ESSAY_BOLD_HEADER_RE.match(line) or ESSAY_HEADING_RE.match(line)
    return int(match.group(1)) if match else None


def _section_points(section_note, qtype):
    """섹션 헤더 괄호 안에서 배점을 읽는다.

    '각 3점, 총 63점'                         → 기본 배점 3
    '28번 5점, 29·30번 각 4점, 총 13점'       → {28: 5, 29: 4, 30: 4}
    괄호가 아예 없으면(`## 객관식`) 유형별 기본 배점을 쓴다.
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

    # 선택지 번호는 반드시 ①→②→③→④ 순으로 나온다. 앞 번호 뒤에서만 다음 번호를 찾으면
    # `④ ①, ②만 존재한다` 처럼 선택지 본문이 다른 번호를 언급해도 쪼개지지 않는다.
    joined = "\n".join(choice_lines)
    marks = []
    cursor = 0
    for number, mark in enumerate(CIRCLED, start=1):
        position = joined.find(mark, cursor)
        if position == -1:
            break
        marks.append((number, position))
        cursor = position + 1

    choices = []
    for index, (number, position) in enumerate(marks):
        end = marks[index + 1][1] if index + 1 < len(marks) else len(joined)
        text = " ".join(joined[position + 1 : end].split()).strip()
        if text:
            choices.append({"number": number, "text": text})

    while stem_lines and not stem_lines[-1].strip():
        stem_lines.pop()
    return "\n".join(stem_lines).strip(), choices


def _strip_scribbled_answer(stem):
    """V1 문제 파일에 사람이 적어 둔 정답 표시(지문 끝의 `3`)를 제거한다."""
    return re.sub(r"\s*`\s*[1-4]\s*`\s*$", "", stem.rstrip(), flags=re.MULTILINE).rstrip()


def _parse_meta(text, source_name):
    """제목 줄과 머리말에서 차수·버전·과목명 등을 읽는다.

    차수·버전 표기는 회차마다 다르다. 제목에서 못 찾으면 파일 이름으로 보완한다.

        `… 모의고사 (2차) — Version 1`                  → 2차 V1
        `Vue Component State Flow 모의고사 — Round 01 v5` → 1차 V5
        `JS DOM과 Event 모의고사 — Version 1`            → (차수는 파일 이름에서)
    """
    meta = {
        "round": None,
        "version": None,
        "title": "",
        "subject": "",
        "scope": "",
        "time_limit_min": 60,
        "time_explicit": False,
        "total_score": None,
        "total_explicit": False,
    }

    title_match = re.search(r"^#\s+(.*)$", text, flags=re.MULTILINE)
    title = title_match.group(1).strip() if title_match else ""
    meta["title"] = title

    for pattern in (r"\((\d+)\s*차\)", r"Round\s*0*(\d+)"):
        match = re.search(pattern, title, flags=re.IGNORECASE)
        if match:
            meta["round"] = int(match.group(1))
            break
    for pattern in (r"Version\s*0*(\d+)", r"\bv0*(\d+)\b"):
        match = re.search(pattern, title, flags=re.IGNORECASE)
        if match:
            meta["version"] = int(match.group(1))
            break

    name = nfc(source_name)
    if meta["round"] is None:
        match = re.search(r"round[_\s-]*0*(\d+)", name, flags=re.IGNORECASE)
        if match:
            meta["round"] = int(match.group(1))
    if meta["version"] is None:
        match = re.search(r"[_\s-]v0*(\d+)\b", name, flags=re.IGNORECASE)
        if match:
            meta["version"] = int(match.group(1))

    # 과목명 — 제목에서 버전 꼬리표와 '모의고사'를 떼어낸 부분. 시험 이름에 쓴다.
    subject = re.split(r"\s+[—–]\s+", title)[0]
    subject = re.sub(r"\(\s*\d+\s*차\s*\)", "", subject)
    meta["subject"] = re.sub(r"모의고사\s*$", "", subject.strip()).strip()

    scope_match = re.search(r"^>\s*출제 범위\s*:\s*(.*)$", text, flags=re.MULTILINE)
    meta["scope"] = scope_match.group(1).strip() if scope_match else meta["subject"]
    time_match = re.search(r"권장 시간\s*:\s*\**\s*(\d+)\s*분", text)
    if time_match:
        meta["time_limit_min"] = int(time_match.group(1))
        meta["time_explicit"] = True
    total_match = re.search(r"총\s*\**\s*(\d+)\s*점\**\s*$", text, flags=re.MULTILINE)
    if total_match:
        meta["total_score"] = int(total_match.group(1))
        meta["total_explicit"] = True
    return meta


def parse_questions(md_text, source_name=""):
    """`*_문제.md` → {"meta": {...}, "questions": [...]}

    `source_name`은 제목에 차수·버전이 없을 때 참고하는 파일 이름이다(선택).
    """
    text = nfc(md_text)
    meta = _parse_meta(text, source_name)

    questions = []
    current = None
    qtype = None
    default_points = 3
    per_question_points = {}
    points_explicit = False

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
            # 서술형은 지문 끝에 배점을 적어 두기도 한다 — `… 설명하시오. (4점)`
            # 배점은 화면에서 따로 보여 주므로 지문에서는 떼어낸다.
            lines = current["body"].splitlines()
            if current["qtype"] == "ESSAY" and lines:
                trailing = TRAILING_POINTS_RE.search(lines[0])
                if trailing:
                    lines[0] = TRAILING_POINTS_RE.sub("", lines[0])
                    current["body"] = "\n".join(lines)
                    if not current["points_explicit"]:
                        current["points"] = float(trailing.group(1))
                        current["points_explicit"] = True
        del current["lines"]
        questions.append(current)

    for line, in_fence in iter_lines(text):
        if not in_fence:
            section = SECTION_RE.match(line)
            if section:
                label = section.group(1).strip()
                if label in SECTION_TYPES:
                    flush()
                    current = None
                    qtype = SECTION_TYPES[label]
                    note = section.group(2)
                    default_points, per_question_points = _section_points(note, qtype)
                    points_explicit = bool(note and "점" in note)
                continue

            question = _match_question_header(line)
            if question and qtype:
                flush()
                number, difficulty, first_line = question
                current = {
                    "number": number,
                    "qtype": qtype,
                    "difficulty": DIFFICULTIES.get(difficulty, "BASIC"),
                    "points": per_question_points.get(number, default_points),
                    "points_explicit": points_explicit or number in per_question_points,
                    "lines": [(first_line, False)],
                }
                continue

        if current is not None:
            current["lines"].append((line, in_fence))

    flush()

    if not meta["total_explicit"]:
        # 원본에 총점 표기가 없으면 배점 합계가 곧 총점이다(1차는 세트마다 문항 수가 다르다).
        meta["total_score"] = round(sum(q["points"] for q in questions))
    if not meta["time_explicit"] and questions:
        # 권장 시간이 적혀 있지 않으면 2차 기준(30문항 60분 = 문항당 2분)으로 잡는다.
        # 응시 화면은 이 시간이 끝나면 자동 제출하므로 문항 수에 비례해야 한다.
        meta["time_limit_min"] = max(60, round(len(questions) * 2 / 5) * 5)
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
    # `정답: Pinia — 슬라이드에서 …` 처럼 머리말과 부연 설명이 붙어 오는 회차가 있다.
    stem = re.sub(r"^정답\s*[::]\s*", "", stem)
    stem = re.split(r"\s+[—–]\s+", stem, maxsplit=1)[0].strip()

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

    # 마크업이 없는 짧은 한 낱말 답(`HTMLCollection`)은 그 자체를 키워드로 쓴다.
    keywords = [tokens] if tokens else ([[plain]] if plain and len(plain) <= 30 else [])

    needs_review = (
        is_fence  # 답이 코드블록 안에 있음
        or is_list_item  # 여러 항목으로 나뉜 답
        or not keywords  # 뽑아낼 값이 없음
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
    """`**모범 답안**` 뒤의 본문을 모은다.

    인용문(`> …`)으로 적힌 회차와 `**모범 답안:** 본문…`처럼 같은 줄에 이어 쓴 회차가 있다.
    """
    lines = []
    collecting = False
    for line, in_fence in iter_lines(block):
        stripped = line.strip()
        # 표제 줄만 시작 신호로 본다. 인용문 본문에 같은 표현이 나와도 건너뛰면 안 된다.
        if not in_fence and not stripped.startswith(">") and "모범 답안" in stripped:
            collecting = True
            # `**모범 답안:**` / `**모범 답안**:` 등 표기가 섞여 있어 남은 기호를 털어낸다.
            rest = re.sub(r"^.*?모범\s*답안", "", stripped).lstrip("*:： ").strip()
            if rest:
                lines.append(rest)
            continue
        if not collecting:
            continue
        if stripped.startswith(">"):
            lines.append(re.sub(r"^>\s?", "", stripped).rstrip())
        elif stripped and not stripped.startswith(("|", "-")):
            lines.append(stripped)
        elif not stripped and lines:
            lines.append("")  # 여러 문단으로 된 모범 답안의 문단 구분을 남긴다
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
                label = section_match.group(1).strip()
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
            elif section == "SHORT":
                header = SHORT_HEADER_RE.match(line)
                if header:
                    flush()
                    current_number = int(header.group(1))
                    current_lines = [(header.group(2), False)]
                    continue
            elif section == "ESSAY":
                header = _match_essay_header(line)
                if header:
                    flush()
                    current_number = header
                    current_lines = []
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
