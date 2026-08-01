# JS 비동기(Asynchronous) 모의고사 — Version 2

---

## 객관식

**1.** 다음 중 객체(Object)에 대한 설명으로 옳은 것은?

① 순서가 있는 데이터 집합을 저장하는 자료형이다 ② 키로 구분된 데이터 집합을 저장하는 자료형이다 ③ 반드시 숫자형 키만 가질 수 있다 ④ 함수는 객체의 속성 값으로 사용할 수 없다

---

**2.** 객체의 속성(key)에 대한 설명으로 틀린 것은?

① key는 문자형만 허용된다 ② value는 모든 자료형이 허용된다 ③ key 이름에 띄어쓰기가 있으면 점(`.`) 표기법으로 접근할 수 없다 ④ key는 숫자형이어야 한다

---

**3.** 다음 코드의 실행 결과는?

```js
const user = { name: "Alice" };
console.log("greeting" in user);
```

① true ② false ③ undefined ④ TypeError 발생

---

**4.** 객체의 속성에 정의된 함수를 부르는 명칭과 호출 방식으로 옳은 것은?

① 함수(Function), `function()` ② 메서드(Method), `object.method()` ③ 프로퍼티(Property), `object.property` ④ 콜백(Callback), `callback()`

---

**5.** `this` 키워드에 대한 설명으로 옳은 것은?

① 함수나 메서드를 정의한 위치에 따라 값이 고정된다 ② 함수나 메서드를 호출한 객체를 가리키는 키워드이다 ③ 항상 전역 객체를 가리킨다 ④ 화살표 함수에서만 사용할 수 있다

---

**6.** 다음 코드의 실행 결과는?

```js
const myFunc = function () {
  return this;
};
console.log(myFunc());
```

① undefined ② myFunc 함수 자체 ③ window(전역 객체) ④ null

---

**7.** 다음 코드의 실행 결과는?

```js
const myObj = {
  data: 1,
  myFunc: function () {
    return this;
  },
};
console.log(myObj.myFunc());
```

① window ② undefined ③ myObj ④ 1

---

**8.** forEach 콜백 내부에서 일반 함수(function)를 사용했을 때 this가 window를 가리키는 문제를 해결하는 방법으로 옳은 것은?

① `var` 대신 `let`을 사용한다 ② 콜백 함수를 화살표 함수로 작성한다 ③ forEach 대신 for문을 사용해야만 해결된다 ④ 해결할 수 없다

---

**9.** JavaScript의 this에 대한 설명 중 슬라이드에서 강조한 내용으로 옳은 것은?

① Python의 self, Java의 this처럼 선언 시 값이 이미 정해진다 ② 함수가 호출되기 전까지 값이 할당되지 않고, 호출 시에 동적으로 결정된다 ③ 클래스 내부에서만 사용 가능하다 ④ 항상 함수가 정의된 객체를 가리킨다

---

**10.** this가 동적으로 할당되는 것의 장점으로 슬라이드에서 언급한 것은?

① 하나의 함수(메서드)를 만들어 여러 객체에서 재사용할 수 있다 ② 코드 실행 속도가 빨라진다 ③ 메모리 사용량이 줄어든다 ④ 항상 예측 가능한 값을 반환한다

---

**11.** 다음 중 객체 리터럴의 "단축 속성" 문법을 올바르게 사용한 것은? (키 이름과 변수 이름이 같은 경우)

① `{ name: name, age: age }` ② `{ name, age }` ③ `{ 'name', 'age' }` ④ `{ [name]: [age] }`

---

**12.** 다음 중 단축 메서드 문법으로 옳은 것은?

① `myFunc: function() { return 'Hello' }` ② `myFunc = function() { return 'Hello' }` ③ `myFunc() { return 'Hello' }` ④ `function myFunc() { return 'Hello' }`

---

**13.** 계산된 속성(computed property name)에 대한 설명으로 옳은 것은?

① 키를 소괄호(`()`)로 감싸서 작성한다 ② 키가 대괄호(`[]`)로 둘러싸이며, 고정 값이 아닌 변수 값을 키로 사용할 수 있다 ③ 값(value)만 계산식으로 작성 가능하다 ④ ES5부터 지원되는 문법이다

---

**14.** 다음 코드에서 사용된 문법의 이름으로 옳은 것은?

```js
function printInfo({ name, age, city }) {
  console.log(`이름: ${name}, 나이: ${age}, 도시: ${city}`);
}
```

① 전개 구문 ② 계산된 속성 ③ 구조 분해 할당 ④ 단축 속성

---

**15.** 다음 코드의 실행 결과는?

```js
const obj = { b: 2, c: 3, d: 4 };
const newObj = { a: 1, ...obj, e: 5 };
console.log(newObj);
```

① `{a: 1, e: 5}` ② `{b: 2, c: 3, d: 4}` ③ `{a: 1, b: 2, c: 3, d: 4, e: 5}` ④ SyntaxError 발생

---

**16.** 객체의 key 목록과 value 목록을 각각 배열로 반환하는 메서드 쌍으로 옳은 것은?

① `Object.entries()` / `Object.values()` ② `Object.keys()` / `Object.values()` ③ `Object.getKeys()` / `Object.getValues()` ④ `Object.list()` / `Object.data()`

---

**17.** JSON에 대한 설명으로 옳은 것은?

① JavaScript의 Object 자료형과 완전히 동일한 자료형이다 ② JSON은 형식이 있는 "문자열"이다 ③ JSON은 배열만 표현할 수 있다 ④ JSON은 JS에서 바로 객체처럼 속성 접근이 가능하다

---

**18.** 배열(Array)의 정의로 옳은 것은?

① 키로 구분된 데이터 집합을 저장하는 자료형 ② 순서가 있는 데이터 집합을 저장하는 자료구조 ③ 중복을 허용하지 않는 데이터 집합 ④ 고정된 크기의 데이터 집합

---

**19.** 배열 끝에서 요소를 추가/제거하는 메서드 쌍은?

① `shift` / `unshift` ② `push` / `pop` ③ `pop` / `push` ④ `unshift` / `push`

---

**20.** Array Helper Methods의 공통적인 특징으로 슬라이드에서 강조한 것은?

① 항상 원본 배열을 직접 수정한다 ② 메서드 호출 시 인자로 함수(콜백함수)를 받는 것이 특징이다 ③ ES5 이전부터 존재했다 ④ 반환 값이 없다

---

**21.** forEach와 map의 가장 큰 차이는?

① forEach는 콜백을 받지 않는다 ② map은 콜백 호출 결과를 모아 새로운 배열을 반환하지만, forEach는 반환 값이 없다(undefined) ③ forEach만 index를 사용할 수 있다 ④ map은 원본 배열을 직접 수정한다

---

**22.** forEach의 콜백 함수가 받을 수 있는 매개변수 구성으로 옳은 것은?

① `(index)` ② `(item, index, array)` ③ `(array, item)` ④ `(callback, index)`

---

**23.** 다음 코드의 실행 결과 중 첫 번째 줄로 옳은 것은?

```js
const names = ["Alice", "Bella", "Cathy"];
names.forEach(function (name, index, array) {
  console.log(`${name} / ${index} / ${array}`);
});
```

① `Alice / 0 / Alice,Bella,Cathy` ② `0 / Alice / Alice,Bella,Cathy` ③ `Alice / 1 / Alice,Bella,Cathy` ④ `Alice / 0 / [Alice, Bella, Cathy]`

---

**24.** 배열 순회 방법 비교 중 옳은 것은?

① for loop는 break/continue를 사용할 수 없다 ② for...of는 break/continue를 사용할 수 없다 ③ forEach는 break/continue를 사용할 수 없으며 사용이 권장된다 ④ forEach는 break/continue를 사용할 수 있다

---

**25.** 다음 중 콜백의 반환 값이 참인 요소들만 모아 새로운 배열로 반환하는 메서드는?

① find ② filter ③ some ④ every

---

**26.** 다음 중 콜백의 반환 값이 처음으로 참이 되는 "요소 자체"를 반환하는 메서드는?

① find ② filter ③ map ④ forEach

---

**27.** 배열의 모든 요소가 조건을 통과해야 true를 반환하고, 하나라도 실패하면 즉시 false를 반환하며 순회를 중지하는 메서드는?

① some ② every ③ find ④ filter

---

**28.** 배열 요소 중 하나라도 조건을 통과하면 즉시 true를 반환하는 메서드는?

① every ② some ③ find ④ filter

---

**29.** "배열은 객체다"라는 슬라이드 내용과 관련해 옳은 것은?

① 배열의 키는 문자열이다 ② 배열은 인덱스를 키로 가지며 length 속성을 갖는 특수한 객체이다 ③ 배열은 객체와 완전히 다른 자료형이다 ④ 배열에는 length 속성이 존재하지 않는다

---

**30.** `Object.getOwnPropertyDescriptors(numbers)`로 배열을 확인했을 때 length 속성의 특징으로 옳은 것은?

① writable: false, enumerable: true ② writable: true, enumerable: false, configurable: false ③ writable: false, configurable: true ④ enumerable: true, configurable: true

---

**31.** Synchronous(동기)의 정의로 옳은 것은?

① 프로그램의 실행 흐름이 순차적으로 진행되며, 하나의 작업이 완료된 후 다음 작업이 실행되는 방식 ② 작업 완료를 기다리지 않고 동시에 여러 작업을 수행하는 방식 ③ 여러 스레드가 동시에 작업을 처리하는 방식 ④ 이벤트 루프를 사용하는 처리 방식

---

**32.** Asynchronous(비동기)의 정의로 옳은 것은?

① 작업이 완료되기를 기다리지 않고 다음 작업이 실행되는 방식 ② 반드시 순서대로 작업을 처리하는 방식 ③ 하나의 스레드로 한 번에 한 작업만 수행하는 방식 ④ Call Stack만으로 모든 처리가 끝나는 방식

---

**33.** JavaScript가 Single Thread 언어라는 것의 의미로 옳은 것은?

① 여러 작업을 동시에 병렬로 처리할 수 있다 ② 한 번에 하나의 작업만 수행할 수 있어 요청한 순서대로 처리할 수 밖에 없다 ③ 스레드가 없는 언어다 ④ 비동기 처리가 불가능한 언어다

---

**34.** 브라우저 환경에서 JavaScript 비동기 처리를 가능하게 하는 4가지 핵심 요소가 아닌 것은?

① Call Stack ② Web API ③ Task Queue ④ Virtual DOM

---

**35.** Call Stack에 대한 설명으로 옳은 것은?

① FIFO(선입선출) 구조이다 ② LIFO(후입선출) 구조이며 JavaScript의 Single Thread 작업을 기본적으로 처리한다 ③ 브라우저가 제공하는 런타임 환경이다 ④ 비동기 콜백 함수만 저장하는 공간이다

---

**36.** Web API에 대한 설명으로 옳은 것은?

① JavaScript 엔진 내부에 포함된 기능이다 ② JavaScript 엔진이 아닌, 브라우저가 제공하는 런타임 환경으로 시간이 소요되는 작업을 처리한다 ③ FIFO 구조의 대기열이다 ④ Call Stack이 비었는지 계속 감시하는 역할을 한다

---

**37.** Task Queue(Callback Queue)와 Event Loop에 대한 설명으로 옳은 것은?

① Task Queue는 LIFO 구조이며 Event Loop는 Call Stack만 감시한다 ② Task Queue는 FIFO 구조로 비동기 처리된 콜백 함수가 대기하며, Event Loop는 Call Stack이 비었을 때 Task Queue의 가장 오래된 작업을 Call Stack으로 보낸다 ③ Event Loop는 Web API 내부에서만 동작한다 ④ Task Queue는 동기 작업만 저장한다

---

**38.** AJAX의 정확한 풀네임(약자)은?

① Asynchronous JavaScript and XML ② Advanced JavaScript and XML ③ Asynchronous Java and XML ④ Automated JavaScript API for XML

---

**39.** AJAX의 'X'는 XML을 의미하지만, 최근 더 많이 사용되는 데이터 형식은?

① HTML ② YAML ③ JSON ④ CSV

---

**40.** XMLHttpRequest(XHR) 객체에 대한 설명으로 틀린 것은?

① 서버와 상호작용할 때 사용하는 객체이다 ② 이름에 XML이 들어가므로 XML 데이터만 가져올 수 있다 ③ 사용자의 작업을 방해하지 않고 페이지 일부를 업데이트할 수 있다 ④ 요청의 상태와 응답을 모니터링할 수 있다

---

## 주관식

**41.** 객체 리터럴에서 key 이름에 띄어쓰기 등이 포함되어 점(.) 표기법으로 접근할 수 없을 때 사용해야 하는 접근 방식(기호)은?

---

**42.** 객체의 속성을 삭제할 때 사용하는 연산자(키워드)는?

---

**43.** 함수나 메서드를 호출한 객체를 가리키며, 호출 방식에 따라 값이 동적으로 결정되는 JavaScript 키워드는?

---

**44.** 화살표 함수가 중첩 함수의 this 문제를 해결할 수 있는 이유를, "자신만의 this"라는 표현을 포함해 한 문장으로 서술하시오.

---

**45.** 객체 리터럴에서 `[product]: 5`처럼 대괄호로 감싼 키에 변수 값을 사용하는 문법의 이름은?

---

**46.** 배열이나 객체를 분해하여 속성 값을 변수에 쉽게 할당하는 문법의 이름은?

---

**47.** 객체를 복사하거나 다른 객체 내부에 펼쳐 넣을 때 사용하는 `...` 문법의 이름은?

---

**48.** 객체의 key 목록만 배열로 반환하는 메서드 이름을 쓰시오.

---

**49.** JSON의 정식 명칭(풀네임)을 쓰시오.

---

**50.** 배열 앞쪽에서 요소를 제거하는 메서드 이름을 쓰시오.

---

**51.** Array Helper Methods 중, 배열의 각 요소에 대해 콜백을 호출하고 그 결과 값을 모아 새로운 배열로 반환하는 메서드 이름을 쓰시오.

---

**52.** 다음 코드의 출력 결과를 쓰시오.

```js
const numbers = [1, 2, 3];
const doubleNumber = numbers.map((number) => number * 2);
console.log(doubleNumber);
```

---

**53.** 배열 순회 방법 중 break와 continue를 사용할 수 없는 메서드 이름을 쓰시오.

---

**54.** 배열 요소 중 조건을 만족하는 "첫 번째 요소 자체"를 반환하는 메서드 이름을 쓰시오. (배열이 아님)

---

**55.** `Object.getOwnPropertyDescriptors(numbers)`로 배열을 확인했을 때, 배열이 가지고 있는 요소 개수를 나타내는 특수한 속성 이름을 쓰시오.

---

**56.** 프로그램 실행 흐름이 순차적으로 진행되며, 하나의 작업이 완료된 후 다음 작업이 실행되는 처리 방식을 무엇이라 하는가?

---

**57.** 브라우저 환경에서 시간이 소요되는 작업(setTimeout, DOM Event, 비동기 요청 등)을 처리하는, JavaScript 엔진이 아닌 브라우저 제공 런타임 환경의 이름을 쓰시오.

---

**58.** Call Stack이 비어있는지 계속 체크하고, 비어 있으면 Task Queue의 가장 오래된 작업을 Call Stack으로 보내는 역할을 하는 요소의 이름을 쓰시오.

---

**59.** Call Stack의 자료구조 방식(선입선출/후입선출 중)을 쓰시오.

---

**60.** Web API에서 처리가 끝난 작업이 곧바로 Call Stack에 들어가지 못하고 순서대로 대기하는 FIFO 구조의 이름을 쓰시오.

---

## 서술형

**61.** 동기(Synchronous)와 비동기(Asynchronous)의 차이를 슬라이드의 정의를 바탕으로 서술하시오.

---

**62.** JavaScript는 Single Thread 언어임에도 불구하고 어떻게 비동기 처리가 가능한지, Call Stack·Web API·Task Queue·Event Loop 4가지 요소를 모두 포함하여 설명하시오.

---

**63.** `this` 키워드가 단순 호출과 메서드 호출에서 각각 무엇을 가리키는지 예시 코드와 함께 설명하시오.

---

**64.** forEach와 map의 공통점과 차이점을 비교하여 서술하시오.

---

**65.** AJAX의 개념과 목적을 기존(전통적인) 웹 페이지 갱신 방식과 비교하여 서술하시오.

---

**66.** 비동기 콜백 방식의 한계인 "콜백 지옥(Callback Hell)"이 무엇인지, 그리고 이를 해결하기 위해 등장한 개념을 서술하시오.

---

**67.** Promise가 비동기 콜백과 비교했을 때 보장하는 것이 무엇인지 서술하시오.

---

**68.** Axios의 정의와 특징을 XHR 객체와 관련지어 서술하시오.

---

**69.** Axios의 then과 catch의 동작 방식과 체이닝(chaining)이 가능한 이유를 서술하시오.

---

**70.** 웹 애플리케이션에서 비동기 처리를 사용하는 이유를 사용자 경험(UX) 관점에서 서술하시오.

---

_— 수고하셨습니다. —_
