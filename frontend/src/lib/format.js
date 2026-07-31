export const CIRCLED = ['①', '②', '③', '④', '⑤']

export const TYPE_LABEL = { MC: '객관식', SHORT: '주관식', ESSAY: '서술형' }
export const DIFFICULTY_LABEL = { BASIC: '기초', APPLIED: '응용', ADVANCED: '심화' }

/** 초 → "42:07" (한 시간을 넘기면 "1:02:07") */
export function formatClock(totalSeconds) {
  const seconds = Math.max(0, Math.floor(totalSeconds))
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = seconds % 60
  const pad = (n) => String(n).padStart(2, '0')
  return h > 0 ? `${h}:${pad(m)}:${pad(s)}` : `${pad(m)}:${pad(s)}`
}

export function formatDate(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}.${pad(d.getMonth() + 1)}.${pad(d.getDate())} ${pad(d.getHours())}:${pad(
    d.getMinutes(),
  )}`
}

/** 소수점이 없으면 정수로 — 3.0점이 아니라 3점 */
export function formatPoints(value) {
  const n = Number(value)
  return Number.isInteger(n) ? String(n) : n.toFixed(1)
}
