<script setup>
/**
 * 빨간펜 채점 표시. 종이에 손으로 그은 것처럼 획이 그려진다.
 * correct → ○,  wrong → ✗,  null → 아직 채점 안 함(서술형)
 */
defineProps({
  state: { type: String, default: 'ungraded' }, // 'correct' | 'wrong' | 'ungraded'
  size: { type: Number, default: 34 },
})
</script>

<template>
  <svg
    class="mark"
    :class="`mark--${state}`"
    :width="size"
    :height="size"
    viewBox="0 0 40 40"
    fill="none"
    aria-hidden="true"
  >
    <!-- 완전한 원이 아니라 살짝 열린 호 — 손으로 그린 동그라미 -->
    <path
      v-if="state === 'correct'"
      class="stroke stroke--circle"
      d="M27.5 8.6C23.4 6 17.4 5.8 12.9 8.4 8 11.2 5.6 17 6.6 22.6c1 5.4 5.4 9.6 10.9 10.4 5.8.8 11.6-2.2 14-7.5 2.3-5.1 1-11.4-3.1-15"
    />
    <template v-else-if="state === 'wrong'">
      <path class="stroke stroke--x1" d="M10.5 10.5 29.5 29.5" />
      <path class="stroke stroke--x2" d="M29.5 10.5 10.5 29.5" />
    </template>
    <path v-else class="stroke stroke--dash" d="M11 20h18" stroke-dasharray="3 4" />
  </svg>
</template>

<style scoped>
.mark {
  flex: none;
  overflow: visible;
}

.stroke {
  stroke: var(--red);
  stroke-width: 2.4;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.mark--ungraded .stroke {
  stroke: var(--ink-3);
  stroke-width: 2;
}

/* 펜이 지나가는 길이만큼 획을 그린다 */
.stroke--circle {
  stroke-dasharray: 100;
  stroke-dashoffset: 100;
  animation: draw 0.55s ease-out forwards;
}

.stroke--x1,
.stroke--x2 {
  stroke-dasharray: 28;
  stroke-dashoffset: 28;
  animation: draw 0.22s ease-out forwards;
}

.stroke--x2 {
  animation-delay: 0.16s;
}

@keyframes draw {
  to {
    stroke-dashoffset: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .stroke {
    stroke-dashoffset: 0 !important;
    animation: none !important;
  }
}
</style>
