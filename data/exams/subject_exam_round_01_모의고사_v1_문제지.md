# JS DOM과 Event 모의고사 — Version 1

---

## 객관식

**1.** 반복문에서 `for (let i = 0; i < arr.length; i++) {...}`의 `i`를 `const`로 선언하면 어떤 문제가 발생하는가?

① 아무 문제 없이 정상 동작한다
② `i`가 매 반복마다 재할당되므로 에러가 발생한다
③ 반복문이 무한 루프에 빠진다
④ `undefined`가 반환된다

---

**2.** `for...in`, `for...of` 반복문에서 반복 변수를 `const`로 선언해도 에러가 나지 않는 이유는?

① 두 반복문은 변수를 사용하지 않기 때문
② 매 반복마다 재할당이 아니라 새로운 값이 "새로 지정"되기 때문
③ `let`으로 자동 변환되기 때문
④ 두 반복문은 블록 스코프가 아니기 때문

---

**3.** `while`, `for`, `for...in`, `for...of` 반복문의 공통된 스코프 특성은?

① 전역 스코프
② 함수 스코프
③ 블록 스코프
④ 모듈 스코프

---

**4.** JavaScript를 실행할 수 있는 환경으로 슬라이드에서 언급되지 않은 것은?

① HTML `<script>` 태그 내부에 직접 작성
② `.js` 확장자 파일을 `<script src="...">`로 연결
③ 브라우저 Console
④ 서버의 `.env` 설정 파일

---

**5.** DOM(Document Object Model)에 대한 설명으로 옳지 않은 것은?

① 웹 페이지(Document)를 구조화된 객체로 제공한다
② 프로그래밍 언어가 페이지 구조에 접근할 수 있게 한다
③ 문서의 구조, 스타일, 내용을 변경할 수 있다
④ CSS 파일만을 객체로 표현하는 모델이다

---

**6.** DOM에서 모든 요소, 속성, 텍스트가 공통으로 속하는 최상위 객체는?

① `window`
② `document`
③ `navigator`
④ `location`

---

**7.** 브라우저가 HTML 문서를 해석하여 객체 트리로 구조화하는 것을 무엇이라 하는가?

① Event Loop
② DOM Tree
③ Call Stack
④ Shadow Tree

---

**8.** `document.title = 'Hello :)'`를 실행하면 어떤 일이 일어나는가?

① 아무 변화 없음
② 콘솔에 에러 발생
③ 브라우저 탭 제목(HTML `<title>`)이 변경됨
④ 페이지가 새로고침됨

---

**9.** 웹 페이지를 동적으로 조작하는 순서로 옳은 것은?

① 조작 → 선택
② 선택(탐색) → 조작
③ 생성 → 삭제
④ 삭제 → 생성

---

**10.** `document.querySelector(selector)`에 대한 설명으로 옳은 것은?

① 조건에 맞는 모든 요소를 NodeList로 반환한다
② 조건에 맞는 첫 번째 요소를 반환하며, 없으면 null을 반환한다
③ 조건에 맞는 요소가 없으면 에러를 던진다
④ HTMLCollection을 반환한다

---

**11.** `document.querySelectorAll(selector)`의 반환 타입은?

① HTMLCollection
② Array
③ NodeList
④ DOMTokenList

---

**12.** `querySelectorAll()`로 얻은 NodeList의 특징으로 옳은 것은?

① DOM 변경사항을 실시간으로 반영한다 (live)
② DOM 변경사항을 실시간으로 반영하지 않는다
③ 배열 메서드를 전혀 사용할 수 없다
④ 항상 length가 1이다

---

**13.** DOM 조작의 4가지 분류에 해당하지 않는 것은?

① 속성(attribute) 조작
② HTML 콘텐츠 조작
③ DOM 요소 조작
④ 네트워크 요청 조작

---

**14.** `classList` property가 반환하는 자료구조는?

① Array
② NodeList
③ DOMTokenList
④ HTMLCollection

---

**15.** `element.classList.toggle('red')`를 호출했을 때, 이미 `red` 클래스가 존재하는 경우의 동작과 반환값은?

① 클래스를 추가하고 true 반환
② 클래스를 제거하고 false 반환
③ 아무 것도 하지 않고 undefined 반환
④ 에러 발생

---

**16.** 요소의 특정 속성 값을 조회하는 메서드는?

① `Element.setAttribute(name, value)`
② `Element.getAttribute(name)`
③ `Element.removeAttribute(name)`
④ `Element.hasAttribute(name)`

---

**17.** `aTag.removeAttribute('href')`를 실행한 후 `aTag.getAttribute('href')`를 호출하면 반환값은?

① 빈 문자열 `''`
② `undefined`
③ `null`
④ 에러 발생

---

**18.** `textContent` property에 대한 설명으로 옳은 것은?

① HTML 마크업까지 해석하여 렌더링한다
② 요소의 순수 텍스트 콘텐츠만 표현하며, 태그는 무시한다
③ 요소의 속성 값을 반환한다
④ 인라인 스타일을 반환한다

---

**19.** `innerHTML`을 사용할 때 특히 주의해야 하는 보안 위험은?

① SQL Injection
② XSS(Cross-Site Scripting)
③ CSRF
④ DDoS

---

**20.** `document.createElement(tagName)`에 대한 설명으로 옳은 것은?

① 작성한 tagName의 HTML 요소를 생성하여 반환한다
② DOM에서 요소를 즉시 제거한다
③ 이미 존재하는 요소를 복제한다
④ 요소의 속성만 초기화한다

---

**21.** `Node.appendChild()`에 대한 설명으로 옳은 것은?

① 부모 Node의 첫 번째 자식으로 삽입한다
② 부모 Node의 자식 NodeList 중 마지막 자식으로 삽입하고, 추가된 Node를 반환한다
③ 형제 노드 사이에 삽입한다
④ 반환값이 없다

---

**22.** `Node.removeChild()`가 반환하는 값은?

① `true`/`false`
② `undefined`
③ 제거된 Node
④ 부모 Node

---

**23.** DOM의 Node 종류에 해당하지 않는 것은?

① Document Node
② Element Node
③ Text Node
④ Function Node

---

**24.** NodeList의 특징으로 옳지 않은 것은?

① 배열과 유사한 구조를 가진다
② Index로만 각 항목에 접근할 수 있다
③ JavaScript 배열 메서드를 사용할 수 있다
④ 모든 NodeList는 항상 DOM 변경을 실시간 반영한다(live)

---

**25.** Node와 Element의 관계 설명으로 옳은 것은?

① 모든 Node는 Element이다
② 모든 Element는 Node이지만, 모든 Node가 Element인 것은 아니다
③ Node와 Element는 서로 무관하다
④ Element가 Node보다 상위 개념이다

---

**26.** 브라우저가 문자열을 해석하여 DOM Tree로 만드는 과정을 무엇이라 하는가?

① Rendering
② Parsing
③ Bundling
④ Transpiling

---

**27.** 함수가 속하는 자료형 분류로 옳은 것은?

① 원시 자료형(Primitive type)
② 참조 자료형(Reference type)
③ 둘 다 아님
④ 상황에 따라 다름

---

**28.** 원시 자료형(Primitive type)에 해당하지 않는 것은?

① Number
② String
③ Boolean
④ Array

---

**29.** 함수 정의 시 `return` 문이 없다면 기본으로 반환되는 값은?

① `null`
② `undefined`
③ `0`
④ 빈 문자열

---

**30.** 함수 선언식(function declaration)과 함수 표현식(function expression)의 차이로 옳은 것은?

① 선언식은 호이스팅되지 않지만, 표현식은 호이스팅된다
② 선언식은 호이스팅되지만, 표현식은 호이스팅되지 않는다
③ 둘 다 호이스팅되지 않는다
④ 둘 다 익명 함수를 사용할 수 없다

---

**31.** `const sub = function(num1, num2) {...}`처럼 함수 표현식으로 정의된 `sub`를 정의 이전에 호출하면 어떤 에러가 발생하는가?

① `TypeError`
② `SyntaxError`
③ `ReferenceError: Cannot access 'sub' before initialization`
④ 에러 없이 `undefined` 반환

---

**32.** 슬라이드에서 강조된 함수 정의 권장 방식은?

① 선언식 사용 권장
② 표현식 사용 권장
③ 둘 다 사용 금지
④ 화살표 함수만 사용 금지

---

**33.** 기본 함수 매개변수(Default function parameter)가 적용되는 조건은?

① 인자를 아예 전달하지 않거나 `undefined`를 전달한 경우
② 인자로 `null`을 전달한 경우
③ 인자로 `0`을 전달한 경우
④ 인자를 2개 이상 전달한 경우

---

**34.** 나머지 매개변수(Rest parameters) 작성 규칙으로 옳은 것은?

① 한 함수에 여러 개 작성할 수 있다
② 매개변수 목록 중 어디에나 위치할 수 있다
③ 하나만 작성 가능하며, 반드시 매개변수 목록의 마지막에 위치해야 한다
④ 배열이 아닌 객체로 인자를 받는다

---

**35.** `function threeArgs(a, b, c) {...}`를 `threeArgs(1)`로 호출하면 `b`, `c`에 할당되는 값은?

① `null`, `null`
② `undefined`, `undefined`
③ `0`, `0`
④ 에러 발생

---

**36.** Spread syntax(전개 구문, `...`)에 대한 설명으로 옳은 것은?

① 반복 가능한 항목을 펼치는(확장) 구문이다
② 함수 정의에서만 사용할 수 있다
③ 배열을 문자열로 변환하는 구문이다
④ 항상 얕은 복사가 아닌 깊은 복사를 수행한다

---

**37.** 화살표 함수에서 함수 본문이 표현식 한 줄이고 객체를 반환하고 싶을 때 올바른 작성법은?

① `() => { key: 'value' }`
② `() => ({ key: 'value' })`
③ `() => key: 'value'`
④ `() => return { key: 'value' }`

---

**38.** ASI(Automatic Semicolon Insertion)에 대한 설명으로 옳은 것은?

① JS 문법상 세미콜론은 절대 생략할 수 없다
② 문장 마지막 세미콜론이 없으면 자동으로 삽입해주는 JS의 특성이다
③ ASI는 ES6부터 폐지되었다
④ ASI는 화살표 함수에서만 적용된다

---

**39.** `var` 키워드의 특징으로 옳지 않은 것은?

① 재할당과 재선언이 모두 가능하다
② 함수 스코프(function scope)를 가진다
③ 블록 스코프를 가져 `let`/`const`보다 안전하다
④ 호이스팅 특성으로 인해 예기치 못한 문제가 발생할 수 있다

---

**40.** `addEventListener`로 등록한 콜백을 **화살표 함수**로 작성했을 때, 콜백 내부의 `this`가 가리키는 것은?

① 이벤트가 발생한 버튼 요소
② `event.currentTarget`
③ `window` (상위 스코프의 this)
④ `null`

---

## 주관식

**41.** `getElementById`, `getElementsByClassName`, `getElementsByTagName`이 반환하는, DOM 변경사항을 실시간으로 반영하는 자료구조의 이름은?

---

**42.** DOM Tree의 진입점이며, 페이지를 구성하는 모든 객체 요소를 포함하는 객체의 이름은?

---

**43.** 지정한 이름의 속성 값을 설정(추가 또는 갱신)하는 Element 메서드의 이름을 작성하시오.

---

**44.** `document.createElement(tagName)`으로 생성한 요소를 실제 DOM에 삽입하려면 부모 요소에서 어떤 메서드를 호출해야 하는가?

---

**45.** Parsing 이후 브라우저 렌더링 파이프라인에서 진행되는 두 단계(Parse 다음 순서)를 순서대로 쓰시오.

---

**46.** 함수 표현식의 특징 중, 함수 이름 없이 정의하는 함수를 무엇이라 부르는가?

---

**47.** 매개변수 개수보다 인자를 더 많이 전달했을 때, 초과 입력된 인자는 어떻게 처리되는가? (한 단어/짧은 구절로 답하시오)

---

**48.** 임의의 수의 인자를 배열로 허용하여 가변 인자를 나타내는 매개변수 방식의 이름은?

---

**49.** `myFunc(...numbers)`처럼 배열을 함수 인자로 펼쳐서 전달하는 구문의 이름은?

---

**50.** 화살표 함수에서 매개변수가 하나뿐일 때 생략 가능한 문법 요소는?

---

**51.** `let`/`const`로 선언한 변수를 선언 이전에 참조하면 발생하는 에러 메시지에 포함되는 핵심 용어는?

---

**52.** `var` 키워드 없이 변수를 선언하면(예: `x = 10`) 암묵적으로 어떤 키워드로 선언된 것과 같은 효과가 나는가?

---

**53.** DOM에서 이벤트가 발생했을 때 생성되는, mouse/input/keyboard/touch 등의 종류를 갖는 객체의 이름은?

---

**54.** 이벤트가 발생했을 때 실행되는, "사용자의 행동에 어떻게 반응할지를 JavaScript 코드로 표현한 것"을 무엇이라 하는가?

---

**55.** `EventTarget.addEventListener(type, handler)`에서 `type` 인자에는 어떤 자료형의 값이 들어가는가?

---

**56.** 한 요소에서 발생한 이벤트가 자신의 핸들러를 실행한 뒤 부모 요소로 순차적으로 전파되며 각 핸들러를 실행시키는 현상의 이름은?

---

**57.** 이벤트 버블링에서 "이벤트 핸들러가 연결된 요소"를 가리키는 속성의 이름은?

---

**58.** 이벤트 버블링에서 "실제로 이벤트가 발생한 가장 안쪽 요소"를 가리키는 속성의 이름은?

---

**59.** 해당 이벤트의 기본 동작(예: form 제출 시 새로고침, a 태그 클릭 시 페이지 이동)을 실행하지 않도록 막는 메서드의 이름은?

---

**60.** `innerHTML`과 대비하여, HTML 마크업을 해석하지 않고 순수 텍스트만 다루는 property의 이름은?

---

## 서술형

**61.** `document.querySelector()`와 `document.querySelectorAll()`의 차이를 반환하는 요소의 개수와 반환 타입 관점에서 설명하시오.

---

**62.** `innerHTML`과 `textContent`의 차이를 동작 방식과 보안 측면에서 설명하시오.

---

**63.** Node, NodeList, Element의 관계를 설명하시오.

---

**64.** 함수 선언식(function declaration)과 함수 표현식(function expression)의 차이를 호이스팅 관점에서 설명하고, 슬라이드가 권장하는 방식을 언급하시오.

---

**65.** 기본 함수 매개변수(Default function parameter)와 나머지 매개변수(Rest parameters)의 차이를 예시와 함께 설명하시오.

---

**66.** `addEventListener`의 콜백 함수를 일반 함수(function 키워드)로 작성했을 때와 화살표 함수로 작성했을 때, `this`가 각각 무엇을 가리키는지 설명하고 이유를 서술하시오.

---

**67.** 이벤트 버블링이 무엇인지 설명하고, `event.currentTarget`과 `event.target`의 차이를 예시(중첩된 div 구조)를 들어 설명하시오.

---

**68.** `event.preventDefault()`가 필요한 이유와 실제 활용 예시 두 가지를 서술하시오.

---

**69.** `classList`를 이용해 클래스를 토글하는 세 가지 방식(add/remove 조합, toggle, if문 분기)을 각각 간단히 설명하시오.

---

**70.** `var`와 `let`/`const`의 스코프 및 호이스팅 차이를 설명하고, ES6 이후 `var` 대신 `let`/`const`가 권장되는 이유를 서술하시오.

---

_— 수고하셨습니다. —_
