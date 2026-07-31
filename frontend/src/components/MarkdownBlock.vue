<script setup>
import { computed } from 'vue'

import { renderMarkdown } from '../lib/markdown'

const props = defineProps({
  source: { type: String, default: '' },
})

const html = computed(() => renderMarkdown(props.source))
</script>

<template>
  <!-- markdown-it을 html:false로 실행하므로 원시 HTML은 이스케이프되어 들어온다 -->
  <div class="md" v-html="html"></div>
</template>
