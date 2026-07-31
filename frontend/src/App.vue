<script setup>
import { RouterLink, RouterView, useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()
// 응시 중에는 자체 헤더(타이머)가 있으므로 전역 헤더를 감춘다.
const showHeader = computed(() => route.name !== 'take')
</script>

<template>
  <header v-if="showHeader" class="masthead">
    <div class="wrap masthead__inner">
      <RouterLink to="/" class="brand">
        <span class="brand__mark" aria-hidden="true"></span>
        <span class="brand__name">문제집</span>
        <span class="brand__sub">SSAFY Vue.js &amp; JavaScript</span>
      </RouterLink>
      <nav class="nav">
        <RouterLink to="/" class="nav__link">문제 목록</RouterLink>
        <RouterLink to="/history" class="nav__link">응시 기록</RouterLink>
      </nav>
    </div>
  </header>

  <main>
    <RouterView />
  </main>
</template>

<style scoped>
.masthead {
  border-bottom: 1px solid var(--rule);
  background: var(--sheet);
  position: sticky;
  top: 0;
  z-index: 20;
}

.masthead__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  height: 3.5rem;
}

.brand {
  display: flex;
  align-items: baseline;
  gap: 0.55rem;
  text-decoration: none;
  min-width: 0;
}

/* 빨간펜 촉 — 이 앱이 하는 일(채점)의 표식 */
.brand__mark {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--red);
  flex: none;
  align-self: center;
}

.brand__name {
  font-family: var(--mono);
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: -0.03em;
}

.brand__sub {
  font-family: var(--mono);
  font-size: 0.6875rem;
  color: var(--ink-3);
  letter-spacing: 0.02em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.nav {
  display: flex;
  gap: 1.1rem;
  flex: none;
}

.nav__link {
  font-family: var(--mono);
  font-size: 0.8125rem;
  text-decoration: none;
  color: var(--ink-2);
  padding-bottom: 2px;
  border-bottom: 1.5px solid transparent;
}

.nav__link:hover {
  color: var(--ink);
}

.nav__link.router-link-exact-active {
  color: var(--ink);
  border-bottom-color: var(--ink);
}

@media (max-width: 560px) {
  .brand__sub {
    display: none;
  }
}
</style>
