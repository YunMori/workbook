# JS 비동기(Asynchronous) 모의고사 (Version 2) — 정답 및 해설

## 빠른 정답표 (객관식)

| 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10  | 11  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ②   | ④   | ②   | ②   | ②   | ③   | ③   | ②   | ②   | ①   | ②   |

| 12  | 13  | 14  | 15  | 16  | 17  | 18  | 19  | 20  | 21  | 22  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ③   | ②   | ③   | ③   | ②   | ②   | ②   | ②   | ②   | ②   | ②   |

| 23  | 24  | 25  | 26  | 27  | 28  | 29  | 30  | 31  | 32  | 33  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ①   | ③   | ②   | ①   | ②   | ②   | ②   | ②   | ①   | ①   | ②   |

| 34  | 35  | 36  | 37  | 38  | 39  | 40  |
| --- | --- | --- | --- | --- | --- | --- |
| ④   | ②   | ②   | ②   | ①   | ③   | ②   |

**정답 분포**: ① 6개 · ② 25개 · ③ 7개 · ④ 2개

---

## 객관식 해설

**1. 정답 ②** — 객체는 "키로 구분된 데이터 집합을 저장하는 자료형(data collection)"으로 정의된다. (2_js_javaScript_asynchronousjs §1)

**2. 정답 ④** — 객체의 key는 문자형만 허용되며, value는 함수를 포함한 모든 자료형이 가능하다. (2_js_javaScript_asynchronousjs §2)

**3. 정답 ②** — `in` 연산자는 해당 속성이 객체에 존재하는지 확인하며, `greeting` 속성이 없으므로 `false`를 반환한다. (2_js_javaScript_asynchronousjs §3)

**4. 정답 ②** — 객체 속성에 정의된 함수를 메서드라 하며, `object.method()` 형태로 호출한다. (2_js_javaScript_asynchronousjs §4)

**5. 정답 ②** — this는 함수나 메서드를 호출한 객체를 가리키며, 함수 내에서 객체의 속성 및 메서드에 접근하기 위해 사용된다. (2_js_javaScript_asynchronousjs §5)

**6. 정답 ③** — 단순 호출 시 this는 전역 객체(window)를 가리킨다. (2_js_javaScript_asynchronousjs §6)

**7. 정답 ③** — 메서드 호출 시 this는 메서드를 호출한 객체(myObj)를 가리킨다. (2_js_javaScript_asynchronousjs §7)

**8. 정답 ②** — 화살표 함수는 자신만의 this를 갖지 않고 외부 함수의 this 값을 그대로 사용하므로, 중첩 함수에서의 this 문제를 해결할 수 있다. (2_js_javaScript_asynchronousjs §8)

**9. 정답 ②** — JS의 this는 함수 호출 방식에 따라 동적으로 할당된다는 점이 강조되었다. (2_js_javaScript_asynchronousjs §9)

**10. 정답 ①** — this가 동적으로 결정되는 덕분에 함수(메서드)를 하나만 만들어 여러 객체에서 재사용할 수 있다. (2_js_javaScript_asynchronousjs §10)

**11. 정답 ②** — 키 이름과 값 변수 이름이 같으면 `{ name, age }`처럼 단축 구문을 사용할 수 있다. (2_js_javaScript_asynchronousjs §11)

**12. 정답 ③** — 단축 메서드는 객체 리터럴 안에서 `function` 키워드를 생략하고 `myFunc() { ... }` 형태로 작성할 수 있다. (2_js_javaScript_asynchronousjs §12)

**13. 정답 ②** — 계산된 속성은 `[변수]: 값` 형태로 작성하며, 변수 값을 키로 사용할 수 있게 해준다. (2_js_javaScript_asynchronousjs §13)

**14. 정답 ③** — 함수 매개변수에서 객체의 속성을 바로 변수로 분해해 받는 것은 구조 분해 할당의 활용이다. (2_js_javaScript_asynchronousjs §14)

**15. 정답 ③** — 전개 구문(`...obj`)은 객체를 복사하여 펼치므로, obj의 모든 속성이 newObj에 포함된다. (2_js_javaScript_asynchronousjs §15)

**16. 정답 ②** — `Object.keys()`는 key 목록을, `Object.values()`는 value 목록을 배열로 반환한다. (2_js_javaScript_asynchronousjs §16)

**17. 정답 ②** — JSON은 JavaScript의 Object와 유사한 구조지만 형식이 있는 "문자열"이다. (2_js_javaScript_asynchronousjs §17)

**18. 정답 ②** — 배열은 "순서가 있는 데이터 집합을 저장하는 자료구조"이다. (2_js_javaScript_asynchronousjs §18)

**19. 정답 ②** — `push`는 배열 끝에 요소를 추가하고 `pop`은 배열 끝 요소를 제거한다. (2_js_javaScript_asynchronousjs §19)

**20. 정답 ②** — Array Helper Methods는 인자로 콜백함수를 받아 배열의 각 요소를 순회하며 호출하는 것이 특징이다. (2_js_javaScript_asynchronousjs §20)

**21. 정답 ②** — map은 콜백의 반환 값을 모아 새로운 배열을 반환하지만, forEach는 반환 값이 없다(undefined). (2_js_javaScript_asynchronousjs §21)

**22. 정답 ②** — forEach의 콜백은 `item(요소)`, `index(선택)`, `array(선택)` 3가지 매개변수로 구성된다. (2_js_javaScript_asynchronousjs §22)

**23. 정답 ①** — forEach 콜백은 `(item, index, array)` 순서이며, 배열을 템플릿 리터럴에 넣으면 쉼표로 구분된 문자열로 출력된다. (2_js_javaScript_asynchronousjs §23)

**24. 정답 ③** — for loop와 for...of는 break/continue가 가능하지만, forEach는 콜백 함수 구조상 사용할 수 없으며 사용이 권장된다. (2_js_javaScript_asynchronousjs §24)

**25. 정답 ②** — filter는 콜백 함수의 반환 값이 참인 요소들만 모아서 새로운 배열을 반환한다. (2_js_javaScript_asynchronousjs §25)

**26. 정답 ①** — find는 콜백의 반환 값이 참이면 해당 요소를 반환한다(배열이 아닌 요소 자체). (2_js_javaScript_asynchronousjs §26)

**27. 정답 ②** — every는 모든 요소가 콜백을 통과해야 true를 반환하며, 하나라도 통과하지 못하면 즉시 false를 반환한다. (2_js_javaScript_asynchronousjs §27)

**28. 정답 ②** — some은 요소 중 적어도 하나라도 콜백을 통과하면 즉시 true를 반환한다. (2_js_javaScript_asynchronousjs §28)

**29. 정답 ②** — 배열도 참조 타입의 객체이며, 숫자를 키로 가지고 `length` 속성을 갖는 특수한 객체다. (2_js_javaScript_asynchronousjs §29)

**30. 정답 ②** — 배열의 length 속성은 writable: true, enumerable: false, configurable: false의 속성 기술자를 가진다. (2_js_javaScript_asynchronousjs §30)

**31. 정답 ①** — Synchronous(동기)는 실행 흐름이 순차적으로 진행되며, 하나의 작업이 완료된 후에 다음 작업이 실행되는 방식이다. (2_js_javaScript_asynchronousjs §31)

**32. 정답 ①** — 비동기는 작업의 완료 여부를 신경 쓰지 않고 다음 작업을 동시에 수행할 수 있다는 점이 강조되었다. (2_js_javaScript_asynchronousjs §32)

**33. 정답 ②** — JavaScript는 한 번에 하나의 일만 수행할 수 있는 Single Thread 언어로, 요청한 순서대로 처리할 수밖에 없다. (2_js_javaScript_asynchronousjs §33)

**34. 정답 ④** — 비동기 처리 동작의 4가지 핵심 요소는 Call Stack, Web API, Task Queue(Callback Queue), Event Loop이며, Virtual DOM은 무관한 개념이다. (2_js_javaScript_asynchronousjs §34)

**35. 정답 ②** — Call Stack은 LIFO(후입선출) 구조의 스택이며, JavaScript의 기본적인 Single Thread 작업 처리를 담당한다. (2_js_javaScript_asynchronousjs §35)

**36. 정답 ②** — Web API는 JavaScript 엔진이 아닌 브라우저에서 제공하는 runtime 환경으로, 시간이 소요되는 작업을 처리한다. (2_js_javaScript_asynchronousjs §36)

**37. 정답 ②** — Task Queue는 FIFO 구조로 비동기 처리된 콜백 함수가 대기하며, Event Loop는 Call Stack이 비면 Task Queue의 가장 오래된 작업을 Call Stack으로 보낸다. (2_js_javaScript_asynchronousjs §37)

**38. 정답 ①** — AJAX는 Asynchronous JavaScript and XML의 약자이다. (2_js_javaScript_asynchronousjs §38)

**39. 정답 ③** — AJAX의 'X'는 XML을 의미하지만, 요즘은 더 가벼운 용량과 JS의 일부라는 장점 때문에 JSON을 많이 사용한다. (2_js_javaScript_asynchronousjs §39)

**40. 정답 ②** — XHR은 이름에 XML이 들어가지만 XML뿐 아니라 모든 종류의 데이터를 가져올 수 있다. (2_js_javaScript_asynchronousjs §40)

---

## 주관식 해설

**41.** 대괄호(`[]`) 표기법

- `user['key with space']`처럼 대괄호를 사용해야 공백이 포함된 키에 접근할 수 있다.

**42.** `delete`

- `delete user.name`과 같이 사용하면 해당 속성이 객체에서 제거된다.

**43.** `this`

- this는 함수 내에서 객체의 속성 및 메서드에 접근하기 위해 사용되며, 호출 방식에 따라 가리키는 대상이 달라진다.

**44.** 화살표 함수는 자신만의 this를 갖지 않기 때문에 외부(상위) 함수의 this 값을 그대로 사용한다.

- forEach 콜백을 일반 함수로 쓰면 this가 window를 가리키지만, 화살표 함수로 바꾸면 외부 함수의 this를 그대로 사용한다.

**45.** 계산된 속성(computed property name)

- 키가 대괄호로 둘러싸이며, 고정된 값이 아닌 변수 값을 키로 사용할 수 있게 해준다.

**46.** 구조 분해 할당(destructuring assignment)

- 객체 속성을 변수로 바로 분해해 할당할 수 있으며, 함수 매개변수로도 활용 가능하다.

**47.** 전개 구문(spread syntax)

- 객체 복사(얕은 복사)에 활용되며, `{...obj}` 형태로 사용한다.

**48.** `Object.keys()`

- value만 반환하는 것은 `Object.values()`이다.

**49.** JavaScript Object Notation

- JSON은 Key-Value 형태로 이루어진 자료 표기법으로, JS의 Object와 유사하지만 형식이 있는 "문자열"이다.

**50.** `shift()`

- `unshift`는 배열 앞에 요소를 추가하고, `shift`는 배열 앞 요소를 제거한다.

**51.** `map()`

- map은 콜백함수의 반환값들을 모아 새로운 배열을 반환한다는 점이 forEach와 다르다.

**52.** `[2, 4, 6]`

- map은 각 요소(1,2,3)에 콜백을 적용한 결과(2,4,6)를 모은 새로운 배열을 반환한다.

**53.** `forEach()`

- for loop와 for...of는 break/continue가 가능하지만 forEach는 콜백 함수 구조상 불가능하다.

**54.** `find()`

- find는 콜백의 반환 값이 참이 되는 첫 요소를 반환한다. 배열로 모아 반환하는 filter와 구분된다.

**55.** `length`

- 배열은 인덱스를 키로 가지며 length 속성(writable:true, enumerable:false, configurable:false)을 갖는 특수한 객체이다.

**56.** 동기(Synchronous)

- 슬라이드에서 정의된 그대로의 개념이다.

**57.** Web API

- JavaScript 엔진이 아닌 브라우저에서 제공하는 runtime 환경으로, 오래 걸리는 작업을 Call Stack 대신 처리한다.

**58.** Event Loop

- Call Stack과 Task Queue를 지속적으로 모니터링하는 끊임없이 돌아가는 루프이다.

**59.** LIFO(후입선출)

- Call Stack은 스택(LIFO) 구조이며, Task Queue는 큐(FIFO) 구조라는 점이 대비된다.

**60.** Task Queue(Callback Queue)

- 비동기 처리된 콜백 함수가 대기하는 FIFO 큐이다.

---

## 서술형 채점 기준

**61**

| 배점 | 채점 요소                                                            |
| ---- | --------------------------------------------------------------------- |
| 2점  | 동기: 실행 흐름이 순차적으로 진행되며, 하나의 작업 완료 후 다음 작업 실행 |
| 2점  | 비동기: 작업 완료를 기다리지 않고 다음 작업을 동시에 수행 가능           |

**모범 답안**

> 동기는 프로그램의 실행 흐름이 순차적으로 진행되며, 하나의 작업이 완료된 후에 다음 작업이 실행되는 방식이다. 반면 비동기는 실행 흐름이 순차적이지 않으며, 작업이 완료되기를 기다리지 않고 다음 작업이 실행되는 방식이다. 비동기 처리에서는 작업의 완료 여부를 신경 쓰지 않고 동시에 다른 작업들을 수행할 수 있다는 점이 특징이다.

---

**62**

| 배점 | 채점 요소                                                                          |
| ---- | ----------------------------------------------------------------------------------- |
| 1점  | Single Thread: 한 번에 하나의 작업만 수행 → 기본적으로 동기 처리                    |
| 1점  | Call Stack에 들어온 오래 걸리는 작업을 Web API로 넘겨 처리                          |
| 1점  | Web API 처리 완료 작업은 FIFO 구조인 Task Queue에 순서대로 대기                     |
| 1점  | Event Loop가 Call Stack이 비면 Task Queue의 가장 오래된 작업을 Call Stack으로 전달 |

**모범 답안**

> JavaScript는 한 번에 하나의 작업만 수행하는 Single Thread 언어로 기본적으로 동기적 처리를 진행한다. 오래 걸리는 작업이 Call Stack에 들어오면 이를 브라우저가 제공하는 Web API로 넘겨 별도로 처리하게 한다. Web API에서 처리가 끝난 작업은 곧바로 Call Stack에 들어가지 못하고 FIFO 구조인 Task Queue에 순서대로 쌓인다. Event Loop는 Call Stack과 Task Queue를 계속 모니터링하다가 Call Stack이 비어 있으면 Task Queue에서 가장 오래된 작업을 꺼내 Call Stack으로 보낸다. 이 과정을 통해 브라우저 환경에서 비동기 작업 처리가 가능해진다.

---

**63**

| 배점 | 채점 요소                                                       |
| ---- | ----------------------------------------------------------------- |
| 1.5점 | 단순 호출: this는 전역 객체(window)를 가리킴, 예시 포함           |
| 1.5점 | 메서드 호출: this는 호출한 객체를 가리킴, 예시 포함                |

**모범 답안**

> 단순 호출 시 this는 전역 객체(window)를 가리킨다. 예를 들어 `const myFunc = function () { return this }; myFunc()`를 호출하면 window가 반환된다. 반면 메서드 호출 시 this는 그 메서드를 호출한 객체를 가리킨다. 예를 들어 `myObj.myFunc()`처럼 객체를 통해 호출하면 this는 myObj 자신이 된다. 이처럼 this는 함수가 호출되는 방식에 따라 동적으로 결정된다.

---

**64**

| 배점  | 채점 요소                                                                       |
| ----- | ---------------------------------------------------------------------------------- |
| 1.5점 | 공통점: 각 요소를 순회하며 콜백 호출, item/index/array 매개변수 구조 동일         |
| 1.5점 | 차이점: forEach는 반환 값 없음(undefined), map은 결과를 모은 새 배열 반환         |

**모범 답안**

> forEach와 map은 모두 배열의 각 요소를 순회하며 콜백 함수를 호출하고, 콜백은 item, index, array 세 개의 매개변수를 받을 수 있다는 공통점이 있다. 그러나 forEach는 콜백을 호출할 뿐 반환 값이 없어 결과가 undefined인 반면, map은 콜백 함수 호출 결과들을 모아 새로운 배열을 반환한다는 차이가 있다. 즉 동작 원리는 같지만 새로운 배열 반환 여부에서 갈린다.

---

**65**

| 배점 | 채점 요소                                                                          |
| ---- | ------------------------------------------------------------------------------------ |
| 1.5점 | AJAX 정의: 비동기적으로 서버와 데이터 교환, XHR 사용                                |
| 1.5점 | 기존 방식과 비교: 전체 페이지 새로고침 vs 필요한 부분(JSON 등)만 동적 갱신           |

**모범 답안**

> AJAX(Asynchronous JavaScript and XML)는 브라우저와 서버 간의 데이터를 비동기적으로 교환하는 기술로, XMLHttpRequest를 사용해 동적인 웹 페이지를 구성한다. 기존 방식은 form을 제출하면 서버가 새로운 웹페이지 전체를 응답하여 매번 페이지 새로고침이 발생하고 대역폭 낭비가 컸다. 반면 AJAX 방식은 XHR 객체로 요청을 보내고 서버가 필요한 부분 데이터(JSON 등)만 응답하므로, 페이지 전체를 새로고침하지 않고도 필요한 DOM 일부만 동적으로 갱신할 수 있다.

---

**66**

| 배점 | 채점 요소                                                                     |
| ---- | -------------------------------------------------------------------------------- |
| 2점  | 콜백 지옥: 콜백 안에 콜백이 계속 중첩되어 코드가 피라미드처럼 깊어지는 현상, 예시 포함 |
| 2점  | 해결책: Promise 객체의 등장                                                      |

**모범 답안**

> 콜백 지옥은 비동기 작업을 순차적으로 처리하기 위해 콜백 함수 안에 또 다른 콜백 함수를 계속 중첩해서 작성하면서, 코드 형태가 피라미드처럼 깊어지는 현상을 말하며 "Pyramid of doom"이라고도 불린다. 예를 들어 fetchUserData의 콜백 안에서 fetchUserPosts를 호출하고, 그 콜백 안에서 다시 fetchPostComments를 호출하는 식으로 중첩된다. 이는 코드 가독성을 해치고 유지보수를 어렵게 만드는 문제가 있어, 이를 해결하기 위해 Promise 객체가 등장하게 되었다.

---

**67**

| 배점 | 채점 요소                                                                          |
| ---- | ------------------------------------------------------------------------------------ |
| 2점  | 콜백은 Event Loop가 Call Stack을 완료하기 전까지 절대 호출되지 않음                |
| 2점  | Promise는 then 체이닝을 통해 엄격한 순서로 콜백을 호출함을 보장                     |

**모범 답안**

> 비동기 콜백 함수는 Event Loop가 현재 실행 중인 Call Stack을 완료하기 이전에는 절대 호출되지 않는다. 반면 Promise의 콜백 함수는 Event Queue에 배치되는 엄격한 순서로 호출된다. 또한 비동기 작업이 성공하거나 실패한 이후에 then 메서드를 추가로 붙인 경우에도 호출 순서를 보장하며 동작한다. then을 여러 번 사용해 여러 콜백을 추가할 수 있고, 각 콜백은 주어진 순서대로 하나씩 실행되는데, 이러한 체이닝(Chaining)이 Promise의 가장 뛰어난 장점이다.

---

**68**

| 배점 | 채점 요소                                                                 |
| ---- | ---------------------------------------------------------------------------- |
| 2점  | Axios 정의: HTTP 요청/응답 처리를 위한 JS HTTP 클라이언트 라이브러리, 내부적으로 XHR 사용 |
| 2점  | 특징: Promise 기반 비동기 처리, then/catch 체이닝으로 성공/실패 로직 분리    |

**모범 답안**

> Axios는 클라이언트 및 서버 사이에 HTTP 요청을 만들고 응답을 처리하는 데 사용되는 JavaScript HTTP 클라이언트 라이브러리이다. 내부적으로 브라우저를 위한 XHR 객체를 생성해 동작하지만, 개발자에게는 간편한 API를 제공하며 서버와의 HTTP 요청/응답을 손쉽게 처리하도록 도와준다. 가장 큰 특징은 Promise 기반으로 비동기 요청을 처리한다는 점으로, 이를 통해 `.then()`과 `.catch()` 체이닝으로 성공/실패 로직을 명확히 분리해 작성할 수 있다.

---

**69**

| 배점 | 채점 요소                                                                    |
| ---- | -------------------------------------------------------------------------------- |
| 1.5점 | then: 성공 시 callback 실행, 이전 작업의 성공 결과를 인자로 전달                |
| 1.5점 | catch: then 중 실패 시 callback 실행, 이전 작업의 실패 객체를 인자로 전달       |
| 1점   | 체이닝 가능 이유: axios/then/catch 모두 항상 Promise 객체를 반환하기 때문       |

**모범 답안**

> then(callback)은 요청한 작업이 성공하면 callback을 실행하며, 이때 callback은 이전 작업의 성공 결과를 인자로 전달받는다. catch(callback)은 앞선 then() 중 하나라도 실패하면 callback을 실행하며, 이 경우 남은 then은 중단되고 이전 작업의 실패 객체를 인자로 전달받는다. axios로 처리한 비동기 로직은 항상 Promise 객체를 반환하고, then과 catch 역시 항상 Promise 객체를 반환하기 때문에 `axios({}).then().then().catch()`처럼 계속해서 체이닝을 이어갈 수 있다.

---

**70**

| 배점 | 채점 요소                                                                       |
| ---- | ---------------------------------------------------------------------------------- |
| 2점  | 동기식 처리 시 문제점: 데이터를 모두 불러올 때까지 다른 로직 실행이 차단되어 앱이 멈춘 듯한 경험 |
| 2점  | 비동기 처리 시 장점: 먼저 완료되는 부분부터 화면에 표시 가능 → 긍정적인 UX          |

**모범 답안**

> 아주 큰 데이터를 불러온 뒤 실행되는 로직을 동기식으로 처리한다면, 데이터를 모두 불러올 때까지 다른 로직 실행이 차단되어 사용자는 마치 앱이 멈춘 것과 같은 경험을 하게 된다. 동기식 처리는 특정 로직이 실행되는 동안 다른 로직의 실행을 막기 때문에 앱이 응답하지 않는 듯한 느낌을 주는 것이다. 반면 비동기로 처리하면 먼저 완료되는 부분부터 화면에 보여줄 수 있어 사용자 경험에 긍정적인 영향을 준다. 이런 이유로 많은 웹 기능이 비동기 로직을 사용해 구현된다.

---
