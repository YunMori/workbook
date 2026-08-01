# Vue Component State Flow 모의고사 — Round 01 v5

> 출제 범위: Component State Flow (props, emit, computed, watch, lifecycle hooks, Virtual DOM)
> 구성: 객관식 40 · 주관식 20 · 서술형 10 (총 70문항)

## 객관식

### 1. Vue에서 부모 컴포넌트가 자식 컴포넌트로 데이터를 전달할 때 사용하는 속성은?

① emit ② props ③ watch ④ computed

---

### 2. 자식 컴포넌트에서 자신에게 일어난 일을 부모 컴포넌트에게 알리는 방법은?

① props ② $emit ③ v-bind ④ v-model

---

### 3. Props의 특징으로 옳지 않은 것은?

① 부모 속성이 업데이트되면 자식으로 전달된다
② 자식 컴포넌트 내부에서 props를 변경하려고 시도해서는 안된다
③ 자식이 props를 변경하면 부모의 값도 함께 변경된다
④ 부모 컴포넌트가 업데이트될 때마다 이를 사용하는 자식의 모든 props가 최신 값으로 업데이트된다

---

### 4. 모든 props가 형성하는 바인딩의 이름은?

① two-way binding ② one-way-down binding ③ bottom-up binding ④ bi-directional binding

---

### 5. props가 단방향으로 설계된 이유로 옳은 것은?

① 서버와의 통신량을 줄이기 위해
② 하위 컴포넌트가 실수로 상위 컴포넌트의 상태를 변경하여 데이터 흐름을 이해하기 어렵게 만드는 것을 방지하기 위해
③ 컴포넌트 렌더링 속도를 높이기 위해
④ 자식 컴포넌트의 재사용성을 없애기 위해

---

### 6. 자식 컴포넌트에서 부모로부터 내려받은 props를 사용하기 위해 명시적으로 선언할 때 사용하는 함수는?

① defineEmits() ② defineProps() ③ defineComponent() ④ defineExpose()

---

### 7. defineProps()의 선언 방식으로 옳지 않은 것은?

① 문자열 배열을 사용한 선언
② 객체를 사용한 선언
③ 함수를 사용한 선언
④ ①, ②만 존재하며 ③은 존재하지 않는다

---

### 8. 다음 중 문자열 배열을 사용한 props 선언 코드는?

① `defineProps({ myMsg: String })`
② `defineProps(['myMsg'])`
③ `defineProps(myMsg: String)`
④ `defineProps.myMsg = String`

---

### 9. 객체를 사용한 props 선언에서 값으로 들어가야 하는 것은?

① props의 초기값
② 데이터 타입에 해당하는 생성자 함수(Number, String 등)
③ 부모 컴포넌트의 이름
④ CSS 클래스명

---

### 10. Vue 슬라이드에서 강조(❖)하며 권장하는 props 선언 방식은?

① 문자열 배열을 사용한 선언
② 객체를 사용한 선언
③ 두 방식 모두 권장하지 않음
④ 두 방식 중 편한 것을 무작위로 사용

---

### 11. props 객체 선언 문법을 권장하는 이유로 옳지 않은 것은?

① 컴포넌트를 가독성 좋게 문서화할 수 있다
② 다른 개발자가 잘못된 유형을 전달했을 때 브라우저 콘솔에 경고가 출력된다
③ props에 대한 유효성 검사로 활용할 수 있다
④ 컴포넌트의 렌더링 속도가 항상 2배 빨라진다

---

### 12. `propC: { type: String, required: true }` 선언이 의미하는 것은?

① 문자열이며 선택적으로 전달 가능
② 문자열이며 필수로 전달되어야 함
③ 숫자이며 기본값이 있음
④ 여러 타입을 허용함

---

### 13. `propD: { type: Number, default: 10 }` 선언이 의미하는 것은?

① 숫자형이며 값이 없을 경우 기본값 10이 사용됨
② 숫자형이며 필수 전달
③ 문자열형이며 기본값 "10"
④ 여러 타입 허용, 기본값 10

---

### 14. 부모 컴포넌트에서 자식 컴포넌트에 props를 전달하는 템플릿 표기 시 권장되는 케이싱은?

① camelCase ② kebab-case ③ snake_case ④ PascalCase

---

### 15. props 선언 및 템플릿 내부에서 참조할 때 사용하는 케이싱은?

① kebab-case ② camelCase ③ UPPER_CASE ④ 케이싱 규칙 없음

---

### 16. `<SomeComponent num-props="1" />` 형태로 전달했을 때 자식이 실제로 받는 값과 타입은?

① 숫자 1 ② 문자열 "1" ③ boolean true ④ undefined

---

### 17. `<SomeComponent :num-props="1" />` 형태로 전달했을 때 자식이 실제로 받는 값과 타입은?

① 문자열 "1" ② 숫자 1 ③ undefined ④ null

---

### 18. v-for와 함께 props를 전달하는 예시로 옳은 것은?

① `<ParentItem v-for="item in items" :key="item.id" :my-prop="item" />`
② `<ParentItem v-for="item in items" my-prop="item" />`
③ `<ParentItem :items="items" />`
④ `<ParentItem v-bind="items" />`

---

### 19. $emit의 '$' 표기가 의미하는 것은?

① 전역 변수
② Vue 인스턴스의 내부 변수(라이프사이클 훅, 인스턴스 메서드 등)에 접근함을 나타냄
③ jQuery 문법의 잔재
④ 반응형 데이터 선언

---

### 20. $emit 메서드의 구조 `$emit(event, ...args)`에서 args가 의미하는 것은?

① 커스텀 이벤트 이름 ② 추가 인자 ③ 이벤트 발생 시점 ④ 부모 컴포넌트의 참조

---

### 21. 자식 컴포넌트에서 커스텀 이벤트를 발신하는 템플릿 코드로 옳은 것은?

① `<button @click="someEvent">클릭</button>`
② `<button @click="$emit('someEvent')">클릭</button>`
③ `<button v-on="someEvent">클릭</button>`
④ `<button emit="someEvent">클릭</button>`

---

### 22. 부모 컴포넌트가 자식이 발신한 커스텀 이벤트를 수신할 때 사용하는 디렉티브는?

① v-bind ② v-on(@) ③ v-model ④ v-if

---

### 23. script 영역에서 발신할 이벤트를 명시적으로 선언할 때 사용하는 함수는?

① defineProps() ② defineEmits() ③ defineEvents() ④ defineExpose()

---

### 24. defineEmits()를 사용하는 이유로 옳은 것은?

① script에서는 $emit 메서드에 접근할 수 없기 때문에 이를 대신할 동등한 함수가 필요하기 때문
② $emit보다 성능이 항상 뛰어나기 때문
③ props를 선언하기 위해 필수적이기 때문
④ 템플릿에서만 사용 가능한 함수이기 때문

---

### 25. `emit('emitArgs', 1, 2, 3)`처럼 이벤트에 추가 인자를 전달했을 때, 부모의 콜백 함수에서 이를 수신하는 형태는?

① 개별 매개변수로 각각 수신
② `(...args) => { console.log(args) }` 형태로 배열로 수신
③ 객체로 자동 병합되어 수신
④ 수신할 수 없음

---

### 26. 이벤트 선언 및 발신 시 사용하는 케이싱과, 부모에서 수신 시 사용하는 케이싱을 순서대로 옳게 짝지은 것은?

① camelCase / camelCase ② kebab-case / kebab-case ③ camelCase / kebab-case ④ kebab-case / camelCase

---

### 27. emit 이벤트를 객체 선언 문법으로 작성할 때 `click: null`처럼 값을 null로 지정하면 어떤 의미인가?

① 이벤트가 비활성화된다
② 해당 이벤트에 대한 유효성 검사가 없음을 의미한다
③ 이벤트가 항상 실패로 처리된다
④ 이벤트 이름이 자동으로 변경된다

---

### 28. emit 이벤트의 객체 선언 문법에서 유효성 검사 함수가 false를 반환하면 어떤 일이 발생하는가?

① 이벤트가 두 번 발신된다 ② console.warn이 출력된다 ③ 부모 컴포넌트가 새로고침된다 ④ 아무 일도 일어나지 않는다

---

### 29. computed()가 정의하는 것은 무엇인가?

① 이벤트 리스너 ② 계산된 속성(computed property)을 정의하는 함수 ③ DOM 엘리먼트 참조 ④ 라이프사이클 훅

---

### 30. computed 속성이 반환하는 것은 무엇인가?

① 일반 배열 ② computed ref ③ Promise ④ 문자열 리터럴

---

### 31. computed와 method의 가장 핵심적인 차이는?

① computed는 데이터를 반환하지 않는다
② computed는 의존된 반응형 데이터를 기반으로 캐시(cached)되며 데이터가 변경될 때만 재평가되지만, method는 호출할 때마다 항상 함수를 실행한다
③ method만 반응형 데이터에 접근할 수 있다
④ computed는 오직 배열 데이터에만 사용할 수 있다

---

### 32. "데이터나 결과를 일시적으로 저장해두는 임시 저장소로, 이후 같은 데이터를 다시 계산하지 않고 빠르게 접근할 수 있도록 하는 것"을 의미하는 용어는?

① Cache ② Watch ③ Reactive ④ Emit

---

### 33. 동일한 의존성을 가진 여러 곳에서 계산 결과를 캐싱하여 중복 계산을 방지하고 싶을 때 적절한 선택은?

① method ② computed ③ watch ④ emit

---

### 34. 데이터 의존 여부와 관계없이 항상 동일한 결과를 반환하거나 단순히 특정 동작을 수행하는 함수를 정의할 때 적절한 선택은?

① computed ② method ③ watch ④ props

---

### 35. watch()의 정의로 옳은 것은?

① 하나 이상의 반응형 데이터를 감시하고, 변경되면 콜백 함수를 호출한다
② 계산된 속성을 캐싱하여 반환한다
③ 부모에서 자식으로 데이터를 전달한다
④ DOM 엘리먼트를 직접 생성한다

---

### 36. `watch(source, (newValue, oldValue) => {...})`에서 두번째 인자인 콜백 함수의 매개변수 중 optional(생략 가능)한 것은?

① newValue ② oldValue ③ source ④ 둘 다 필수

---

### 37. 여러 개의 source를 동시에 감시하는 watch 작성 방식으로 옳은 것은?

① 객체를 사용: `watch({foo, bar}, ...)`
② 배열을 사용: `watch([foo, bar], ([newFoo, newBar], [prevFoo, prevBar]) => {...})`
③ 여러 개의 watch를 이어붙여 작성: `watch(foo).watch(bar)`
④ 여러 source는 감시할 수 없다

---

### 38. Computed와 Watchers의 비교로 옳지 않은 것은?

① Computed는 의존하는 데이터 속성의 계산된 값을 반환한다
② Watchers는 특정 데이터 속성의 변화를 감시하고 side-effect 작업을 수행한다
③ Computed와 Watchers 모두 의존(감시)하는 원본 데이터를 직접 변경한다
④ 둘 다 데이터의 변화를 감지하고 처리한다는 공통점이 있다

---

### 39. DOM 변경, 비동기 작업 수행, 외부 API 연동과 같은 side-effect 작업이 필요할 때 적절한 선택은?

① computed ② watch ③ props ④ static props

---

### 40. computed 사용 시 원본 배열을 변경하지 않기 위한 올바른 코드는?

① `return numbers.reverse()`
② `return numbers.sort()`
③ `return [...numbers].reverse()`
④ `numbers.reverse(); return numbers`

---

## 주관식

### 41. 부모 컴포넌트가 업데이트될 때, 이를 사용하는 자식 컴포넌트의 props는 어떻게 되는가? (한 단어/짧은 구로 답)

---

### 42. 문자열 배열을 사용하여 props를 선언하는 defineProps() 코드를 작성하시오. (props 이름: myMsg)

---

### 43. 객체를 사용하여 props를 선언하는 defineProps() 코드를 작성하시오. (props 이름: myMsg, 타입: String)

---

### 44. `<ParentChild my-msg="message" />`처럼 부모→자식으로 props를 전달할 때 사용하는 속성 표기 케이싱은?

---

### 45. v-bind 없이 정적으로 전달된 문자열 props와 달리, v-bind를 사용하여 동적으로 값을 할당하는 props를 무엇이라 부르는가?

---

### 46. 자식 컴포넌트가 이벤트를 발생시켜 부모 컴포넌트로 데이터를 전달하는 역할의 메서드 이름은?

---

### 47. script에서 $emit 대신 사용할 수 있는 동등한 함수를 반환하는 선언 함수는?

---

### 48. `emit('emitArgs', 1, 2, 3)`처럼 이벤트 발신 시 추가로 전달하는 값들을 무엇이라 부르는가?

---

### 49. 이벤트를 선언 및 발신할 때 사용하는 케이싱은?

---

### 50. '계산된 속성'을 정의하는 함수로, 템플릿에서 표현식을 단순하게 하고 불필요한 반복 연산을 줄이는 함수는?

---

### 51. computed 속성이 캐시된 결과를 즉시 반환하는 조건은 무엇인가? (짧게 서술)

---

### 52. method 호출은 리렌더링이 발생할 때마다 어떻게 동작하는가?

---

### 53. "하나 이상의 반응형 데이터를 감시하고, 감시하는 데이터가 변경되면 콜백 함수를 호출"하는 함수는?

---

### 54. watch(source, callback)에서 callback의 첫 번째 매개변수 이름과, 감시 대상이 변화된 값을 나타내는 것은?

---

### 55. computed와 watch의 공통점 중 슬라이드에서 강조(❖)된 원칙은 무엇인가?

---

### 56. computed 내부에서 배열을 정렬/역순 처리할 때 원본 배열을 변경하지 않기 위해 사용하는 문법은?

---

### 57. Vue 인스턴스의 생애주기 동안 특정 시점에 실행되는 함수를 무엇이라 부르는가?

---

### 58. 가장 일반적으로 사용되는 Lifecycle Hooks 3가지를 쓰시오.

---

### 59. Lifecycle Hooks에 등록된 콜백 함수가 Vue 인스턴스와 자동으로 연결되어 정상 동작하려면 hooks 함수는 어떻게 작성되어야 하는가?

---

### 60. 가상의 DOM을 메모리에 저장하고 실제 DOM과 동기화하는 프로그래밍 개념을 무엇이라 부르는가?

---

## 서술형

### 61. Props와 $emit을 이용한 부모-자식 컴포넌트 간 데이터 흐름을 설명하시오. (4점)

---

### 62. props가 단방향 데이터 흐름(one-way-down binding)으로 설계된 이유와, 자식 컴포넌트가 부모의 데이터를 직접 변경하려 할 때 발생하는 문제를 설명하시오. (4점)

---

### 63. defineProps()의 "문자열 배열" 선언 방식과 "객체" 선언 방식의 차이를 비교하고, 왜 객체 선언 문법이 권장되는지 설명하시오. (4점)

---

### 64. Props Name Casing과 Event Name Casing 규칙을 각각 설명하고, 왜 이런 케이싱 차이가 존재하는지 설명하시오. (4점)

---

### 65. Static Props와 Dynamic Props의 차이를 예시와 함께 설명하시오. (3점)

---

### 66. Computed와 Method의 차이를 캐싱(cache) 관점에서 설명하고, 각각 어떤 상황에 사용하는 것이 적절한지 설명하시오. (4점)

---

### 67. Computed와 Watchers를 사용 목적과 동작 방식 측면에서 비교하여 설명하시오. (4점)

---

### 68. computed 사용 시 주의해야 할 두 가지 사항(반환 값 변경 금지, 원본 배열 변경 금지)을 예시와 함께 설명하시오. (4점)

---

### 69. Lifecycle Hooks 중 onMounted와 onUpdated의 역할을 설명하고, 이들이 자동으로 인스턴스와 연결되어 정상 동작하기 위해 지켜야 할 조건을 설명하시오. (3점)

---

### 70. Virtual DOM의 개념과 장점, 그리고 실제 DOM에 직접 접근해야 할 때 Vue에서 권장하는 방법을 설명하시오. (4점)

---

_— 수고하셨습니다. —_
