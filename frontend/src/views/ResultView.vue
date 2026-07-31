<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

import AnswerSheet from '../components/AnswerSheet.vue'
import GradeMark from '../components/GradeMark.vue'
import MarkdownBlock from '../components/MarkdownBlock.vue'
import QuestionHead from '../components/QuestionHead.vue'
import RubricGrader from '../components/RubricGrader.vue'
import SolutionPanel from '../components/SolutionPanel.vue'
import { CIRCLED, TYPE_LABEL, formatClock, formatPoints } from '../lib/format'
import { gradeAnswer, getAttempt } from '../api/client'

const props = defineProps({ attemptId: { type: [String, Number], required: true } })

const attempt = ref(null)
const loading = ref(true)
const error = ref('')
const onlyWrong = ref(false)

onMounted(async () => {
  try {
    attempt.value = await getAttempt(props.attemptId)
  } catch {
    error.value = '결과를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
})

const total = computed(
  () => Number(attempt.value?.auto_score ?? 0) + Number(attempt.value?.self_score ?? 0),
)

const pendingEssays = computed(
  () => attempt.value?.answers.filter((a) => a.is_correct === null).length ?? 0,
)

/** 유형별 득점 — 어디서 무너졌는지 한눈에 */
const byType = computed(() => {
  const buckets = {}
  for (const answer of attempt.value?.answers ?? []) {
    const type = answer.question.qtype
    buckets[type] ??= { earned: 0, possible: 0, correct: 0, count: 0 }
    buckets[type].earned += Number(answer.awarded_points)
    buckets[type].possible += Number(answer.question.points)
    buckets[type].count += 1
    if (answer.is_correct) buckets[type].correct += 1
  }
  return buckets
})

const visibleAnswers = computed(() => {
  const list = attempt.value?.answers ?? []
  return onlyWrong.value ? list.filter((a) => a.is_correct !== true) : list
})

const sheetQuestions = computed(() => (attempt.value?.answers ?? []).map((a) => a.question))

const sheetAnswers = computed(() =>
  Object.fromEntries(
    (attempt.value?.answers ?? []).map((a) => [
      a.question.id,
      { selected_choice: a.selected_choice, text_answer: a.text_answer },
    ]),
  ),
)

const sheetResults = computed(() =>
  Object.fromEntries(
    (attempt.value?.answers ?? []).map((a) => [a.question.id, markState(a)]),
  ),
)

function markState(answer) {
  if (answer.is_correct === true) return 'correct'
  if (answer.is_correct === false) return 'wrong'
  return 'ungraded'
}

function jump(number) {
  document.getElementById(`a${number}`)?.scrollIntoView({ block: 'start' })
}

/** 자동 채점이 틀렸다고 본 주관식을 정답으로 되돌린다 */
async function applyGrade(answer, payload) {
  const updated = await gradeAnswer(answer.id, payload)
  answer.is_correct = updated.is_correct
  answer.awarded_points = updated.awarded_points
  answer.graded_by = updated.graded_by
  attempt.value.auto_score = updated.auto_score
  attempt.value.self_score = updated.self_score
}

const acceptShort = (answer) =>
  applyGrade(answer, { is_correct: true, awarded_points: answer.question.points })

const rejectShort = (answer) => applyGrade(answer, { is_correct: false, awarded_points: '0' })
</script>

<template>
  <div class="wrap">
    <p v-if="loading" class="empty">채점 결과를 불러오는 중…</p>
    <p v-else-if="error" class="empty">{{ error }}</p>

    <template v-else>
      <!-- 점수: 채점된 시험지 맨 위에 찍히는 빨간 숫자 -->
      <section class="score">
        <div class="score__main">
          <p class="eyebrow">{{ attempt.exam_title }}</p>
          <p class="score__value mono">
            <span class="score__earned">{{ formatPoints(total) }}</span>
            <span class="score__max">/ 100</span>
          </p>
          <p class="score__meta mono">
            소요 {{ formatClock(attempt.elapsed_sec) }}
            <template v-if="pendingEssays">
              <span class="score__dot">·</span>
              <span class="score__pending">서술형 {{ pendingEssays }}문항 자기채점 전</span>
            </template>
          </p>
        </div>

        <dl class="breakdown">
          <div v-for="(bucket, type) in byType" :key="type" class="breakdown__item">
            <dt class="eyebrow">{{ TYPE_LABEL[type] }}</dt>
            <dd class="mono">
              <strong>{{ formatPoints(bucket.earned) }}</strong
              >/{{ formatPoints(bucket.possible) }}점
              <span class="breakdown__sub">{{ bucket.correct }}/{{ bucket.count }}문항</span>
            </dd>
          </div>
        </dl>
      </section>

      <div class="body">
        <div class="review">
          <div class="review__bar">
            <label class="toggle">
              <input v-model="onlyWrong" type="checkbox" />
              <span>맞은 문항 숨기기</span>
            </label>
            <RouterLink class="btn" :to="{ name: 'study', params: { id: attempt.exam } }">
              문제집으로 복습
            </RouterLink>
          </div>

          <article
            v-for="answer in visibleAnswers"
            :key="answer.id"
            :id="`a${answer.question.number}`"
            class="a"
          >
            <div class="a__mark">
              <GradeMark :state="markState(answer)" />
            </div>

            <div class="a__body">
              <QuestionHead :question="answer.question">
                <span class="a__got mono" :class="{ 'a__got--zero': !Number(answer.awarded_points) }">
                  {{ formatPoints(answer.awarded_points) }}점
                </span>
              </QuestionHead>

              <MarkdownBlock :source="answer.question.body" />

              <ol v-if="answer.question.choices.length" class="choices">
                <li
                  v-for="choice in answer.question.choices"
                  :key="choice.id"
                  class="choice"
                  :class="{
                    'choice--answer': choice.is_correct,
                    'choice--picked': answer.selected_choice === choice.number,
                  }"
                >
                  <span class="choice__num mono">{{ CIRCLED[choice.number - 1] }}</span>
                  <MarkdownBlock class="choice__text" :source="choice.text" />
                  <span v-if="answer.selected_choice === choice.number" class="choice__flag mono">
                    내 답
                  </span>
                </li>
              </ol>

              <div v-else class="mine">
                <p class="eyebrow">내가 쓴 답</p>
                <p v-if="answer.text_answer.trim()" class="mine__text">{{ answer.text_answer }}</p>
                <p v-else class="mine__blank">쓰지 않음</p>
              </div>

              <SolutionPanel :question="answer.question" />

              <!-- 주관식 키워드 채점이 어긋났을 때 손으로 바로잡는다 -->
              <div v-if="answer.question.qtype === 'SHORT'" class="fix">
                <button v-if="!answer.is_correct" class="btn" type="button" @click="acceptShort(answer)">
                  정답으로 인정
                </button>
                <button v-else-if="answer.graded_by === 'SELF'" class="btn" type="button" @click="rejectShort(answer)">
                  인정 취소
                </button>
              </div>

              <RubricGrader
                v-if="answer.question.qtype === 'ESSAY'"
                :answer="answer"
                :on-grade="(payload) => applyGrade(answer, payload)"
              />
            </div>
          </article>

          <p v-if="!visibleAnswers.length" class="empty">틀린 문항이 없습니다.</p>
        </div>

        <aside class="sheet-col">
          <div class="omr-card">
            <p class="eyebrow omr-card__title">채점된 답안지</p>
            <AnswerSheet
              :questions="sheetQuestions"
              :answers="sheetAnswers"
              :results="sheetResults"
              @jump="jump"
            />
          </div>
        </aside>
      </div>
    </template>
  </div>
</template>

<style scoped>
.score {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 2rem;
  flex-wrap: wrap;
  padding: 2.5rem 0 1.5rem;
  border-bottom: 2px solid var(--ink);
}

.score__value {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  margin: 0.4rem 0 0.3rem;
  font-variant-numeric: tabular-nums;
}

.score__earned {
  font-size: clamp(3rem, 11vw, 4.5rem);
  font-weight: 700;
  letter-spacing: -0.06em;
  line-height: 1;
  color: var(--red);
}

.score__max {
  font-size: 1.25rem;
  color: var(--ink-3);
  letter-spacing: -0.03em;
}

.score__meta {
  font-size: 0.75rem;
  color: var(--ink-3);
  margin: 0;
}

.score__dot {
  padding: 0 0.3rem;
}

.score__pending {
  color: var(--red);
}

.breakdown {
  display: flex;
  gap: 1.75rem;
  margin: 0;
  padding-bottom: 0.3rem;
}

.breakdown__item dd {
  margin: 0.15rem 0 0;
  font-size: 0.8125rem;
  font-variant-numeric: tabular-nums;
}

.breakdown__item strong {
  font-size: 1rem;
}

.breakdown__sub {
  display: block;
  font-size: 0.6875rem;
  color: var(--ink-3);
}

.body {
  display: flex;
  align-items: flex-start;
  gap: 2.5rem;
  padding-bottom: 5rem;
}

.review {
  flex: 1;
  min-width: 0;
  max-width: 46rem;
}

.review__bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.9rem 0;
  border-bottom: 1px solid var(--rule);
}

.toggle {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.8125rem;
  color: var(--ink-2);
  cursor: pointer;
}

.a {
  display: flex;
  gap: 1rem;
  padding: 1.75rem 0;
  border-bottom: 1px solid var(--rule);
}

.a__mark {
  width: 34px;
  flex: none;
  padding-top: 0.1rem;
}

.a__body {
  flex: 1;
  min-width: 0;
}

.a__got {
  font-size: 0.6875rem;
  margin-left: auto;
  font-weight: 600;
}

.a__got--zero {
  color: var(--ink-3);
  font-weight: 400;
}

.choices {
  list-style: none;
  margin: 1rem 0 0;
  padding: 0;
}

.choice {
  display: flex;
  gap: 0.55rem;
  align-items: baseline;
  padding: 0.3rem 0.5rem;
  border-radius: 3px;
  border-left: 2px solid transparent;
}

.choice--answer {
  background: var(--marker);
}

/* 내가 고른 답에는 빨간 세로줄 — 채점자의 표시 */
.choice--picked {
  border-left-color: var(--red);
}

.choice__num {
  flex: none;
  color: var(--ink-3);
}

.choice--answer .choice__num {
  color: var(--ink);
  font-weight: 700;
}

.choice__text {
  flex: 1;
  min-width: 0;
}

.choice__flag {
  flex: none;
  font-size: 0.625rem;
  color: var(--red);
  letter-spacing: 0.04em;
}

.mine {
  margin-top: 1rem;
  padding: 0.7rem 0.9rem;
  border: 1px solid var(--rule);
  border-left: 2px solid var(--red);
  border-radius: 0 3px 3px 0;
  background: var(--sheet);
}

.mine__text {
  margin: 0.3rem 0 0;
  font-size: 0.875rem;
  white-space: pre-wrap;
}

.mine__blank {
  margin: 0.3rem 0 0;
  font-size: 0.875rem;
  color: var(--ink-3);
}

.fix {
  margin-top: 0.9rem;
}

.sheet-col {
  width: 15rem;
  flex: none;
  position: sticky;
  top: 4.5rem;
  padding-top: 1.5rem;
}

.omr-card {
  padding: 0.85rem 0.9rem 1rem;
  background: var(--sheet);
  border: 1px solid var(--rule-strong);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

.omr-card__title {
  margin: 0 0 0.6rem;
  padding-bottom: 0.45rem;
  border-bottom: 1px solid var(--rule);
}

@media (max-width: 900px) {
  .body {
    display: block;
  }

  .sheet-col {
    display: none;
  }

  .review {
    max-width: none;
  }
}

@media (max-width: 560px) {
  .breakdown {
    gap: 1.25rem;
  }
}
</style>
