<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

import MarkdownBlock from '../components/MarkdownBlock.vue'
import QuestionHead from '../components/QuestionHead.vue'
import SolutionPanel from '../components/SolutionPanel.vue'
import { CIRCLED, TYPE_LABEL } from '../lib/format'
import { useExamStore } from '../stores/exams'

const props = defineProps({ id: { type: [String, Number], required: true } })

const store = useExamStore()
const exam = ref(null)
const loading = ref(true)
const error = ref('')

const revealed = ref(new Set())
const typeFilter = ref('ALL')
const difficultyFilter = ref('ALL')
const query = ref('')

onMounted(async () => {
  try {
    exam.value = await store.loadExam(props.id, { withSolutions: true })
  } catch {
    error.value = '문제를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
})

const questions = computed(() => {
  const list = exam.value?.questions ?? []
  const needle = query.value.trim().toLowerCase()
  return list.filter((q) => {
    if (typeFilter.value !== 'ALL' && q.qtype !== typeFilter.value) return false
    if (difficultyFilter.value !== 'ALL' && q.difficulty !== difficultyFilter.value) return false
    if (!needle) return true
    const haystack = [q.body, ...q.choices.map((c) => c.text), q.solution?.explanation ?? '']
      .join(' ')
      .toLowerCase()
    return haystack.includes(needle)
  })
})

const allRevealed = computed(
  () => questions.value.length > 0 && questions.value.every((q) => revealed.value.has(q.id)),
)

function toggle(questionId) {
  const next = new Set(revealed.value)
  next.has(questionId) ? next.delete(questionId) : next.add(questionId)
  revealed.value = next
}

function toggleAll() {
  revealed.value = allRevealed.value ? new Set() : new Set(questions.value.map((q) => q.id))
}
</script>

<template>
  <div class="wrap">
    <p v-if="loading" class="empty">불러오는 중…</p>
    <p v-else-if="error" class="empty">{{ error }}</p>

    <template v-else>
      <header class="page-head">
        <div>
          <p class="eyebrow">문제 보기</p>
          <h1 class="page-head__title">{{ exam.title }}</h1>
        </div>
        <RouterLink class="btn btn--solid" :to="{ name: 'take', params: { id } }">
          응시하기
        </RouterLink>
      </header>

      <div class="toolbar">
        <div class="filters">
          <select v-model="typeFilter" class="control mono" aria-label="유형 거르기">
            <option value="ALL">유형 전체</option>
            <option v-for="(label, value) in TYPE_LABEL" :key="value" :value="value">
              {{ label }}
            </option>
          </select>
          <select v-model="difficultyFilter" class="control mono" aria-label="난이도 거르기">
            <option value="ALL">난이도 전체</option>
            <option value="BASIC">기초</option>
            <option value="APPLIED">응용</option>
          </select>
          <input
            v-model="query"
            class="control control--search"
            type="search"
            placeholder="문제·해설 검색"
            aria-label="문제와 해설 검색"
          />
        </div>
        <button class="btn" type="button" @click="toggleAll">
          {{ allRevealed ? '정답 모두 접기' : '정답 모두 펼치기' }}
        </button>
      </div>

      <p class="count mono">{{ questions.length }}문항</p>

      <article v-for="question in questions" :key="question.id" :id="`q${question.number}`" class="q">
        <QuestionHead :question="question" />
        <MarkdownBlock :source="question.body" />

        <ol v-if="question.choices.length" class="choices">
          <li
            v-for="choice in question.choices"
            :key="choice.id"
            class="choice"
            :class="{ 'choice--correct': revealed.has(question.id) && choice.is_correct }"
          >
            <span class="choice__num mono">{{ CIRCLED[choice.number - 1] }}</span>
            <MarkdownBlock class="choice__text" :source="choice.text" />
          </li>
        </ol>

        <button class="reveal" type="button" @click="toggle(question.id)">
          {{ revealed.has(question.id) ? '− 정답 숨기기' : '+ 정답과 해설' }}
        </button>

        <SolutionPanel v-if="revealed.has(question.id)" :question="question" />
      </article>

      <p v-if="!questions.length" class="empty">조건에 맞는 문항이 없습니다.</p>
    </template>
  </div>
</template>

<style scoped>
.page-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
  padding: 2.5rem 0 1.25rem;
}

.page-head__title {
  font-size: 1.4rem;
  font-weight: 700;
  letter-spacing: -0.04em;
  margin-top: 0.2rem;
}

.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  flex-wrap: wrap;
  padding: 0.75rem 0;
  border-top: 2px solid var(--ink);
  border-bottom: 1px solid var(--rule);
  position: sticky;
  top: 3.5rem;
  background: var(--paper);
  z-index: 10;
}

.filters {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.control {
  padding: 0.4rem 0.55rem;
  border: 1px solid var(--rule-strong);
  border-radius: var(--radius);
  background: var(--sheet);
  font-size: 0.8125rem;
}

.control--search {
  min-width: 12rem;
}

.count {
  font-size: 0.75rem;
  color: var(--ink-3);
  margin: 1.25rem 0 0;
}

.q {
  padding: 1.75rem 0;
  border-bottom: 1px solid var(--rule);
  max-width: 46rem;
}

.choices {
  list-style: none;
  margin: 1rem 0 0;
  padding: 0;
}

.choice {
  display: flex;
  gap: 0.55rem;
  padding: 0.3rem 0.45rem;
  border-radius: 3px;
  align-items: baseline;
}

/* 정답 공개는 형광펜 한 줄 — 빨강은 채점에만 쓴다 */
.choice--correct {
  background: var(--marker);
}

.choice__num {
  flex: none;
  color: var(--ink-3);
}

.choice--correct .choice__num {
  color: var(--ink);
  font-weight: 700;
}

.choice__text {
  flex: 1;
  min-width: 0;
}

.reveal {
  margin-top: 1rem;
  padding: 0;
  border: 0;
  background: none;
  font-family: var(--mono);
  font-size: 0.75rem;
  color: var(--ink-3);
  cursor: pointer;
  border-bottom: 1px dashed var(--rule-strong);
}

.reveal:hover {
  color: var(--ink);
}

@media (max-width: 640px) {
  .toolbar {
    position: static;
  }

  .control--search {
    min-width: 0;
    flex: 1;
  }
}
</style>
