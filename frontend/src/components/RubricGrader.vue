<script setup>
import { computed, ref, watch } from 'vue'

import MarkdownBlock from './MarkdownBlock.vue'
import { formatPoints } from '../lib/format'

/**
 * 서술형 자기채점. 채점 기준 항목을 체크하면 부분점수가 합산된다.
 * 자동 채점이 닿지 않는 영역이라 판단은 사람이 한다.
 */
const props = defineProps({
  answer: { type: Object, required: true },
  // emit은 await할 수 없어서, 저장이 끝날 때까지 버튼을 잠그려면 함수를 직접 받는다.
  onGrade: { type: Function, required: true },
})

const rubric = computed(() => props.answer.question.solution?.rubric ?? [])
const checked = ref(new Set())
const saving = ref(false)

// 이미 채점한 기록이 있으면 앞에서부터 점수만큼 되살린다.
watch(
  () => props.answer.id,
  () => {
    checked.value = new Set()
    if (props.answer.graded_by !== 'SELF') return
    let remaining = Number(props.answer.awarded_points)
    rubric.value.forEach((item, index) => {
      if (remaining >= Number(item.points) && Number(item.points) > 0) {
        checked.value.add(index)
        remaining -= Number(item.points)
      }
    })
  },
  { immediate: true },
)

const total = computed(() =>
  rubric.value.reduce((sum, item, i) => sum + (checked.value.has(i) ? Number(item.points) : 0), 0),
)

function toggle(index) {
  const next = new Set(checked.value)
  next.has(index) ? next.delete(index) : next.add(index)
  checked.value = next
}

async function save() {
  saving.value = true
  const points = total.value
  const max = Number(props.answer.question.points)
  try {
    await props.onGrade({
      is_correct: points >= max,
      awarded_points: points.toFixed(1),
    })
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="grader">
    <p class="eyebrow">자기채점 — 해당하는 항목을 고르세요</p>

    <ul class="items">
      <li v-for="(item, index) in rubric" :key="index">
        <label class="item" :class="{ 'item--on': checked.has(index) }">
          <input type="checkbox" :checked="checked.has(index)" @change="toggle(index)" />
          <span class="item__points mono">{{ formatPoints(item.points) }}점</span>
          <MarkdownBlock class="item__criteria" :source="item.criteria" />
        </label>
      </li>
    </ul>

    <div class="grader__foot">
      <span class="grader__total mono">
        {{ formatPoints(total) }} / {{ formatPoints(answer.question.points) }}점
      </span>
      <button class="btn" type="button" :disabled="saving" @click="save">
        {{ saving ? '반영하는 중…' : '점수 반영' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.grader {
  margin-top: 1rem;
  padding: 0.9rem 1.1rem;
  border: 1px dashed var(--rule-strong);
  border-radius: var(--radius);
}

.items {
  list-style: none;
  margin: 0.6rem 0 0;
  padding: 0;
}

.item {
  display: flex;
  gap: 0.6rem;
  align-items: baseline;
  padding: 0.45rem 0.5rem;
  border-radius: 3px;
  font-size: 0.8125rem;
  cursor: pointer;
}

.item:hover {
  background: var(--code-bg);
}

.item--on {
  background: var(--marker);
}

.item__points {
  flex: none;
  width: 2.4rem;
  color: var(--ink-3);
  font-variant-numeric: tabular-nums;
}

.item--on .item__points {
  color: var(--ink);
  font-weight: 700;
}

.item__criteria {
  flex: 1;
  min-width: 0;
}

.grader__foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 0.9rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--rule);
}

.grader__total {
  font-size: 1rem;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}
</style>
