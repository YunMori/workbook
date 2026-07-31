<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

import { listAttempts } from '../api/client'
import { formatClock, formatDate, formatPoints } from '../lib/format'
import { useSessionStore } from '../stores/session'

const session = useSessionStore()
const attempts = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    attempts.value = await listAttempts(session.token)
  } catch {
    error.value = '응시 기록을 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
})

const rows = computed(() =>
  attempts.value.map((attempt) => ({
    ...attempt,
    total: Number(attempt.auto_score) + Number(attempt.self_score),
  })),
)

const best = computed(() => Math.max(0, ...rows.value.map((r) => r.total)))
</script>

<template>
  <div class="wrap">
    <header class="page-head">
      <p class="eyebrow">응시 기록</p>
      <h1 class="page-head__title">지금까지 푼 시험</h1>
      <p class="page-head__note">
        이 브라우저에 저장된 기록입니다. 로그인 없이 이 기기에서만 이어집니다.
      </p>
    </header>

    <p v-if="loading" class="empty">불러오는 중…</p>
    <p v-else-if="error" class="empty">{{ error }}</p>
    <p v-else-if="!rows.length" class="empty">
      아직 응시한 기록이 없습니다. <RouterLink to="/">문제 목록</RouterLink>에서 시작하세요.
    </p>

    <table v-else class="log">
      <thead>
        <tr>
          <th>응시일</th>
          <th>시험</th>
          <th class="num">소요</th>
          <th class="num">자동</th>
          <th class="num">자기채점</th>
          <th class="num">총점</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in rows" :key="row.id">
          <td class="mono dim">{{ formatDate(row.submitted_at) }}</td>
          <td>{{ row.exam_title }}</td>
          <td class="num mono dim">{{ formatClock(row.elapsed_sec) }}</td>
          <td class="num mono dim">{{ formatPoints(row.auto_score) }}</td>
          <td class="num mono dim">{{ formatPoints(row.self_score) }}</td>
          <td class="num mono total" :class="{ 'total--best': row.total === best && best > 0 }">
            {{ formatPoints(row.total) }}
          </td>
          <td class="num">
            <RouterLink
              class="btn"
              :to="{ name: 'result', params: { attemptId: row.id } }"
            >
              결과 보기
            </RouterLink>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.page-head {
  padding: 2.5rem 0 1.25rem;
  border-bottom: 2px solid var(--ink);
}

.page-head__title {
  font-size: 1.4rem;
  font-weight: 700;
  letter-spacing: -0.04em;
  margin: 0.2rem 0 0.4rem;
}

.page-head__note {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--ink-3);
}

.log {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 5rem;
  font-size: 0.875rem;
}

.log th {
  padding: 0.7rem 0.6rem;
  border-bottom: 1px solid var(--rule);
  text-align: left;
  font-family: var(--mono);
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--ink-3);
}

.log td {
  padding: 0.75rem 0.6rem;
  border-bottom: 1px solid var(--rule);
  vertical-align: middle;
}

.num {
  text-align: right;
}

.dim {
  color: var(--ink-3);
  font-variant-numeric: tabular-nums;
  font-size: 0.8125rem;
}

.total {
  font-size: 1rem;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.03em;
}

.total--best {
  color: var(--red);
}

@media (max-width: 720px) {
  .log {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
  }
}
</style>
