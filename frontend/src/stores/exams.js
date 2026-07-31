import { defineStore } from 'pinia'
import { ref } from 'vue'

import { getExam, listExams } from '../api/client'

export const useExamStore = defineStore('exams', () => {
  const exams = ref([])
  const loading = ref(false)
  const error = ref('')

  // 문항 캐시. 정답 포함 여부가 다르면 다른 캐시로 취급한다.
  const cache = new Map()
  const key = (id, withSolutions) => `${id}:${withSolutions ? 'sol' : 'plain'}`

  async function loadExams() {
    if (exams.value.length) return exams.value
    loading.value = true
    error.value = ''
    try {
      exams.value = await listExams()
    } catch {
      error.value = '시험 목록을 불러오지 못했습니다. 백엔드 서버가 켜져 있는지 확인하세요.'
    } finally {
      loading.value = false
    }
    return exams.value
  }

  async function loadExam(id, { withSolutions = false } = {}) {
    const cacheKey = key(id, withSolutions)
    if (cache.has(cacheKey)) return cache.get(cacheKey)
    const exam = await getExam(id, { withSolutions })
    cache.set(cacheKey, exam)
    return exam
  }

  return { exams, loading, error, loadExams, loadExam }
})
