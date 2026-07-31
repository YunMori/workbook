<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

import AnswerSheet from '../components/AnswerSheet.vue'
import MarkdownBlock from '../components/MarkdownBlock.vue'
import QuestionHead from '../components/QuestionHead.vue'
import { CIRCLED, formatClock } from '../lib/format'
import { startAttempt, submitAttempt } from '../api/client'
import { useExamStore } from '../stores/exams'
import { useSessionStore } from '../stores/session'

const props = defineProps({ id: { type: [String, Number], required: true } })

const router = useRouter()
const examStore = useExamStore()
const session = useSessionStore()

const exam = ref(null)
const attemptId = ref(null)
const startedAt = ref(Date.now())
const now = ref(Date.now())
const loading = ref(true)
const error = ref('')
const submitting = ref(false)
const confirming = ref(false)
const autoSubmitted = ref(false)

const answers = reactive({}) // { [questionId]: { selected_choice, text_answer } }
let ticker = null

// 실패 원인을 한 줄로. 응답이 없으면 서버가 죽은 것이고, 있으면 상태 코드가 원인을 가리킨다.
function describe(e) {
  const status = e?.response?.status
  if (!status) return '백엔드 서버에 연결하지 못했습니다.'
  if (status === 403) {
    return '서버가 요청을 거부했습니다 (403). 관리자 로그인 세션을 지우고 다시 시도해 보세요.'
  }
  const detail = e.response.data?.detail
  return `서버 응답 ${status}${detail ? ` — ${detail}` : ''}`
}

const elapsedSec = computed(() => Math.floor((now.value - startedAt.value) / 1000))
const remainingSec = computed(() => (exam.value?.time_limit_min ?? 60) * 60 - elapsedSec.value)
const overtime = computed(() => remainingSec.value < 0)
const lowTime = computed(() => remainingSec.value >= 0 && remainingSec.value <= 300)

const answeredCount = computed(
  () =>
    exam.value?.questions.filter((q) => {
      const answer = answers[q.id]
      if (!answer) return false
      return q.qtype === 'MC' ? answer.selected_choice != null : Boolean(answer.text_answer?.trim())
    }).length ?? 0,
)

const unanswered = computed(
  () =>
    exam.value?.questions
      .filter((q) => {
        const answer = answers[q.id]
        if (!answer) return true
        return q.qtype === 'MC'
          ? answer.selected_choice == null
          : !answer.text_answer?.trim()
      })
      .map((q) => q.number) ?? [],
)

onMounted(async () => {
  try {
    exam.value = await examStore.loadExam(props.id)
    for (const question of exam.value.questions) {
      answers[question.id] = { selected_choice: null, text_answer: '' }
    }

    // 새로고침해도 이어서 풀 수 있게 진행 중이던 응시를 복구한다.
    const draft = session.loadDraft(props.id)
    if (draft?.attemptId) {
      attemptId.value = draft.attemptId
      startedAt.value = draft.startedAt
      Object.assign(answers, draft.answers ?? {})
    } else {
      const attempt = await startAttempt(Number(props.id), session.token)
      attemptId.value = attempt.id
      startedAt.value = Date.now()
      persist()
    }
  } catch (e) {
    // 무엇이 막았는지 화면에 남긴다. 서버가 아니라 브라우저 쪽 문제일 때도 있다.
    error.value = `응시를 시작하지 못했습니다. ${describe(e)}`
  } finally {
    loading.value = false
  }

  ticker = setInterval(() => {
    now.value = Date.now()
    // 권장 시간이 끝나면 실제 시험처럼 그 자리에서 제출한다.
    if (remainingSec.value <= 0 && !submitting.value) {
      autoSubmitted.value = true
      submit()
    }
  }, 1000)
})

onBeforeUnmount(() => clearInterval(ticker))

function persist() {
  if (!attemptId.value) return
  session.saveDraft(props.id, {
    attemptId: attemptId.value,
    startedAt: startedAt.value,
    answers: { ...answers },
  })
}

watch(answers, persist, { deep: true })

function mark(questionId, choiceNumber) {
  const answer = answers[questionId]
  // 같은 번호를 다시 누르면 마킹을 지운다.
  answer.selected_choice = answer.selected_choice === choiceNumber ? null : choiceNumber
}

function jump(number) {
  document.getElementById(`q${number}`)?.scrollIntoView({ block: 'start' })
}

async function submit() {
  if (submitting.value || !attemptId.value) return
  submitting.value = true
  clearInterval(ticker)
  try {
    const payload = Object.entries(answers).map(([questionId, answer]) => ({
      question: Number(questionId),
      selected_choice: answer.selected_choice,
      text_answer: answer.text_answer,
    }))
    await submitAttempt(attemptId.value, payload, Math.max(0, elapsedSec.value))
    session.clearDraft(props.id)
    router.push({ name: 'result', params: { attemptId: attemptId.value } })
  } catch {
    error.value = '제출에 실패했습니다. 다시 시도해 주세요.'
    submitting.value = false
    confirming.value = false
  }
}
</script>

<template>
  <p v-if="loading" class="empty">응시를 준비하는 중…</p>
  <p v-else-if="error" class="empty">{{ error }}</p>

  <template v-else>
    <header class="bar">
      <div class="wrap bar__inner">
        <div class="bar__id mono">
          <strong>{{ exam.title }}</strong>
        </div>

        <div class="clock mono" :class="{ 'clock--low': lowTime, 'clock--over': overtime }">
          <span class="clock__label">{{ autoSubmitted ? '시간 종료' : '남은 시간' }}</span>
          <time>{{ formatClock(Math.max(0, remainingSec)) }}</time>
        </div>

        <div class="bar__right">
          <span class="progress mono">{{ answeredCount }} / {{ exam.questions.length }}</span>
          <button class="btn btn--solid" type="button" @click="confirming = true">제출하기</button>
        </div>
      </div>
    </header>

    <div class="wrap layout">
      <div class="paper">
        <article v-for="question in exam.questions" :key="question.id" :id="`q${question.number}`" class="q">
          <QuestionHead :question="question" />
          <MarkdownBlock :source="question.body" />

          <ol v-if="question.choices.length" class="choices">
            <li v-for="choice in question.choices" :key="choice.id">
              <label class="choice" :class="{ 'choice--on': answers[question.id].selected_choice === choice.number }">
                <input
                  class="choice__input"
                  type="radio"
                  :name="`q${question.id}`"
                  :value="choice.number"
                  :checked="answers[question.id].selected_choice === choice.number"
                  @click="mark(question.id, choice.number)"
                />
                <span class="choice__num mono">{{ CIRCLED[choice.number - 1] }}</span>
                <MarkdownBlock class="choice__text" :source="choice.text" />
              </label>
            </li>
          </ol>

          <input
            v-else-if="question.qtype === 'SHORT'"
            v-model="answers[question.id].text_answer"
            class="field"
            type="text"
            placeholder="답을 쓰세요"
            :aria-label="`${question.number}번 답`"
          />

          <textarea
            v-else
            v-model="answers[question.id].text_answer"
            class="field field--long"
            rows="6"
            placeholder="답을 쓰세요"
            :aria-label="`${question.number}번 답`"
          ></textarea>
        </article>
      </div>

      <aside class="sheet-col">
        <div class="omr-card">
          <p class="eyebrow omr-card__title">답안지</p>
          <AnswerSheet :questions="exam.questions" :answers="answers" @mark="mark" @jump="jump" />
        </div>
      </aside>
    </div>

    <!-- 제출 확인 -->
    <div v-if="confirming" class="overlay" @click.self="confirming = false">
      <div class="dialog sheet" role="dialog" aria-modal="true" aria-labelledby="submit-title">
        <h2 id="submit-title" class="dialog__title">제출하면 채점 결과가 바로 나옵니다.</h2>
        <p class="dialog__body">
          {{ exam.questions.length }}문항 중 <strong>{{ answeredCount }}문항</strong>에 답했습니다.
        </p>
        <p v-if="unanswered.length" class="dialog__warn mono">
          비어 있는 문항 — {{ unanswered.join(', ') }}
        </p>
        <div class="dialog__actions">
          <button class="btn" type="button" @click="confirming = false">더 풀기</button>
          <button class="btn btn--solid" type="button" :disabled="submitting" @click="submit">
            {{ submitting ? '채점하는 중…' : '제출하기' }}
          </button>
        </div>
      </div>
    </div>
  </template>
</template>

<style scoped>
.bar {
  position: sticky;
  top: 0;
  z-index: 20;
  background: var(--sheet);
  border-bottom: 2px solid var(--ink);
}

.bar__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  height: 3.75rem;
}

.bar__id {
  display: flex;
  align-items: baseline;
  gap: 0.45rem;
  font-size: 0.75rem;
  color: var(--ink-3);
}

.bar__id strong {
  font-size: 1rem;
  color: var(--ink);
  letter-spacing: -0.04em;
}

/* 타이머는 시험지의 심장 — 화면에서 가장 큰 숫자 */
.clock {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  font-variant-numeric: tabular-nums;
}

.clock__label {
  font-size: 0.625rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--ink-3);
}

.clock time {
  font-size: 1.5rem;
  font-weight: 600;
  letter-spacing: -0.04em;
}

.clock--low time,
.clock--over time {
  color: var(--red);
}

.clock--over .clock__label {
  color: var(--red);
}

.bar__right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.progress {
  font-size: 0.8125rem;
  color: var(--ink-3);
  font-variant-numeric: tabular-nums;
}

.layout {
  display: flex;
  align-items: flex-start;
  gap: 2.5rem;
  padding-top: 1.5rem;
  padding-bottom: 5rem;
}

.paper {
  flex: 1;
  min-width: 0;
  max-width: 46rem;
}

.q {
  padding: 1.75rem 0;
  border-bottom: 1px solid var(--rule);
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
  padding: 0.35rem 0.5rem;
  border: 1px solid transparent;
  border-radius: 3px;
  cursor: pointer;
}

.choice:hover {
  background: var(--code-bg);
}

.choice--on {
  border-color: var(--ink);
  background: var(--code-bg);
}

.choice__input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.choice__input:focus-visible + .choice__num {
  outline: 2px solid var(--syn-key);
  outline-offset: 2px;
}

.choice__num {
  flex: none;
  color: var(--ink-3);
}

.choice--on .choice__num {
  color: var(--ink);
  font-weight: 700;
}

.choice__text {
  flex: 1;
  min-width: 0;
}

.field {
  width: 100%;
  margin-top: 1rem;
  padding: 0.6rem 0.75rem;
  border: 1px solid var(--rule-strong);
  border-radius: var(--radius);
  background: var(--sheet);
  font-size: 0.9375rem;
}

.field--long {
  font-family: var(--sans);
  line-height: 1.7;
  resize: vertical;
}

.sheet-col {
  width: 15rem;
  flex: none;
  position: sticky;
  top: 4.75rem;
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

.overlay {
  position: fixed;
  inset: 0;
  z-index: 40;
  display: grid;
  place-items: center;
  padding: 1.5rem;
  background: rgba(20, 22, 26, 0.45);
}

.dialog {
  width: min(28rem, 100%);
  padding: 1.5rem;
  box-shadow: var(--shadow);
}

.dialog__title {
  font-size: 1.0625rem;
  margin-bottom: 0.6rem;
}

.dialog__body {
  margin: 0 0 0.5rem;
  font-size: 0.875rem;
  color: var(--ink-2);
}

.dialog__warn {
  margin: 0;
  padding: 0.5rem 0.7rem;
  background: var(--red-soft);
  border-radius: 3px;
  font-size: 0.75rem;
  color: var(--red);
}

.dialog__actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1.25rem;
}

@media (max-width: 900px) {
  .layout {
    display: block;
  }

  .sheet-col {
    display: none;
  }

  .paper {
    max-width: none;
  }
}
</style>
