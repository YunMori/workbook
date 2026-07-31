import axios from 'axios'

const client = axios.create({ baseURL: '/api' })

export const listExams = () => client.get('/exams/').then((r) => r.data)

export const getExam = (id, { withSolutions = false } = {}) =>
  client
    .get(`/exams/${id}/`, { params: withSolutions ? { with_solutions: 1 } : {} })
    .then((r) => r.data)

export const startAttempt = (exam, token) =>
  client.post('/attempts/', { exam, token }).then((r) => r.data)

export const submitAttempt = (attemptId, answers, elapsedSec) =>
  client
    .post(`/attempts/${attemptId}/submit/`, { answers, elapsed_sec: elapsedSec })
    .then((r) => r.data)

export const getAttempt = (attemptId) => client.get(`/attempts/${attemptId}/`).then((r) => r.data)

export const listAttempts = (token) =>
  client.get('/attempts/', { params: { token } }).then((r) => r.data)

export const gradeAnswer = (answerId, payload) =>
  client.patch(`/attempt-answers/${answerId}/`, payload).then((r) => r.data)

export default client
