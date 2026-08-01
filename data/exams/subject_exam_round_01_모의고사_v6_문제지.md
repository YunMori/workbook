# Vue 상태관리(Pinia) & 라우터(Vue Router) 모의고사 — Round 01 v6

> 출제 범위: Vue 상태관리(Pinia), Vue Router
> 구성: 객관식 60 · 주관식 20 · 서술형 10 (총 90문항)

## 객관식

### 1. Vue 컴포넌트의 상태 관리 흐름을 나타낼 때 사용하는 용어로, "상태(State) → 뷰(View) → 기능(Actions) → 상태(State)"로 순환하는 흐름을 무엇이라 부르는가?

① 양방향 데이터 바인딩 ② 단방향 데이터 흐름 (one-way data flow) ③ 이벤트 버블링 ④ 반응형 프록시

---

### 2. 컴포넌트 구조의 3요소와 그 정의를 짝지은 것으로 옳지 않은 것은?

① State — 앱 구동에 필요한 기본 데이터 ② View — 상태를 선언적으로 매핑하여 시각화 ③ Actions — 사용자 입력에 반응하여 상태를 변경하는 동작 ④ Getters — 뷰에서 계산된 값을 캐싱하는 요소

---

### 3. 상태 관리의 단순성이 무너지는 경우로 슬라이드에서 제시한 두 가지에 해당하지 않는 것은?

① 여러 뷰가 동일한 상태에 종속되는 경우 ② 서로 다른 뷰의 기능이 동일한 상태를 변경시켜야 하는 경우 ③ 컴포넌트 개수가 10개를 초과하는 경우 ④ 위 ①, ② 모두 해당

---

### 4. 여러 뷰가 동일한 상태에 종속될 때 슬라이드에서 제시한 해결 방식은?

① 상태를 각 컴포넌트에 복제하여 독립적으로 관리한다 ② 공유 상태를 공통 조상 컴포넌트로 끌어올린(lifting up) 뒤 props로 전달한다 ③ localStorage에 즉시 저장한다 ④ 전역 변수(window 객체)에 상태를 둔다

---

### 5. Vue의 공식 상태 관리 라이브러리는 무엇인가?

① Vuex ② Redux ③ Pinia ④ MobX

---

### 6. Vite로 프로젝트를 생성할 때 Pinia를 추가하기 위해 선택해야 하는 CLI 옵션명은?

① Router (SPA development) ② Pinia (state management) ③ TypeScript ④ Vitest (unit testing)

---

### 7. Pinia 추가 시 프로젝트에 새로 생성되는 폴더는?

① router ② views ③ stores ④ plugins

---

### 8. Pinia의 구성 요소 5가지에 해당하지 않는 것은?

① store ② mutations ③ getters ④ plugin

---

### 9. Pinia의 `defineStore()` 함수의 첫 번째 인자가 의미하는 것은?

① 컴포넌트 이름 ② 애플리케이션 전체에서 사용하는 store의 고유 ID ③ state의 초깃값 ④ plugin 목록

---

### 10. `defineStore()`의 반환값을 저장하는 변수명 작명 컨벤션으로 슬라이드가 권장하는 형태는?

① `store` + 이름 ② `use` + `Store` ③ 이름 + `Store`만 사용 (use 접두어 없이) ④ 반드시 `store.js`라는 파일명과 동일해야 함

---

### 11. Pinia의 state, getters, actions는 Composition API의 어떤 요소와 각각 대응되는가?

① state=ref(), getters=computed(), actions=function() ② state=computed(), getters=ref(), actions=function() ③ state=reactive(), getters=watch(), actions=function() ④ state=function(), getters=ref(), actions=computed()

---

### 12. Pinia의 Setup Store에서 반드시 지켜야 할 규칙으로 옳은 것은?

① 사용할 상태와 함수를 `return { ... }`으로 반환해야 한다 ② state는 자동으로 외부에 노출되므로 반환할 필요가 없다 ③ actions만 반환하면 state는 자동 포함된다 ④ export default로만 내보내야 한다

---

### 13. Pinia의 store에서 getters를 컴포넌트에서 사용하는 방법으로 옳은 것은?

① `store.getters.doubleCount`처럼 getters 네임스페이스를 거쳐야 한다 ② `store.doubleCount`처럼 state와 동일하게 직접 접근한다 ③ `mapGetters`를 반드시 사용해야 한다 ④ getters는 템플릿에서 직접 사용할 수 없다

---

### 14. Pinia의 getters와 actions의 차이를 가장 바르게 설명한 것은?

① getters는 비동기 처리가 가능하고 actions는 불가능하다 ② actions는 state 조작, 비동기, API 호출 등 부수효과를 수행할 수 있지만 getters는 계산된 값 조회에 그친다 ③ getters와 actions는 완전히 동일한 기능을 한다 ④ getters만 컴포넌트에서 호출 가능하다

---

### 15. Vue devtools에서 Pinia 구성 요소를 확인할 때, state가 표시되는 방식은?

① Object로 표시된다 ② Reactive 객체(예: `count: 1 (Ref)`)로 표시된다 ③ 표시되지 않는다 ④ JSON 문자열로만 표시된다

---

### 16. Local Storage에 대한 설명으로 옳지 않은 것은?

① 브라우저 내에 key-value 쌍을 저장하는 웹 스토리지 객체다 ② 페이지 새로고침이나 브라우저 재실행 후에도 데이터가 유지된다 ③ 쿠키와 마찬가지로 네트워크 요청 시 서버로 자동 전송된다 ④ 여러 탭이나 창 간에 데이터를 공유할 수 있다

---

### 17. `pinia-plugin-persistedstate`의 역할로 가장 알맞은 것은?

① Pinia store를 서버와 동기화한다 ② 웹 애플리케이션의 상태를 local/session storage에 영구적으로 저장하고 복원한다 ③ Vue Router와 Pinia를 연결한다 ④ state를 자동으로 압축한다

---

### 18. `pinia-plugin-persistedstate`를 main.js에 등록하는 방식으로 옳은 것은?

① `app.use(createPinia())`만 호출하면 자동 등록된다 ② `const pinia = createPinia(); pinia.use(piniaPluginPersistedstate); app.use(pinia)` ③ `import`만 하면 별도 등록 코드 없이 적용된다 ④ main.js가 아닌 App.vue에서 등록해야 한다

---

### 19. 특정 store에만 persist 기능을 적용하려면 `defineStore()`의 세 번째 인자로 무엇을 전달해야 하는가?

① `{ persist: true }` ② `{ storage: 'local' }` ③ `{ plugin: 'persistedstate' }` ④ `{ save: true }`

---

### 20. Pinia 사용에 대한 슬라이드의 조언으로 옳은 것은?

① 모든 데이터를 반드시 store에서 관리해야 한다 ② props와 emit은 더 이상 사용하지 않아도 된다 ③ 상황에 따라 pass props, emit event와 함께 적절히 사용해야 한다 ④ 소규모 애플리케이션일수록 Pinia를 우선 도입해야 한다

---

### 21. Routing(라우팅)의 정의로 슬라이드에서 제시한 것은?

① 서버의 데이터베이스를 조회하는 기술 ② 웹 애플리케이션에서 다른 페이지 간의 전환과 경로를 관리하는 기술 ③ CSS 스타일을 적용하는 기술 ④ 컴포넌트 간 이벤트를 전달하는 기술

---

### 22. SSR(서버 사이드 렌더링)에서의 Routing에 대한 설명으로 옳은 것은?

① 클라이언트 측 JavaScript가 라우팅을 전담한다 ② 서버가 방문 URL 경로를 기반으로 응답을 전송하며, 링크 클릭 시 전체 페이지가 새 HTML로 다시 로드된다 ③ Ajax 요청을 통해 JSON만 응답받는다 ④ 페이지 리로드가 전혀 발생하지 않는다

---

### 23. CSR(클라이언트 사이드 렌더링)에서의 Routing 특징으로 옳은 것은?

① 라우팅이 서버 측에서 수행된다 ② 클라이언트 측에서 라우팅을 수행하며, 새 데이터를 동적으로 가져와 전체 페이지를 다시 로드하지 않는다 ③ 매 요청마다 전체 HTML을 새로 받는다 ④ Ajax 요청이 사용되지 않는다

---

### 24. SPA(Single Page Application)에 라우팅이 없다면 발생하는 문제로 옳지 않은 것은?

① 새로고침 시 처음 페이지로 되돌아간다 ② 링크 공유 시 첫 페이지만 공유 가능하다 ③ 브라우저의 뒤로 가기 기능을 사용할 수 없다 ④ 서버 응답 속도가 느려진다

---

### 25. Vue Router는 무엇으로 소개되는가?

① Vue의 서드파티 상태 관리 라이브러리 ② Vue 공식 라우터 ③ Vue의 테스트 프레임워크 ④ Vue의 빌드 도구

---

### 26. Vite CLI에서 Vue Router를 추가하기 위해 선택하는 옵션명은?

① Pinia (state management) ② Router (SPA development) ③ Vitest (unit testing) ④ ESLint

---

### 27. Vue Router 추가 시 프로젝트 구조에 발생하는 변화가 아닌 것은?

① App.vue 코드 변화 ② router 폴더 신규 생성 ③ views 폴더 신규 생성 ④ stores 폴더 신규 생성

---

### 28. RouterLink에 대한 설명으로 옳지 않은 것은?

① 페이지를 다시 로드하지 않고 URL을 변경한다 ② 최종적으로 HTML의 `<a>` 태그를 렌더링한다 ③ 최종적으로 HTML의 `<button>` 태그를 렌더링한다 ④ `to` 속성으로 이동할 경로를 지정한다

---

### 29. RouterView의 역할로 옳은 것은?

① RouterLink의 URL에 해당하는 컴포넌트를 표시한다 ② 네비게이션 링크 목록을 렌더링한다 ③ store의 상태를 화면에 출력한다 ④ 페이지 전환 애니메이션을 담당한다

---

### 30. `router/index.js`에 대한 설명으로 옳은 것은?

① 컴포넌트의 스타일을 정의하는 파일이다 ② 라우팅에 관련된 정보 및 설정이 작성되며, URL과 컴포넌트를 매핑한다 ③ Pinia store를 정의하는 파일이다 ④ 반드시 App.vue 내부에 작성해야 한다

---

### 31. views 폴더와 components 폴더의 관계에 대한 설명으로 옳은 것은?

① views 폴더의 컴포넌트만 반응형 상태를 가질 수 있다 ② 기능적으로 다른 것은 없으며 단순 분류 목적으로 구분한다 ③ views 폴더는 반드시 RouterView 없이도 라우팅을 지원한다 ④ components 폴더의 컴포넌트는 라우팅에 사용할 수 없다

---

### 32. views 폴더 내 컴포넌트 이름 작성 관례로 슬라이드가 권장하는 것은?

① 반드시 소문자로 시작해야 한다 ② 컴포넌트 이름을 View로 끝나도록 작성하는 것을 권장한다 (필수는 아님) ③ 파일명에 반드시 숫자를 포함해야 한다 ④ 컴포넌트 이름에 Router를 접두어로 붙여야 한다

---

### 33. 라우팅 기본 3단계의 순서로 옳은 것은?

① RouterView 렌더링 → index.js 설정 → RouterLink 클릭 ② index.js에 라우트 설정 작성 → RouterLink의 to 속성에 path 사용 → 클릭 시 RouterView에 컴포넌트 렌더링 ③ RouterLink 클릭 → index.js 설정 → RouterView 렌더링 ④ views 폴더 생성 → RouterView 렌더링 → index.js 설정

---

### 34. `createRouter()`의 옵션 객체에서 각 라우트를 정의하는 배열의 이름은?

① paths ② links ③ routes ④ views

---

### 35. Named Routes에 대한 설명으로 옳지 않은 것은?

① 경로에 이름을 지정하는 라우팅 방식이다 ② RouterLink에서 이름으로 연결하려면 `to`에 문자열 경로만 전달해야 한다 ③ 하드 코딩된 URL을 사용하지 않아도 되는 장점이 있다 ④ URL 입력 시 오타를 방지할 수 있다

---

### 36. Named Routes 방식으로 홈 링크를 작성한 코드로 옳은 것은?

① `<RouterLink to="/">Home</RouterLink>` ② `<RouterLink :to="{ name: 'home' }">Home</RouterLink>` ③ `<RouterLink name="home">Home</RouterLink>` ④ `<RouterView :to="{ name: 'home' }" />`

---

### 37. Dynamic Route Matching(동적 경로 매칭)에서 매개변수를 표기하는 문법은?

① `{id}` ② `:id` ③ `[id]` ④ `$id`

---

### 38. RouterLink에서 동적 라우트의 매개변수를 전달할 때 사용하는 속성명은?

① query ② props ③ params ④ meta

---

### 39. 컴포넌트 템플릿에서 현재 라우트의 동적 매개변수 id 값을 참조하는 표현으로 옳은 것은?

① `{{ $params.id }}` ② `{{ $route.params.id }}` ③ `{{ route.id }}` ④ `{{ $router.id }}`

---

### 40. 스크립트 내에서 route 객체를 가져와 반응형 변수로 매개변수를 다루기 위해 사용하는 Composition API 함수는?

① `useRouter()` ② `useRoute()` ③ `useParams()` ④ `useStore()`

---

### 41. Programmatic Navigation(프로그래밍 방식 내비게이션)이란 무엇인가?

① CSS로 페이지 전환 애니메이션을 구현하는 것 ② RouterLink 대신 JavaScript를 사용해 페이지를 이동하는 것 ③ 서버에서 리다이렉트를 처리하는 것 ④ Pinia store에서 화면을 그리는 것

---

### 42. router 인스턴스의 메서드 중, RouterLink를 클릭했을 때 내부적으로 호출되는 메서드는?

① `router.replace()` ② `router.push()` ③ `router.go()` ④ `router.back()`

---

### 43. router 인스턴스를 스크립트에서 가져오기 위해 사용하는 Composition API 함수는?

① `useRoute()` ② `useRouter()` ③ `useStore()` ④ `useNavigate()`

---

### 44. named route로 이동하며 매개변수를 함께 전달하는 `router.push()` 코드로 옳은 것은?

① `router.push('/users/1')` ② `router.push({ name: 'user', params: { id: '3' } })` ③ `router.push({ path: 'user', name: '3' })` ④ `router.push(params: { id: '3' })`

---

### 45. Nested Routes(중첩된 라우팅)의 정의로 옳은 것은?

① 컴포넌트 트리의 부모-자식 관계를 표현하는 것 ② URL의 중첩된 관계를 컴포넌트 구조에 따라 표현하는 것 ③ 여러 store를 하나로 병합하는 것 ④ 여러 개의 App.vue를 두는 것

---

### 46. Nested Routes를 설정할 때 하위 라우트들을 배열로 정의하는 옵션명은?

① `nested` ② `children` ③ `sub` ④ `routes`

---

### 47. `children` 배열 안에서 `path: ''`로 지정된 라우트의 의미는?

① 존재할 수 없는 잘못된 설정이다 ② 상위 경로 방문 시 기본(default)으로 표시되는 하위 컴포넌트를 의미한다 ③ 반드시 name을 지정하지 않아야 한다 ④ RouterView를 사용하지 않는 라우트를 의미한다

---

### 48. 중첩된 Named Routes를 다룰 때의 일반적인 관례는?

① 상위 라우트와 하위 라우트 모두 반드시 name을 지정한다 ② 일반적으로 하위 경로에만 이름(name)을 지정한다 ③ 상위 라우트에만 이름을 지정하고 하위는 지정하지 않는다 ④ name은 아예 사용하지 않는다

---

### 49. Navigation Guard의 정의로 옳은 것은?

① CSS 애니메이션을 처리하는 기능 ② 특정 URL 접근 시 다른 URL로 redirect하거나 취소하여 내비게이션을 보호하는 것 ③ store의 상태 변경을 막는 기능 ④ 컴포넌트의 렌더링 순서를 강제하는 기능

---

### 50. Navigation Guard의 종류 3가지에 해당하지 않는 것은?

① Globally (전역 가드) ② Per-route (라우터 가드) ③ In-component (컴포넌트 가드) ④ In-store (스토어 가드)

---

### 51. Lazy Loading Routes(라우트 지연 로딩)의 목적으로 옳은 것은?

① 모든 컴포넌트를 앱 빌드 시 미리 전부 로드하기 위함 ② 해당 경로를 처음 방문할 때 컴포넌트를 로드하여 초기 페이지 로드 시간을 줄이기 위함 ③ Pinia store를 지연 초기화하기 위함 ④ RouterView를 여러 개 두기 위함

---

### 52. Lazy Loading Routes를 구현할 때 `component` 속성에 작성하는 문법은?

① `component: HomeView` ② `component: () => import('../views/AboutView.vue')` ③ `component: lazy(AboutView)` ④ `component: 'AboutView'`

---

### 53. Pinia를 사용해야 할 때에 대한 설명으로 옳은 것은?

① 항상 사용하는 것이 좋으며 규모와 무관하다 ② 애플리케이션이 단순하다면 Pinia가 없는 것이 더 효율적일 수 있고, 중대형 SPA에서 자연스럽게 선택하게 된다 ③ 소규모 프로젝트에만 적합하다 ④ SSR 프로젝트에서는 사용할 수 없다

---

### 54. `router.push({ path: '/register', query: { plan: 'private' } })`의 실행 결과로 생성되는 URL은?

① `/register/private` ② `/register?plan=private` ③ `/register#plan=private` ④ `/register/plan/private`

---

### 55. Pinia state를 컴포넌트에서 사용하기 위한 코드로 옳은 것은?

① `import { useCounterStore } from '@/stores/counter'; const store = useCounterStore(); console.log(store.count)` ② `import CounterStore from '@/stores/counter'; console.log(CounterStore.count)` ③ `this.$store.state.count` ④ `mapState(['count'])`

---

### 56. store에 정의되지 않은 state를 컴포넌트에서 임의로 추가할 수 있는가?

① 가능하다, 어떤 컴포넌트에서든 새로 추가할 수 있다 ② 불가능하다, store에 정의하지 않은 state는 컴포넌트에서 새로 추가할 수 없다 ③ plugin을 사용하면 항상 가능하다 ④ 서버에 요청하면 가능하다

---

### 57. `pinia-plugin-persistedstate` 적용 결과를 개발자도구에서 확인할 수 있는 위치는?

① Network 탭 ② Elements 탭 ③ Application → Local Storage ④ Console 탭의 로그

---

### 58. Vue devtools에서 Pinia 관련 정보를 확인하려면 어느 탭을 선택해야 하는가?

① Console 탭 ② Vue 탭 → Pinia 섹션 ③ Network 탭 ④ Sources 탭

---

### 59. `router.push('/users/1')`처럼 문자열을 그대로 전달하는 방식은 무엇을 의미하는가?

① named route 방식 ② literal string path(문자열 경로) 방식 ③ query 방식 ④ params 방식

---

### 60. `router.push()`와 관련해 브라우저 뒤로 가기와의 관계에 대한 설명으로 옳은 것은?

① `router.push()`는 history stack에 새 항목을 추가하므로 뒤로 가기로 이전 URL로 이동할 수 있다 ② `router.push()`는 history stack을 사용하지 않는다 ③ `router.push()`를 사용하면 뒤로 가기가 항상 비활성화된다 ④ `router.push()`는 현재 URL을 완전히 대체하여 이전 URL이 사라진다

---

## 주관식

### 61. Vue의 공식 상태 관리 라이브러리의 이름을 쓰시오.

---

### 62. Pinia의 구성 요소 5가지를 모두 쓰시오.

---

### 63. Setup Store 문법에서 `ref()`는 Pinia의 무엇에 대응되는가?

---

### 64. Setup Store에서 store 외부에 상태/함수를 노출하기 위해 반드시 작성해야 하는 문법 요소는?

---

### 65. `defineStore()`의 첫 번째 인자로 전달하는 값의 이름(역할)을 쓰시오.

---

### 66. 특정 store에만 persist 기능을 적용할 때 `defineStore()` 세 번째 인자에 전달하는 옵션 객체를 쓰시오.

---

### 67. Local Storage와 달리 네트워크 요청 시 서버로 자동 전송되는 웹 저장 방식은?

---

### 68. CSR 방식에서 라우팅이 이루어질 때, 서버로부터 어떤 형식의 데이터를 받아오는가? (Ajax 요청 응답 형식)

---

### 69. Vue Router 추가 시 CLI에서 선택해야 하는 옵션명을 그대로 쓰시오.

---

### 70. RouterLink가 최종적으로 렌더링하는 HTML 태그는?

---

### 71. 라우팅 설정(경로-이름-컴포넌트 매핑)이 작성되는 파일의 경로를 쓰시오.

---

### 72. `createRouter()`의 옵션 객체 안에서 각 라우트 정보를 담는 배열의 키(key) 이름은?

---

### 73. Named Routes 방식으로 RouterLink를 작성할 때 `to` 속성 앞에 반드시 붙여야 하는 Vue 문법 요소는?

---

### 74. 동적 경로 매칭에서 매개변수(id)를 path에 표기할 때 사용하는 기호를 쓰시오.

---

### 75. 컴포넌트 내에서 현재 라우트의 동적 매개변수에 접근할 때 사용하는 전역 속성명을 쓰시오. (예: `___.params.id`)

---

### 76. RouterLink 대신 JavaScript로 페이지를 이동하는 것을 무엇이라 부르는가?

---

### 77. router 인스턴스에서 현재 위치를 새 URL로 완전히 바꾸는(history에 새 항목을 추가하지 않는) 메서드명을 쓰시오.

---

### 78. 중첩된 라우팅에서 하위 라우트 목록을 정의하는 옵션명을 쓰시오.

---

### 79. Navigation Guard 중 애플리케이션 전역에서 모든 라우트 전환에 적용되는 종류의 이름을 쓰시오.

---

### 80. 라우트를 처음 방문할 때만 해당 컴포넌트를 로드하도록 하여 초기 로딩 시간을 줄이는 기법의 이름을 쓰시오.

---

## 서술형

### 81. 상태 관리의 단순성이 무너지는 두 가지 경우를 각각 설명하시오.

---

### 82. Pinia의 Setup Store 문법에서 state, getters, actions가 Composition API의 어떤 함수와 대응되는지 설명하고, 간단한 예시 코드를 작성하시오.

---

### 83. `pinia-plugin-persistedstate`를 프로젝트에 적용하는 전체 과정을 순서대로 설명하시오.

---

### 84. SSR에서의 라우팅과 CSR에서의 라우팅의 차이를 비교하여 설명하시오.

---

### 85. SPA(Single Page Application)에 라우팅 기능이 없다면 어떤 문제가 발생하는지 설명하시오.

---

### 86. RouterLink와 RouterView의 역할 차이를 설명하시오.

---

### 87. Dynamic Route Matching(동적 경로 매칭)이 필요한 이유와 사용 방법을 예시와 함께 설명하시오.

---

### 88. Named Routes 방식과 Dynamic Route Matching에서 매개변수를 전달하는 방식을 함께 사용하는 코드를 작성하고, params의 key가 지켜야 할 규칙을 설명하시오.

---

### 89. Nested Routes(중첩된 라우팅)의 개념을 설명하고, 이를 컴포넌트의 부모-자식 관계와 혼동하면 안 되는 이유를 설명하시오.

---

### 90. Navigation Guard의 정의와 세 가지 종류를 설명하시오.

---

_— 수고하셨습니다. —_