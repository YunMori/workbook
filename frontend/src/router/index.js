import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  {
    path: '/exams/:id/study',
    name: 'study',
    component: () => import('../views/StudyView.vue'),
    props: true,
  },
  {
    path: '/exams/:id/take',
    name: 'take',
    component: () => import('../views/TakeView.vue'),
    props: true,
  },
  {
    path: '/attempts/:attemptId/result',
    name: 'result',
    component: () => import('../views/ResultView.vue'),
    props: true,
  },
  { path: '/history', name: 'history', component: () => import('../views/HistoryView.vue') },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: (to) => (to.hash ? { el: to.hash } : { top: 0 }),
})
