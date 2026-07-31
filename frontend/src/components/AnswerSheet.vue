<script setup>
import { computed } from 'vue'

import { CIRCLED } from '../lib/format'

/**
 * OMR 답안지. 실제 시험 답안지처럼 객관식은 마킹 원, 주관식·서술형은
 * 작성 여부만 보이는 칸으로 둔다. 응시 중에는 여기서 바로 마킹할 수 있고,
 * 결과 화면에서는 같은 자리에 빨간펜 채점 결과가 찍힌다.
 */
const props = defineProps({
  questions: { type: Array, required: true },
  answers: { type: Object, required: true }, // { [questionId]: { selected_choice, text_answer } }
  results: { type: Object, default: null }, // 결과 모드: { [questionId]: 'correct'|'wrong'|'ungraded' }
  columns: { type: Number, default: 2 },
})

const emit = defineEmits(['mark', 'jump'])

const readonly = computed(() => props.results !== null)

const groups = computed(() => {
  const perColumn = Math.ceil(props.questions.length / props.columns)
  return Array.from({ length: props.columns }, (_, i) =>
    props.questions.slice(i * perColumn, (i + 1) * perColumn),
  )
})

function isFilled(question) {
  const answer = props.answers[question.id]
  if (!answer) return false
  return question.qtype === 'MC'
    ? answer.selected_choice != null
    : Boolean(answer.text_answer?.trim())
}
</script>

<template>
  <div class="omr">
    <div v-for="(group, index) in groups" :key="index" class="omr__col">
      <div v-for="question in group" :key="question.id" class="row" :class="`row--${results?.[question.id] ?? ''}`">
        <button class="row__num mono" type="button" @click="emit('jump', question.number)">
          {{ question.number }}
        </button>

        <div v-if="question.qtype === 'MC'" class="bubbles">
          <button
            v-for="choice in question.choices"
            :key="choice.id"
            class="bubble"
            :class="{
              'bubble--on': answers[question.id]?.selected_choice === choice.number,
              'bubble--answer': readonly && choice.is_correct,
            }"
            type="button"
            :disabled="readonly"
            :aria-label="`${question.number}번 ${CIRCLED[choice.number - 1]}`"
            @click="emit('mark', question.id, choice.number)"
          >
            {{ choice.number }}
          </button>
        </div>

        <button
          v-else
          class="written"
          :class="{ 'written--on': isFilled(question) }"
          type="button"
          @click="emit('jump', question.number)"
        >
          {{ question.qtype === 'SHORT' ? '주관식' : '서술형' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.omr {
  display: flex;
  gap: 1.1rem;
}

.omr__col {
  flex: 1;
  min-width: 0;
}

.row {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 1px 0;
}

.row__num {
  width: 1.4rem;
  flex: none;
  padding: 0;
  border: 0;
  background: none;
  font-family: var(--mono);
  font-size: 0.6875rem;
  color: var(--ink-3);
  text-align: right;
  cursor: pointer;
  font-variant-numeric: tabular-nums;
}

.row__num:hover {
  color: var(--ink);
}

.bubbles {
  display: flex;
  gap: 2px;
}

.bubble {
  width: 17px;
  height: 17px;
  padding: 0;
  border: 1px solid var(--rule-strong);
  border-radius: 50%;
  background: var(--sheet);
  font-family: var(--mono);
  font-size: 0.5625rem;
  color: var(--ink-3);
  cursor: pointer;
  display: grid;
  place-items: center;
  transition: background 0.1s, color 0.1s;
}

.bubble:hover:not(:disabled) {
  border-color: var(--ink-2);
}

.bubble--on {
  background: var(--ink);
  border-color: var(--ink);
  color: var(--paper);
}

.bubble:disabled {
  cursor: default;
}

/* 채점 모드: 정답 자리에 빨간 테두리를 둘러 준다 */
.bubble--answer {
  border-color: var(--red);
  border-width: 1.5px;
  color: var(--red);
}

.bubble--answer.bubble--on {
  background: var(--red);
  border-color: var(--red);
  color: #fff;
}

.written {
  height: 17px;
  padding: 0 0.4rem;
  border: 1px solid var(--rule-strong);
  border-radius: 2px;
  background: var(--sheet);
  font-family: var(--mono);
  font-size: 0.5625rem;
  color: var(--ink-3);
  cursor: pointer;
}

.written--on {
  background: var(--ink);
  border-color: var(--ink);
  color: var(--paper);
}

.row--wrong .row__num {
  color: var(--red);
  font-weight: 700;
}
</style>
