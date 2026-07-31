<script setup>
import MarkdownBlock from './MarkdownBlock.vue'
import { CIRCLED, formatPoints } from '../lib/format'

defineProps({
  question: { type: Object, required: true },
})
</script>

<template>
  <div class="solution">
    <p class="solution__answer">
      <span class="eyebrow">정답</span>
      <template v-if="question.qtype === 'MC'">
        <strong class="mono">{{ CIRCLED[question.correct_choice - 1] }}</strong>
      </template>
      <template v-else-if="question.qtype === 'SHORT'">
        <strong v-if="question.solution?.accepted_answers?.length" class="mono answer-text">
          {{ question.solution.accepted_answers[0] }}
        </strong>
        <span v-else class="solution__none">아래 해설 참고</span>
      </template>
      <span v-else class="solution__none">채점 기준으로 자기채점</span>
    </p>

    <MarkdownBlock
      v-if="question.solution?.explanation"
      class="solution__body"
      :source="question.solution.explanation"
    />

    <template v-if="question.solution?.rubric?.length">
      <p class="eyebrow solution__label">채점 기준</p>
      <ul class="rubric">
        <li v-for="(item, i) in question.solution.rubric" :key="i">
          <span class="rubric__points mono">{{ formatPoints(item.points) }}점</span>
          <MarkdownBlock class="rubric__criteria" :source="item.criteria" />
        </li>
      </ul>
    </template>

    <template v-if="question.solution?.model_answer">
      <p class="eyebrow solution__label">모범 답안</p>
      <MarkdownBlock class="solution__model" :source="question.solution.model_answer" />
    </template>
  </div>
</template>

<style scoped>
/* 정답 영역은 형광펜으로 그은 자리처럼 — 본문과 확실히 구분된다 */
.solution {
  margin-top: 1rem;
  padding: 0.9rem 1.1rem;
  background: var(--code-bg);
  border-left: 3px solid var(--rule-strong);
  border-radius: 0 3px 3px 0;
}

.solution__answer {
  display: flex;
  align-items: baseline;
  gap: 0.6rem;
  margin: 0 0 0.6rem;
  flex-wrap: wrap;
}

.solution__answer strong {
  font-size: 1rem;
  background: var(--marker);
  padding: 0.05rem 0.4rem;
  border-radius: 2px;
}

.answer-text {
  font-size: 0.875rem;
  word-break: break-all;
}

.solution__none {
  font-size: 0.8125rem;
  color: var(--ink-2);
}

.solution__body {
  font-size: 0.875rem;
  color: var(--ink-2);
}

.solution__label {
  margin: 1rem 0 0.4rem;
}

.rubric {
  list-style: none;
  margin: 0;
  padding: 0;
  border-top: 1px solid var(--rule);
}

.rubric li {
  display: flex;
  gap: 0.7rem;
  padding: 0.4rem 0;
  border-bottom: 1px solid var(--rule);
  font-size: 0.8125rem;
}

.rubric__points {
  flex: none;
  width: 2.6rem;
  color: var(--ink-3);
  font-variant-numeric: tabular-nums;
}

.rubric__criteria {
  color: var(--ink-2);
}

.solution__model {
  font-size: 0.875rem;
  padding: 0.7rem 0.9rem;
  background: var(--sheet);
  border: 1px solid var(--rule);
  border-radius: 3px;
}
</style>
