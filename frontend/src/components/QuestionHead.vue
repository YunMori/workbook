<script setup>
import { TYPE_LABEL, DIFFICULTY_LABEL, formatPoints } from '../lib/format'

defineProps({
  question: { type: Object, required: true },
})
</script>

<template>
  <div class="head">
    <span class="head__number mono">{{ String(question.number).padStart(2, '0') }}</span>
    <span class="tag">{{ TYPE_LABEL[question.qtype] }}</span>
    <span class="tag">{{ DIFFICULTY_LABEL[question.difficulty] }}</span>
    <span class="head__points mono">{{ formatPoints(question.points) }}점</span>
    <slot />
  </div>
</template>

<style scoped>
.head {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-bottom: 0.85rem;
}

/* 문항 번호가 페이지의 뼈대 — 크고 무겁게 */
.head__number {
  font-size: 1.15rem;
  font-weight: 700;
  letter-spacing: -0.05em;
  margin-right: 0.25rem;
  font-variant-numeric: tabular-nums;
}

.head__points {
  font-size: 0.6875rem;
  color: var(--ink-3);
  margin-left: auto;
}
</style>
