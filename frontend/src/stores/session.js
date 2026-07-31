import { defineStore } from 'pinia'
import { ref } from 'vue'

const TOKEN_KEY = 'workbook:token'
const activeKey = (examId) => `workbook:active:${examId}`

function readJSON(key) {
  try {
    const raw = localStorage.getItem(key)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

/**
 * 로그인 없이 응시 이력을 이어 가기 위한 브라우저 세션.
 * - token: 이 브라우저를 가리키는 UUID. 서버의 응시 기록과 묶인다.
 * - 진행 중인 응시: 새로고침해도 답안이 남도록 localStorage에 임시 저장한다.
 */
export const useSessionStore = defineStore('session', () => {
  const token = ref(localStorage.getItem(TOKEN_KEY) || '')

  if (!token.value) {
    token.value = crypto.randomUUID()
    localStorage.setItem(TOKEN_KEY, token.value)
  }

  function loadDraft(examId) {
    return readJSON(activeKey(examId))
  }

  function saveDraft(examId, draft) {
    localStorage.setItem(activeKey(examId), JSON.stringify(draft))
  }

  function clearDraft(examId) {
    localStorage.removeItem(activeKey(examId))
  }

  return { token, loadDraft, saveDraft, clearDraft }
})
