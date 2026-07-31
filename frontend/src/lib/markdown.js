import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js/lib/core'
import javascript from 'highlight.js/lib/languages/javascript'
import xml from 'highlight.js/lib/languages/xml'
import css from 'highlight.js/lib/languages/css'
import json from 'highlight.js/lib/languages/json'
import bash from 'highlight.js/lib/languages/bash'

hljs.registerLanguage('javascript', javascript)
hljs.registerLanguage('js', javascript)
hljs.registerLanguage('html', xml)
hljs.registerLanguage('xml', xml)
hljs.registerLanguage('vue', xml)
hljs.registerLanguage('css', css)
hljs.registerLanguage('json', json)
hljs.registerLanguage('bash', bash)

// html:false — 문항 지문의 <button>, <div> 같은 예시 태그가 실제 DOM으로
// 렌더링되지 않고 글자 그대로 보이게 한다. 원시 HTML 주입도 함께 막힌다.
const md = new MarkdownIt({
  html: false,
  linkify: false,
  breaks: true,
  highlight(code, language) {
    if (language && hljs.getLanguage(language)) {
      try {
        return hljs.highlight(code, { language, ignoreIllegals: true }).value
      } catch {
        /* 강조 실패 시 평문으로 */
      }
    }
    return md.utils.escapeHtml(code)
  },
})

export function renderMarkdown(text) {
  return md.render(text || '')
}

export function renderInline(text) {
  return md.renderInline(text || '')
}
