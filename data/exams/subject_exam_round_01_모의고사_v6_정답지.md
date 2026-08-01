# Vue 상태관리(Pinia) & 라우터(Vue Router) 모의고사 — Round 01 v6 정답지

## 빠른 정답표 (객관식)

| 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10  | 11  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ② | ④ | ③ | ② | ③ | ② | ③ | ② | ② | ② | ① |

| 12  | 13  | 14  | 15  | 16  | 17  | 18  | 19  | 20  | 21  | 22  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ① | ② | ② | ② | ③ | ② | ② | ① | ③ | ② | ② |

| 23  | 24  | 25  | 26  | 27  | 28  | 29  | 30  | 31  | 32  | 33  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ② | ④ | ② | ② | ④ | ③ | ① | ② | ② | ② | ② |

| 34  | 35  | 36  | 37  | 38  | 39  | 40  | 41  | 42  | 43  | 44  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ③ | ② | ② | ② | ③ | ② | ② | ② | ② | ② | ② |

| 45  | 46  | 47  | 48  | 49  | 50  | 51  | 52  | 53  | 54  | 55  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ② | ② | ② | ② | ② | ④ | ② | ② | ② | ② | ① |

| 56  | 57  | 58  | 59  | 60  |
| --- | --- | --- | --- | --- |
| ② | ③ | ② | ② | ① |

**정답 분포:** ① 6개 (11, 12, 19, 29, 55, 60) · ② 41개 (1, 4, 6, 8, 9, 10, 13, 14, 15, 17, 18, 21, 22, 23, 25, 26, 30, 31, 32, 33, 35, 36, 37, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 51, 52, 53, 54, 56, 58, 59) · ③ 9개 (3, 5, 7, 16, 20, 28, 34, 38, 57) · ④ 4개 (2, 24, 27, 50)

---

## 객관식 해설

**1. 정답 ②** — State-View-Actions가 한 방향으로 순환하는 구조를 단방향 데이터 흐름이라 한다. (6_vue_statemanagement_router)

**2. 정답 ④** — 컴포넌트 구조 3요소는 State, View, Actions이다. Getters는 Pinia의 구성 요소이지 컴포넌트 구조 3요소가 아니다. (6_vue_statemanagement_router)

**3. 정답 ③** — 단순성이 무너지는 경우는 "여러 뷰가 동일 상태 공유" / "여러 기능이 동일 상태 변경" 두 가지이며, 컴포넌트 개수는 기준이 아니다. (6_vue_statemanagement_router)

**4. 정답 ②** — 슬라이드는 "끌어올리기(lifting up)" 후 props 전달을 제시하되, 계층이 깊어지면 비효율적이라는 한계를 함께 언급한다. (6_vue_statemanagement_router)

**5. 정답 ③** — 슬라이드에서 "Vue의 공식 상태 관리 라이브러리 === Pinia"로 강조되어 있다. (6_vue_statemanagement_router)

**6. 정답 ②** — create-vue CLI 화면에는 "Pinia (state management)" 옵션이 있으며, 이를 선택하면 stores 폴더가 생성된다. (6_vue_statemanagement_router)

**7. 정답 ③** — Pinia 추가 시 src 하위에 stores 폴더(예: stores/counter.js)가 신규 생성된다. router/views는 Vue Router 추가 시 생성되는 폴더다. (6_vue_statemanagement_router)

**8. 정답 ②** — Pinia 구성 요소는 store, state, getters, actions, plugin이다. mutations는 Vuex의 개념으로 Pinia에는 없다. (6_vue_statemanagement_router)

**9. 정답 ②** — `defineStore('counter', ...)`에서 'counter'는 앱 전체에서 store를 식별하는 고유 ID다. (6_vue_statemanagement_router)

**10. 정답 ②** — `useCounterStore`처럼 `use` + 대상 이름 + `Store` 형태로 작성하는 것을 권장한다. (6_vue_statemanagement_router)

**11. 정답 ①** — Setup Store 문법에서는 `ref() === state`, `computed() === getters`, `function() === actions`로 매핑된다. (6_vue_statemanagement_router)

**12. 정답 ①** — Setup Store에서는 반환하지 않은 값은 store 외부에서 접근할 수 없다 — 즉 store는 공유하지 않는 private 상태 속성을 가지지 않는다. (6_vue_statemanagement_router)

**13. 정답 ②** — Pinia는 store의 모든 getters도 state처럼 `store.doubleCount` 형태로 직접 접근 가능하다. (6_vue_statemanagement_router)

**14. 정답 ②** — getters는 계산값 조회 성격이고, actions는 상태 조작·비동기·API 호출 등 부수효과가 가능한 메서드다. (6_vue_statemanagement_router)

**15. 정답 ②** — devtools의 Pinia 섹션에서 state는 Reactive 객체로, getters는 Object로 표시된다. (6_vue_statemanagement_router)

**16. 정답 ③** — Local Storage는 쿠키와 달리 네트워크 요청 시 서버로 전송되지 않는다는 점이 특징이다. (6_vue_statemanagement_router)

**17. 정답 ②** — pinia-plugin-persistedstate는 Pinia의 플러그인으로 상태를 local storage/session storage에 영구 저장 및 복원한다. (6_vue_statemanagement_router)

**18. 정답 ②** — 기존 `app.use(createPinia())` 대신 pinia 인스턴스를 변수로 만들어 plugin을 등록한 뒤 `app.use(pinia)`로 적용한다. (6_vue_statemanagement_router)

**19. 정답 ①** — `defineStore('counter', () => {...}, { persist: true })` 형태로 세 번째 인자에 persist 옵션을 넣는다. (6_vue_statemanagement_router)

**20. 정답 ③** — Pinia를 쓴다고 모든 데이터를 state에 넣을 필요는 없으며, props/emit과 함께 적절히 병행해야 한다. 애플리케이션이 단순하면 Pinia가 없는 편이 더 효율적일 수 있다. (6_vue_statemanagement_router)

**21. 정답 ②** — Routing은 네트워크에서 경로를 선택하는 프로세스이며, 웹 애플리케이션에서는 페이지 간 전환/경로 관리 기술을 의미한다. (6_vue_statemanagement_router)

**22. 정답 ②** — SSR에서는 서버가 라우팅을 수행하며, 클릭할 때마다 서버로부터 새 HTML 전체를 받아 페이지를 다시 로드한다. (6_vue_statemanagement_router)

**23. 정답 ②** — CSR은 클라이언트 측 JavaScript가 라우팅을 수행하며 Ajax로 데이터만 가져와 전체 리로드 없이 화면을 갱신한다. (6_vue_statemanagement_router)

**24. 정답 ④** — 라우팅이 없을 때의 문제는 URL 변화 감지 불가, 새로고침 시 첫 페이지로 복귀, 링크 공유 시 첫 페이지만 공유, 뒤로 가기 불가 등이며 서버 응답 속도 문제는 언급되지 않는다. (6_vue_statemanagement_router)

**25. 정답 ②** — Vue Router는 "Vue 공식 라우터(The official Router for Vue.js)"로 소개된다. (6_vue_statemanagement_router)

**26. 정답 ②** — "Router (SPA development)" 옵션을 선택하면 Router가 프로젝트에 추가된다. (6_vue_statemanagement_router)

**27. 정답 ④** — stores 폴더는 Pinia 추가 시 생성되는 것이고, Router 추가 시에는 App.vue 변화, router 폴더, views 폴더가 생긴다. (6_vue_statemanagement_router)

**28. 정답 ③** — RouterLink는 `<a>` 태그를 렌더링하며 `<button>` 태그가 아니다. (6_vue_statemanagement_router)

**29. 정답 ①** — RouterView는 현재 URL에 대응하는 컴포넌트를 표시하는 영역이다. (6_vue_statemanagement_router)

**30. 정답 ②** — router/index.js는 라우팅 설정이 작성되는 곳으로 URL과 컴포넌트를 매핑한다. (6_vue_statemanagement_router)

**31. 정답 ②** — views 폴더는 components와 기능적으로 다르지 않고, RouterView에 렌더링할 컴포넌트를 단순 분류상 모아두는 폴더다. (6_vue_statemanagement_router)

**32. 정답 ②** — 일반 컴포넌트와 구분하기 위해 이름을 View로 끝내는 것을 권장하지만 필수 사항은 아니다 (예: HomeView.vue). (6_vue_statemanagement_router)

**33. 정답 ②** — ① index.js에 path/name/component 설정 → ② RouterLink의 to 속성에 해당 path 사용 → ③ 클릭 시 경로에 맞는 컴포넌트가 RouterView에 렌더링된다. (6_vue_statemanagement_router)

**34. 정답 ③** — `createRouter({ routes: [...] })` 형태로 routes 배열 안에 각 라우트 객체(path, name, component)를 정의한다. (6_vue_statemanagement_router)

**35. 정답 ②** — Named Routes를 사용하려면 `v-bind`(`:to`)로 `{ name: 'home' }` 형태의 객체를 전달해야 하며, 단순 문자열 경로가 아니다. (6_vue_statemanagement_router)

**36. 정답 ②** — Named Routes는 v-bind를 사용해 `:to="{ name: 'home' }"` 형태의 객체를 전달한다. ①은 path 방식(문자열)이다. (6_vue_statemanagement_router)

**37. 정답 ②** — `path: '/user/:id'`처럼 콜론(:)으로 동적 세그먼트(매개변수)를 표기한다. (6_vue_statemanagement_router)

**38. 정답 ③** — `:to="{ name: 'user', params: { id: userId } }"`처럼 params 속성의 객체로 전달하며, key 이름은 index.js의 매개변수 이름(`:id`)과 같아야 한다. (6_vue_statemanagement_router)

**39. 정답 ②** — 라우트의 매개변수는 컴포넌트에서 `$route.params`로 참조할 수 있으며, 템플릿에서는 `{{ $route.params.id }}`처럼 사용한다. (6_vue_statemanagement_router)

**40. 정답 ②** — `useRoute()`로 route 객체를 가져와 `ref(route.params.id)` 형태로 반응형 변수에 담는 것이 권장된다. (6_vue_statemanagement_router)

**41. 정답 ②** — Programmatic Navigation은 RouterLink 대신 router 인스턴스 메서드를 JavaScript로 호출해 이동하는 방식이다. (6_vue_statemanagement_router)

**42. 정답 ②** — `<RouterLink :to="...">`(선언적 표현)를 클릭하면 내부적으로 `router.push(...)`(프로그래밍적 표현)가 호출된다. (6_vue_statemanagement_router)

**43. 정답 ②** — `useRouter()`는 router 인스턴스(push, replace 등 메서드 호출용)를 반환하고, `useRoute()`는 현재 route 객체를 반환한다 — 서로 다른 함수이므로 혼동에 주의해야 한다. (6_vue_statemanagement_router)

**44. 정답 ②** — named route + params 형태로 라우터가 URL을 빌드하도록 전달한다. (6_vue_statemanagement_router)

**45. 정답 ②** — Nested Routes는 URL에서의 중첩 관계를 표현하는 개념으로, 컴포넌트 간 부모-자식 관계 관점이 아니라는 점이 슬라이드에서 강조된다. (6_vue_statemanagement_router)

**46. 정답 ②** — 라우트 객체에 `children` 배열 옵션을 두어 필요한 만큼 중첩 관계를 표현한다. (6_vue_statemanagement_router)

**47. 정답 ②** — `{ path: '', name: 'user', component: UserHome }`처럼 빈 path는 상위 경로(`/user/:id`) 방문 시 기본으로 렌더링되는 자식 라우트다. (6_vue_statemanagement_router)

**48. 정답 ②** — 슬라이드는 중첩된 Named Routes를 다룰 때 일반적으로 하위(자식) 경로에만 name을 지정한다고 강조한다. (6_vue_statemanagement_router)

**49. 정답 ②** — Navigation Guard는 라우트 전환 전/후 자동 실행되는 Hook으로, 특정 URL 접근을 redirect하거나 취소해 내비게이션을 보호한다. (6_vue_statemanagement_router)

**50. 정답 ④** — Navigation Guard는 Globally, Per-route, In-component 세 종류이며 In-store는 존재하지 않는다. (6_vue_statemanagement_router)

**51. 정답 ②** — 처음부터 모든 컴포넌트를 준비하면 로드 시간이 길어질 수 있어, 해당 경로를 처음 방문할 때 컴포넌트를 로드하는 것이 Lazy Loading Routes다. (6_vue_statemanagement_router)

**52. 정답 ②** — 화살표 함수로 감싼 동적 import(`() => import(...)`)를 사용하면 route level code-splitting이 적용되어 별도 chunk 파일로 분리, 지연 로드된다. (6_vue_statemanagement_router)

**53. 정답 ②** — Pinia는 시작 비용과 구조적 이해가 필요하므로, 단순한 앱에서는 없는 편이 효율적일 수 있고 중대형 규모에서 자연스럽게 필요해진다. (6_vue_statemanagement_router)

**54. 정답 ②** — query 옵션은 URL에 `?key=value` 형태의 쿼리 스트링으로 붙는다. (6_vue_statemanagement_router)

**55. 정답 ①** — `useCounterStore()`로 store 인스턴스를 얻은 뒤 `store.count`처럼 state에 직접 접근한다. (6_vue_statemanagement_router)

**56. 정답 ②** — store에 정의되지 않은 state는 컴포넌트에서 새로 추가할 수 없다. (6_vue_statemanagement_router)

**57. 정답 ③** — 개발자도구의 Application → Local Storage에서 store 이름을 key로 한 JSON 문자열 값을 확인할 수 있다. (6_vue_statemanagement_router)

**58. 정답 ②** — Elements/Console 등 옆의 "Vue" 탭을 선택하고 그 안의 "Pinia" 섹션을 클릭하면 store 상태를 확인할 수 있다. (6_vue_statemanagement_router)

**59. 정답 ②** — 문자열을 그대로 전달하는 것은 literal string path 방식이며, 객체로 path/name/params/query를 전달하는 방식과 구분된다. (6_vue_statemanagement_router)

**60. 정답 ①** — push는 새 항목을 history stack에 추가하는 방식이라 뒤로 가기 시 이전 URL로 돌아갈 수 있다. (④는 replace의 특징) (6_vue_statemanagement_router)

---

## 주관식 해설

- **61.** 정답: Pinia — 슬라이드에서 강조된 핵심 사실이다.
- **62.** 정답: store, state, getters, actions, plugin — Pinia는 store라는 저장소를 가지며, store는 state/getters/actions로 구성되고 plugin으로 확장 가능하다.
- **63.** 정답: state — `ref() === state`, `computed() === getters`, `function() === actions`.
- **64.** 정답: return { ... } (반환문) — 반환하지 않은 값은 store 외부에서 접근할 수 없다.
- **65.** 정답: store의 고유 ID(store id) — 애플리케이션 전체에서 store를 식별하는 고유 ID다.
- **66.** 정답: `{ persist: true }` — `defineStore('counter', () => {...}, { persist: true })` 형태로 작성한다.
- **67.** 정답: 쿠키(Cookie) — Local Storage는 쿠키와 달리 네트워크 요청에 자동으로 실리지 않는다는 점이 비교 포인트다.
- **68.** 정답: JSON — CSR은 최초 요청 시 HTML을 받고, 이후 Ajax 요청으로 JSON 데이터만 받아 동적으로 갱신한다.
- **69.** 정답: Router (SPA development) — create-vue CLI 화면의 옵션명이다.
- **70.** 정답: `<a>` 태그 — RouterLink는 페이지 리로드 없이 URL을 변경하는 `<a>` 태그를 렌더링한다.
- **71.** 정답: src/router/index.js — router/index.js에서 createRouter()로 routes 배열을 정의한다.
- **72.** 정답: routes — `createRouter({ routes: [...] })` 형태로 사용한다.
- **73.** 정답: v-bind (콜론 `:`) — `:to="{ name: 'home' }"`처럼 객체를 바인딩해야 하므로 v-bind(:)가 필요하다.
- **74.** 정답: 콜론 `:` (예: `/user/:id`) — 콜론으로 동적 세그먼트를 표기한다.
- **75.** 정답: $route — `$route.params.id` 형태로 참조한다.
- **76.** 정답: Programmatic Navigation (프로그래밍 방식 내비게이션) — router 인스턴스의 메서드(push, replace)를 코드로 호출해 이동하는 방식이다.
- **77.** 정답: router.replace() — push는 history stack에 새 항목을 추가하지만, replace는 현재 위치를 바꾼다.
- **78.** 정답: children — 라우트 객체에 children 배열로 중첩 관계를 표현한다.
- **79.** 정답: Globally (전역 가드) — Navigation Guard는 Globally, Per-route, In-component 세 종류가 있다.
- **80.** 정답: Lazy Loading Routes (지연 로딩) — `component: () => import(...)` 형태로 route level code-splitting을 적용한다.

---

## 서술형 채점 기준

### 81. 상태 관리의 단순성이 무너지는 두 가지 경우를 각각 설명하시오.

| 배점 | 채점 요소 |
| --- | --- |
| 2점 | 핵심 개념 정의를 정확히 서술 |
| 1점 | 관련 예시·세부 근거를 함께 제시 |
| 1점 | 개념 간 비교/구분점을 명확히 설명 |

**모범 답안:**

첫째, 여러 뷰(컴포넌트)가 동일한 상태에 종속되는 경우다. 이때는 공유 상태를 공통 조상 컴포넌트로 끌어올려(lifting up) props로 하위에 전달해야 하는데, 컴포넌트 계층 구조가 깊어질수록 props 전달이 비효율적이고 관리가 어려워진다. 둘째, 서로 다른 뷰의 기능이 동일한 상태를 변경시켜야 하는 경우다. 이때는 이벤트를 발신(emit)하여 상태의 여러 복사본을 동기화해야 하는데, 이 패턴 역시 깨지기 쉽고 유지 관리가 불가능한 코드로 이어지기 쉽다. 두 경우 모두 컴포넌트 트리가 커질수록 문제가 심화되며, 이를 해결하기 위해 Pinia 같은 중앙 저장소가 필요해진다.

---

### 82. Pinia의 Setup Store 문법에서 state, getters, actions가 Composition API의 어떤 함수와 대응되는지 설명하고, 간단한 예시 코드를 작성하시오.

| 배점 | 채점 요소 |
| --- | --- |
| 2점 | 핵심 개념 정의를 정확히 서술 |
| 1점 | 관련 예시·세부 근거를 함께 제시 |
| 1점 | 개념 간 비교/구분점을 명확히 설명 |

**모범 답안:**

Pinia의 Setup Store는 `ref()`를 state, `computed()`를 getters, `function()`을 actions로 사용한다. 예를 들어 다음과 같이 작성한다.

```js
import { ref, computed } from "vue";
import { defineStore } from "pinia";

export const useCounterStore = defineStore("counter", () => {
  const count = ref(0); // state
  const doubleCount = computed(() => count.value * 2); // getters
  const increment = function () {
    count.value++;
  }; // actions

  return { count, doubleCount, increment };
});
```

반드시 사용할 값을 `return`으로 반환해야 store 외부(컴포넌트)에서 접근할 수 있으며, 반환하지 않은 값은 private하게 유지된다.

---

### 83. `pinia-plugin-persistedstate`를 프로젝트에 적용하는 전체 과정을 순서대로 설명하시오.

| 배점 | 채점 요소 |
| --- | --- |
| 2점 | 핵심 개념 정의를 정확히 서술 |
| 1점 | 관련 예시·세부 근거를 함께 제시 |
| 1점 | 개념 간 비교/구분점을 명확히 설명 |

**모범 답안:**

먼저 `npm i pinia-plugin-persistedstate`로 패키지를 설치한다. 이후 main.js에서 `createPinia()`로 만든 pinia 인스턴스에 `pinia.use(piniaPluginPersistedstate)`로 플러그인을 등록하고, 기존의 `app.use(createPinia())` 대신 `app.use(pinia)`를 호출한다. 그 다음 영구 저장을 적용할 store의 `defineStore()` 세 번째 인자로 `{ persist: true }`를 전달한다. 적용 후에는 개발자도구의 Application → Local Storage에서 store 이름을 key로 하는 JSON 문자열 값이 저장된 것을 확인할 수 있다.

---

### 84. SSR에서의 라우팅과 CSR에서의 라우팅의 차이를 비교하여 설명하시오.

| 배점 | 채점 요소 |
| --- | --- |
| 2점 | 핵심 개념 정의를 정확히 서술 |
| 1점 | 관련 예시·세부 근거를 함께 제시 |
| 1점 | 개념 간 비교/구분점을 명확히 설명 |

**모범 답안:**

SSR에서는 라우팅이 서버 측에서 수행된다. 사용자가 링크를 클릭하면 브라우저는 서버로 요청을 보내고, 서버는 방문한 URL 경로를 기반으로 새로운 HTML 응답을 전송하며, 브라우저는 이 새 HTML로 전체 페이지를 다시 로드한다. 반면 CSR에서는 라우팅이 클라이언트 측에서 수행된다. 최초 요청 시에만 HTML을 받고, 이후에는 클라이언트의 JavaScript가 Ajax 요청으로 필요한 데이터(JSON)만 동적으로 가져와 화면 일부를 갱신하므로 전체 페이지를 다시 로드하지 않는다.

---

### 85. SPA(Single Page Application)에 라우팅 기능이 없다면 어떤 문제가 발생하는지 설명하시오.

| 배점 | 채점 요소 |
| --- | --- |
| 2점 | 핵심 개념 정의를 정확히 서술 |
| 1점 | 관련 예시·세부 근거를 함께 제시 |
| 1점 | 개념 간 비교/구분점을 명확히 설명 |

**모범 답안:**

SPA는 물리적으로 하나의 HTML 페이지만 사용하므로, 라우팅이 없다면 사용자가 URL을 통한 페이지 변화를 감지할 수 없고 현재 어떤 화면이 렌더링 중인지 상태를 알 수 없다. 그 결과 새로고침하면 항상 처음 페이지로 되돌아가고, 링크를 공유해도 항상 첫 페이지만 공유되며, 브라우저의 뒤로 가기 기능도 사용할 수 없다. 따라서 라우팅을 통해 하나의 페이지 안에서도 주소에 따라 여러 컴포넌트를 새로 렌더링하여 마치 여러 페이지를 사용하는 것처럼 보이도록 구현해야 한다.

---

### 86. RouterLink와 RouterView의 역할 차이를 설명하시오.

| 배점 | 채점 요소 |
| --- | --- |
| 2점 | 핵심 개념 정의를 정확히 서술 |
| 1점 | 관련 예시·세부 근거를 함께 제시 |
| 1점 | 개념 간 비교/구분점을 명확히 설명 |

**모범 답안:**

RouterLink는 페이지를 다시 로드하지 않고 URL을 변경하는 네비게이션 링크로, 최종적으로 HTML의 `<a>` 태그를 렌더링하며 `to` 속성으로 이동할 경로를 지정한다. 반면 RouterView는 현재 URL(RouterLink로 이동한 경로)에 대응하는 컴포넌트를 실제로 화면에 표시하는 영역이다. 즉 RouterLink는 "어디로 이동할지"를 담당하고, RouterView는 "이동한 결과 어떤 컴포넌트를 보여줄지"를 담당한다.

---

### 87. Dynamic Route Matching(동적 경로 매칭)이 필요한 이유와 사용 방법을 예시와 함께 설명하시오.

| 배점 | 채점 요소 |
| --- | --- |
| 2점 | 핵심 개념 정의를 정확히 서술 |
| 1점 | 관련 예시·세부 근거를 함께 제시 |
| 1점 | 개념 간 비교/구분점을 명확히 설명 |

**모범 답안:**

user/1, user/2, user/3처럼 특정 패턴을 공유하는 URL을 각각의 라우트로 일일이 정의하면 반복 작업이 많아진다. 이를 해결하기 위해 URL의 일부를 변수(매개변수)로 사용해 동일한 컴포넌트에 매핑하는 것이 동적 경로 매칭이다. index.js에서 `path: '/user/:id'`처럼 콜론으로 매개변수를 지정하고, RouterLink에서는 `:to="{ name: 'user', params: { id: userId } }"`로 값을 전달한다. 컴포넌트에서는 `$route.params.id` 혹은 `useRoute()`로 얻은 route 객체의 `params.id`를 통해 전달된 값을 사용할 수 있다.

---

### 88. Named Routes 방식과 Dynamic Route Matching에서 매개변수를 전달하는 방식을 함께 사용하는 코드를 작성하고, params의 key가 지켜야 할 규칙을 설명하시오.

| 배점 | 채점 요소 |
| --- | --- |
| 2점 | 핵심 개념 정의를 정확히 서술 |
| 1점 | 관련 예시·세부 근거를 함께 제시 |
| 1점 | 개념 간 비교/구분점을 명확히 설명 |

**모범 답안:**

```js
// index.js
{ path: '/user/:id', name: 'user', component: UserView }
```

```html
<RouterLink :to="{ name: 'user', params: { id: userId } }">User</RouterLink>
```

이때 params 객체의 key(`id`)는 index.js의 path에서 지정한 매개변수 이름(`:id`)과 반드시 동일해야 한다. 이름이 다르면 컴포넌트에서 `$route.params`로 값을 제대로 참조할 수 없다.

---

### 89. Nested Routes(중첩된 라우팅)의 개념을 설명하고, 이를 컴포넌트의 부모-자식 관계와 혼동하면 안 되는 이유를 설명하시오.

| 배점 | 채점 요소 |
| --- | --- |
| 2점 | 핵심 개념 정의를 정확히 서술 |
| 1점 | 관련 예시·세부 근거를 함께 제시 |
| 1점 | 개념 간 비교/구분점을 명확히 설명 |

**모범 답안:**

Nested Routes는 `/user/:id/profile`, `/user/:id/posts`처럼 URL 자체가 계층적으로 중첩된 관계를 컴포넌트 구조로 표현하는 것이다. 상위 라우트(`/user/:id`)에 `children` 배열을 두어 하위 라우트(profile, posts)를 정의하며, `path: ''`인 자식 라우트는 상위 경로 방문 시 기본으로 표시되는 컴포넌트가 된다. 슬라이드는 이를 컴포넌트 간 부모-자식 관계로 바라보지 말고, "URL에서의 중첩된 관계"를 표현하는 관점으로 이해해야 한다고 강조한다. 즉 컴포넌트를 어떻게 조합하느냐가 아니라, URL 경로 구조를 어떻게 라우트로 반영하느냐가 핵심이다.

---

### 90. Navigation Guard의 정의와 세 가지 종류를 설명하시오.

| 배점 | 채점 요소 |
| --- | --- |
| 2점 | 핵심 개념 정의를 정확히 서술 |
| 1점 | 관련 예시·세부 근거를 함께 제시 |
| 1점 | 개념 간 비교/구분점을 명확히 설명 |

**모범 답안:**

Navigation Guard는 Vue Router를 통해 특정 URL에 접근할 때 다른 URL로 redirect하거나 내비게이션 자체를 취소하여 라우트 전환을 보호하는 기능으로, 라우트 전환 전/후에 자동으로 실행되는 Hook이다. 종류는 세 가지로, 애플리케이션 전역의 모든 라우트 전환에 적용되는 Globally(전역 가드), 특정 라우트에만 적용되는 Per-route(라우터 가드), 컴포넌트 내부에서만 적용되는 In-component(컴포넌트 가드)가 있다.

---
