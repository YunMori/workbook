<script setup>
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'

import { useExamStore } from '../stores/exams'

const store = useExamStore()

onMounted(() => store.loadExams())
</script>

<template>
  <div class="wrap">
    <!-- 표지: 이 문제집이 무엇을 묻는지가 첫 화면의 주장 -->
    <section class="cover">
      <p class="eyebrow">SSAFY 모의고사</p>
      <h1 class="cover__title">
        과목 평가<br />
        WEB(Front_End)
      </h1>
  
    </section>

    <p v-if="store.error" class="error">{{ store.error }}</p>
    <p v-else-if="store.loading" class="empty">불러오는 중…</p>

    <!-- 목차: 문제집 앞머리의 차례 그대로 -->
    <ol v-else class="toc">
      <li v-for="exam in store.exams" :key="exam.id" class="toc__row">
        <div class="toc__body">
          <h2 class="toc__title">{{ exam.title }}</h2>
          <p class="toc__meta mono">
            객관식 {{ exam.mc_count }} · 주관식 {{ exam.short_count }} · 서술형
            {{ exam.essay_count }}
            <span class="toc__dot">·</span> {{ exam.total_score }}점
            <span class="toc__dot">·</span> {{ exam.time_limit_min }}분
          </p>
        </div>

        <div class="toc__actions">
          <RouterLink class="btn" :to="{ name: 'study', params: { id: exam.id } }">
            문제 보기
          </RouterLink>
          <RouterLink class="btn btn--solid" :to="{ name: 'take', params: { id: exam.id } }">
            응시하기
          </RouterLink>
        </div>
      </li>
    </ol>
  </div>
</template>

<style scoped>
.cover {
  padding: 4.5rem 0 3rem;
  border-bottom: 2px solid var(--ink);
  margin-bottom: 0;
}

.cover__title {
  font-size: clamp(2.75rem, 9vw, 5rem);
  line-height: 0.95;
  font-weight: 700;
  letter-spacing: -0.055em;
  margin: 0.6rem 0 1.4rem;
}

.cover__scope {
  font-size: 0.75rem;
  line-height: 1.9;
  color: var(--ink-3);
  margin: 0;
}

.toc {
  list-style: none;
  margin: 0 0 5rem;
  padding: 0;
}

.toc__row {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.35rem 0.25rem;
  border-bottom: 1px solid var(--rule);
  transition: background 0.15s;
}

.toc__row:hover {
  background: var(--sheet);
}

.toc__body {
  flex: 1;
  min-width: 0;
}

.toc__title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.15rem;
}

.toc__meta {
  font-size: 0.75rem;
  color: var(--ink-3);
  margin: 0;
}

.toc__dot {
  padding: 0 0.15rem;
}

.toc__actions {
  display: flex;
  gap: 0.5rem;
  flex: none;
}

.error {
  margin: 2rem 0;
  padding: 0.9rem 1.1rem;
  border: 1px solid var(--red);
  border-radius: var(--radius);
  background: var(--red-soft);
  color: var(--red);
  font-size: 0.875rem;
}

@media (max-width: 640px) {
  .toc__row {
    flex-wrap: wrap;
    gap: 0.75rem 1rem;
  }

  .toc__actions {
    width: 100%;
  }

  .toc__actions .btn {
    flex: 1;
  }
}
</style>
