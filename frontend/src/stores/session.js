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
 * 서버의 token은 UUIDField라서 형식이 맞아야 한다.
 * crypto.randomUUID는 보안 컨텍스트(HTTPS·localhost)에서만 있으므로,
 * http://<IP> 로 접속한 배포 환경에서는 getRandomValues로 v4를 직접 만든다.
 */
function newToken() {
  if (crypto.randomUUID) return crypto.randomUUID()

  const bytes = crypto.getRandomValues(new Uint8Array(16))
  bytes[6] = (bytes[6] & 0x0f) | 0x40 // version 4
  bytes[8] = (bytes[8] & 0x3f) | 0x80 // variant 10
  const hex = [...bytes].map((b) => b.toString(16).padStart(2, '0')).join('')
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`
}

/**
 * 로그인 없이 응시 이력을 이어 가기 위한 브라우저 세션.
 * - token: 이 브라우저를 가리키는 UUID. 서버의 응시 기록과 묶인다.
 * - 진행 중인 응시: 새로고침해도 답안이 남도록 localStorage에 임시 저장한다.
 */
export const useSessionStore = defineStore('session', () => {
  const token = ref(localStorage.getItem(TOKEN_KEY) || '')

  if (!token.value) {
    token.value = newToken()
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
