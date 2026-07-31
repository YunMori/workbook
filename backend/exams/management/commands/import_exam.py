"""마크다운 모의고사를 DB로 가져오는 명령어.

    python manage.py import_exam                     # settings.EXAM_SOURCE_DIR 전체
    python manage.py import_exam ../data/exams       # 디렉터리 지정
    python manage.py import_exam a_문제.md a_정답해설.md
    python manage.py import_exam --dry-run           # 파싱 결과만 확인
    python manage.py import_exam --update            # 이미 있는 버전을 덮어쓰기
"""

import json
import unicodedata
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from exams.models import Choice, Exam, Question, QuestionType, Solution
from exams.parsers.markdown_exam import parse_questions, parse_solutions

QUESTION_SUFFIX = "_문제.md"
SOLUTION_SUFFIX = "_정답해설.md"
OVERRIDES_FILE = "overrides.json"


def nfc(value):
    """macOS는 파일명을 NFD로 저장한다. 한글 접미사 비교 전에 NFC로 통일."""
    return unicodedata.normalize("NFC", str(value))


class Command(BaseCommand):
    help = "문제/정답해설 마크다운을 파싱해 시험·문항·해설을 등록한다."

    def add_arguments(self, parser):
        parser.add_argument("paths", nargs="*", help="디렉터리 또는 마크다운 파일 경로")
        parser.add_argument("--dry-run", action="store_true", help="DB에 쓰지 않고 파싱 결과만 출력")
        parser.add_argument("--update", action="store_true", help="이미 등록된 버전을 지우고 다시 등록")

    def handle(self, *args, **options):
        pairs = self._collect_pairs(options["paths"])
        if not pairs:
            raise CommandError("가져올 문제 파일을 찾지 못했습니다.")
        self.overrides = self._load_overrides(options["paths"])

        imported = skipped = 0
        for question_path, solution_path in pairs:
            result = self._import_pair(question_path, solution_path, options)
            imported += result == "imported"
            skipped += result == "skipped"

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(f"완료: {imported}개 등록, {skipped}개 건너뜀")
            if not options["dry_run"]
            else self.style.WARNING("--dry-run 이므로 DB에 저장하지 않았습니다.")
        )

    def _collect_pairs(self, paths):
        """`*_문제.md` 와 짝이 되는 `*_정답해설.md` 를 접두사로 묶는다."""
        if not paths:
            paths = [settings.EXAM_SOURCE_DIR]

        candidates = []
        for raw in paths:
            path = Path(raw)
            if path.is_dir():
                candidates.extend(sorted(path.iterdir()))
            elif path.exists():
                candidates.append(path)
            else:
                raise CommandError(f"경로를 찾을 수 없습니다: {path}")

        questions = {}
        solutions = {}
        for path in candidates:
            name = nfc(path.name)
            if name.endswith(QUESTION_SUFFIX):
                questions[name[: -len(QUESTION_SUFFIX)]] = path
            elif name.endswith(SOLUTION_SUFFIX):
                solutions[name[: -len(SOLUTION_SUFFIX)]] = path

        pairs = []
        for prefix, question_path in sorted(questions.items()):
            solution_path = solutions.get(prefix)
            if solution_path is None:
                self.stderr.write(self.style.WARNING(f"정답해설 파일 없음, 건너뜀: {prefix}"))
                continue
            pairs.append((question_path, solution_path))
        return pairs

    def _load_overrides(self, paths):
        """overrides.json — 파서가 지문과 구분할 수 없는 손글씨 답안 등을 문항 단위로 덮어쓴다."""
        directories = [Path(p) for p in paths if Path(p).is_dir()] or [Path(settings.EXAM_SOURCE_DIR)]
        for directory in directories:
            path = directory / OVERRIDES_FILE
            if path.exists():
                data = json.loads(path.read_text(encoding="utf-8"))
                return {k: v for k, v in data.items() if not k.startswith("_")}
        return {}

    def _import_pair(self, question_path, solution_path, options):
        parsed = parse_questions(question_path.read_text(encoding="utf-8"))
        solved = parse_solutions(solution_path.read_text(encoding="utf-8"))
        meta = parsed["meta"]
        questions = parsed["questions"]

        applied = self._apply_overrides(meta, questions)
        label = f"{meta['round']}차 V{meta['version']}"
        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING(f"■ {label}  ({nfc(question_path.name)})"))

        for message in self._validate(questions, solved):
            self.stderr.write(self.style.ERROR(f"  ✗ {message}"))

        counts = {t: sum(1 for q in questions if q["qtype"] == t) for t in ("MC", "SHORT", "ESSAY")}
        self.stdout.write(
            f"  문항 {len(questions)}개 (객관식 {counts['MC']} / 주관식 {counts['SHORT']} / "
            f"서술형 {counts['ESSAY']}), 배점 합계 {sum(q['points'] for q in questions):g}점"
        )
        if applied:
            self.stdout.write(f"  overrides.json 적용: {', '.join(f'{n}번' for n in applied)}")
        for warning in solved["warnings"]:
            self.stdout.write(self.style.WARNING(f"  🔧 {warning}"))

        if options["dry_run"]:
            return "dry-run"

        existing = Exam.objects.filter(round=meta["round"], version=meta["version"]).first()
        if existing and not options["update"]:
            self.stdout.write(self.style.WARNING("  이미 등록됨 — 덮어쓰려면 --update"))
            return "skipped"

        with transaction.atomic():
            self._write(meta, questions, solved, existing)
        self.stdout.write(self.style.SUCCESS("  ✓ 저장 완료"))
        return "imported"

    def _apply_overrides(self, meta, questions):
        entries = self.overrides.get(f"{meta['round']}-{meta['version']}", {})
        applied = []
        for question in questions:
            entry = entries.get(str(question["number"]))
            if not entry:
                continue
            question.update(entry)
            applied.append(question["number"])
        return applied

    def _validate(self, questions, solved):
        """구조가 무너진 파싱을 조용히 넘기지 않도록 확인한다."""
        problems = []
        numbers = [q["number"] for q in questions]
        if numbers != sorted(numbers) or len(set(numbers)) != len(numbers):
            problems.append("문항 번호가 중복되거나 순서가 어긋납니다.")
        for question in questions:
            if question["qtype"] == QuestionType.MULTIPLE_CHOICE:
                if len(question["choices"]) != 4:
                    problems.append(f"{question['number']}번 선택지가 {len(question['choices'])}개")
                if question["number"] not in solved["answers"]:
                    problems.append(f"{question['number']}번 정답을 정답표에서 찾지 못함")
            if not question["body"].strip():
                problems.append(f"{question['number']}번 지문이 비어 있음")
        return problems

    def _write(self, meta, questions, solved, existing):
        exam, _ = Exam.objects.update_or_create(
            round=meta["round"],
            version=meta["version"],
            defaults={
                # 화면에 그대로 노출되는 이름. 원본 마크다운 제목은 너무 길어 쓰지 않는다.
                "title": f"모의고사 {meta['version']}",
                "scope": meta["scope"],
                "time_limit_min": meta["time_limit_min"],
                "total_score": meta["total_score"],
                "order": meta["version"],
            },
        )
        exam.questions.all().delete()  # 문항을 통째로 다시 만든다(선택지·해설은 cascade)

        for item in questions:
            number = item["number"]
            question = Question.objects.create(
                exam=exam,
                number=number,
                qtype=item["qtype"],
                difficulty=item["difficulty"],
                body=item["body"],
                points=item["points"],
            )

            correct = solved["answers"].get(number)
            Choice.objects.bulk_create(
                Choice(
                    question=question,
                    number=choice["number"],
                    text=choice["text"],
                    is_correct=choice["number"] == correct,
                )
                for choice in item["choices"]
            )

            solution = {"explanation": "", "needs_review": False}
            if item["qtype"] == QuestionType.MULTIPLE_CHOICE:
                solution["explanation"] = solved["explanations"].get(number, "")
            elif item["qtype"] == QuestionType.SHORT_ANSWER:
                data = solved["short"].get(number, {})
                solution.update(
                    explanation=data.get("explanation", ""),
                    accepted_answers=data.get("accepted_answers", []),
                    required_keywords=data.get("required_keywords", []),
                    needs_review=data.get("needs_review", True),
                )
            else:
                data = solved["essay"].get(number, {})
                solution.update(
                    explanation=data.get("explanation", ""),
                    model_answer=data.get("model_answer", ""),
                    rubric=data.get("rubric", []),
                )
            Solution.objects.create(question=question, **solution)
