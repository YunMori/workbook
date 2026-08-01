import unicodedata
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase

from exams.parsers.markdown_exam import parse_questions, parse_solutions

QUESTION_MD = """# Vue.js & JavaScript 모의고사 (2차) — Version 9

> 출제 범위: Basic_Syntax / DOM_Event
> 문항 수: 3문항
> 배점: — **총 100점**
> 권장 시간: 45분

---

## Ⅰ. 객관식 (각 3점, 총 63점)

**1. [기초]** 조건문에서 `false`로 평가되지 **않는** 것은? `1`

① `'0'`  ② `0`  ③ `''`  ④ `NaN`

---

**2. [응용]** 다음 코드의 출력 결과는?

```js
const arr = ['a']
// ① 는 코드블록 안이므로 선택지가 아니다
// --- 도 구분선이 아니다
```

① `a`
② `0`
③ `TypeError`
④ `undefined`

---

## Ⅱ. 주관식 (각 4점, 총 24점)

**3. [기초]** `v-bind`의 shorthand를 쓰시오.

---

## Ⅲ. 서술형 (28번 5점, 29·30번 각 4점, 총 13점)

**28. [응용]** 차이를 서술하시오.

---
"""

SOLUTION_MD = """# 2차 Version 9 — 정답 및 해설

## 빠른 정답표 (객관식)

| 1 | 2 |
|---|---|
| ① | ④ |

---

## Ⅰ. 객관식 해설

**1. 정답 ①** — 빈 문자열만 `false`다.

**2. 정답 ④** — 설명.

---

## Ⅱ. 주관식 해설

**3.** `:` (colon)
- 예: `:src="imageSrc"`

---

## Ⅲ. 서술형 채점 기준

**28. (5점)**

| 배점 | 채점 요소 |
|---|---|
| 3점 | 첫 번째 요소 |
| 2점 | 두 번째 요소 |

**모범 답안**
> 모범 답안 본문이다.
"""


class ParseQuestionsTests(SimpleTestCase):
    def setUp(self):
        self.parsed = parse_questions(QUESTION_MD)
        self.questions = {q["number"]: q for q in self.parsed["questions"]}

    def test_meta(self):
        meta = self.parsed["meta"]
        self.assertEqual(meta["round"], 2)
        self.assertEqual(meta["version"], 9)
        self.assertEqual(meta["time_limit_min"], 45)
        self.assertEqual(meta["total_score"], 100)
        self.assertEqual(meta["scope"], "Basic_Syntax / DOM_Event")

    def test_question_types_and_points(self):
        self.assertEqual(self.questions[1]["qtype"], "MC")
        self.assertEqual(self.questions[1]["points"], 3)
        self.assertEqual(self.questions[3]["qtype"], "SHORT")
        self.assertEqual(self.questions[3]["points"], 4)
        self.assertEqual(self.questions[28]["qtype"], "ESSAY")
        self.assertEqual(self.questions[28]["points"], 5)  # 서술형은 문항별 배점이 다르다

    def test_difficulty(self):
        self.assertEqual(self.questions[1]["difficulty"], "BASIC")
        self.assertEqual(self.questions[2]["difficulty"], "APPLIED")

    def test_choices_on_one_line(self):
        choices = self.questions[1]["choices"]
        self.assertEqual([c["number"] for c in choices], [1, 2, 3, 4])
        self.assertEqual(choices[0]["text"], "`'0'`")
        self.assertEqual(choices[3]["text"], "`NaN`")

    def test_scribbled_answer_is_stripped(self):
        self.assertNotIn("`1`", self.questions[1]["body"])
        self.assertTrue(self.questions[1]["body"].endswith("것은?"))

    def test_code_fence_content_is_not_parsed_as_structure(self):
        question = self.questions[2]
        self.assertIn("// ① 는 코드블록 안이므로", question["body"])
        self.assertIn("// --- 도 구분선이 아니다", question["body"])
        self.assertEqual(len(question["choices"]), 4)


class ParseSolutionsTests(SimpleTestCase):
    def setUp(self):
        self.solved = parse_solutions(SOLUTION_MD)

    def test_answer_table(self):
        self.assertEqual(self.solved["answers"], {1: 1, 2: 4})
        self.assertEqual(self.solved["warnings"], [])

    def test_explanations(self):
        self.assertIn("빈 문자열만", self.solved["explanations"][1])

    def test_short_answer_rules(self):
        rules = self.solved["short"][3]
        self.assertIn(":", rules["accepted_answers"])
        self.assertEqual(rules["required_keywords"], [[":"]])

    def test_essay_rubric_and_model_answer(self):
        essay = self.solved["essay"][28]
        self.assertEqual([r["points"] for r in essay["rubric"]], [3.0, 2.0])
        self.assertEqual(essay["rubric"][0]["criteria"], "첫 번째 요소")
        self.assertEqual(essay["model_answer"], "모범 답안 본문이다.")

    def test_answer_table_and_inline_mismatch_is_reported(self):
        broken = SOLUTION_MD.replace("**2. 정답 ④**", "**2. 정답 ③**")
        warnings = parse_solutions(broken)["warnings"]
        self.assertTrue(any("2번 정답 불일치" in w for w in warnings))


ROUND_01_QUESTION_MD = """# JS DOM과 Event 모의고사 — Version 3

---

## 객관식

**1.** DOM에서 최상위 객체는?

① `window`
② `document`
③ `navigator`
④ 위 ①, ② 모두

---

## 주관식

**41.** 실시간으로 DOM 변경을 반영하는 자료구조의 이름은?

---

## 서술형

**61.** `innerHTML`과 `textContent`의 차이를 설명하시오. (4점)

---
"""

ROUND_01_SOLUTION_MD = """# JS DOM과 Event 모의고사 (Version 3) — 정답 및 해설

## 빠른 정답표 (객관식)

| 1   |
| --- |
| ②   |

---

## 객관식 해설

**1. 정답 ②** — 모든 요소는 `document`의 하위 객체다.

---

## 주관식 해설

- **41.** 정답: HTMLCollection — 구식 선택자들이 반환한다.

---

## 서술형 채점 기준

### 61. innerHTML과 textContent의 차이 (4점)

| 배점 | 채점 요소 |
| --- | --- |
| 2점 | `innerHTML`은 마크업으로 해석되어 XSS에 취약 |
| 2점 | `textContent`는 순수 텍스트로만 처리 |

**모범 답안:** `innerHTML`은 문자열을 HTML로 해석한다.

---
"""


class Round01FormatTests(SimpleTestCase):
    """1차(round 01) 표기 — 로마 숫자 없는 섹션, `### N.` 머리글, 배점 표기 없음."""

    def setUp(self):
        self.parsed = parse_questions(
            ROUND_01_QUESTION_MD, source_name="subject_exam_round_01_모의고사_v3_문제지.md"
        )
        self.questions = {q["number"]: q for q in self.parsed["questions"]}
        self.solved = parse_solutions(ROUND_01_SOLUTION_MD)

    def test_round_comes_from_file_name_when_title_omits_it(self):
        self.assertEqual(self.parsed["meta"]["round"], 1)
        self.assertEqual(self.parsed["meta"]["version"], 3)
        self.assertEqual(self.parsed["meta"]["subject"], "JS DOM과 Event")

    def test_sections_without_roman_numeral_or_points(self):
        self.assertEqual(self.questions[1]["qtype"], "MC")
        self.assertEqual(self.questions[41]["qtype"], "SHORT")
        self.assertEqual(self.questions[61]["qtype"], "ESSAY")

    def test_choice_text_may_mention_other_choice_numbers(self):
        choices = self.questions[1]["choices"]
        self.assertEqual([c["number"] for c in choices], [1, 2, 3, 4])
        self.assertEqual(choices[3]["text"], "위 ①, ② 모두")

    def test_essay_points_come_from_the_stem(self):
        essay = self.questions[61]
        self.assertEqual(essay["points"], 4)
        self.assertNotIn("(4점)", essay["body"])  # 배점은 화면에서 따로 보여 준다

    def test_total_score_falls_back_to_the_sum_of_points(self):
        self.assertEqual(self.parsed["meta"]["total_score"], 11)  # 3 + 4 + 4

    def test_short_answer_written_as_a_bullet(self):
        rules = self.solved["short"][41]
        self.assertEqual(rules["accepted_answers"], ["HTMLCollection"])  # `정답:`과 부연 설명 제거
        self.assertFalse(rules["needs_review"])

    def test_essay_heading_with_inline_model_answer(self):
        essay = self.solved["essay"][61]
        self.assertEqual([r["points"] for r in essay["rubric"]], [2.0, 2.0])
        self.assertEqual(essay["model_answer"], "`innerHTML`은 문자열을 HTML로 해석한다.")


class RealExamFilesTests(SimpleTestCase):
    """data/exams 의 실제 파일이 규격대로 파싱되는지 확인한다."""

    SUFFIXES = (("_문제.md", "_정답해설.md"), ("_문제지.md", "_정답지.md"))

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        source = Path(settings.EXAM_SOURCE_DIR)
        cls.pairs = []
        files = {unicodedata.normalize("NFC", p.name): p for p in source.glob("*.md")}
        for name, path in sorted(files.items()):
            for question_suffix, solution_suffix in cls.SUFFIXES:
                if name.endswith(question_suffix):
                    solution = files.get(name.replace(question_suffix, solution_suffix))
                    cls.pairs.append((name, path, solution))

    def test_all_versions_present(self):
        self.assertEqual(len(self.pairs), 11)  # 2차 5세트 + 1차 6세트
        self.assertTrue(all(solution is not None for _, _, solution in self.pairs))

    def test_structure_of_round_01_files(self):
        """1차는 세트마다 문항 수가 다르므로 규격이 아니라 짝이 맞는지를 본다."""
        pairs = [p for p in self.pairs if "round_01" in p[0]]
        self.assertEqual(len(pairs), 6)
        for name, question_path, solution_path in pairs:
            with self.subTest(version=name):
                parsed = parse_questions(question_path.read_text(encoding="utf-8"), source_name=name)
                solved = parse_solutions(solution_path.read_text(encoding="utf-8"))
                questions = parsed["questions"]

                numbers = [q["number"] for q in questions]
                self.assertEqual(numbers, list(range(1, len(questions) + 1)))
                self.assertEqual(parsed["meta"]["round"], 1)

                for question in questions:
                    number = question["number"]
                    self.assertTrue(question["body"].strip(), f"{number}번 지문 비어 있음")
                    if question["qtype"] == "MC":
                        self.assertEqual(len(question["choices"]), 4, f"{number}번")
                        self.assertIn(number, solved["answers"])
                    elif question["qtype"] == "SHORT":
                        self.assertIn(number, solved["short"], f"{number}번")
                    else:
                        self.assertTrue(solved["essay"].get(number, {}).get("rubric"), f"{number}번")

                self.assertEqual([w for w in solved["warnings"] if "불일치" in w], [])

    def test_structure_of_every_version(self):
        """2차는 5세트 모두 30문항·100점 규격이다."""
        pairs = [p for p in self.pairs if "2차" in p[0]]
        self.assertEqual(len(pairs), 5)
        for name, question_path, solution_path in pairs:
            with self.subTest(version=name):
                parsed = parse_questions(question_path.read_text(encoding="utf-8"))
                solved = parse_solutions(solution_path.read_text(encoding="utf-8"))
                questions = parsed["questions"]

                self.assertEqual(len(questions), 30)
                self.assertEqual([q["number"] for q in questions], list(range(1, 31)))
                self.assertEqual(sum(q["points"] for q in questions), 100)

                by_type = {t: [q for q in questions if q["qtype"] == t] for t in ("MC", "SHORT", "ESSAY")}
                self.assertEqual(len(by_type["MC"]), 21)
                self.assertEqual(len(by_type["SHORT"]), 6)
                self.assertEqual(len(by_type["ESSAY"]), 3)

                for question in by_type["MC"]:
                    self.assertEqual(len(question["choices"]), 4, f"{question['number']}번")
                    self.assertIn(question["number"], solved["answers"])

                for question in questions:
                    self.assertTrue(question["body"].strip(), f"{question['number']}번 지문 비어 있음")

                # 정답표와 개별 해설의 정답이 어긋나면 안 된다.
                mismatches = [w for w in solved["warnings"] if "불일치" in w]
                self.assertEqual(mismatches, [])
