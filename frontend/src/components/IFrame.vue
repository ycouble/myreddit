<script setup>
import { computed } from 'vue'
/**
 * INITIALIZATION
 */

const props = defineProps({
  service: Object,
  dashboard: Number
})


const serviceUrl = computed( () => 'http://' + props.service.id + '.' + import.meta.env.VITE_DOMAIN )
const dashboardUrl = computed( () => 'http://' + import.meta.env.VITE_DOMAIN + '/metabase/public/dashboard/' + props.service.items[props.dashboard].id)

</script>

<template>
  <iframe
    v-if="!service.items"
    :id="service.id"
    :title="service.label"
    allow="fullscreen"
    frameborder="0"
    :src="serviceUrl"
    class="iframe"
  >
  Your browser does not support iframes<a href="{{ serviceUrl }}"> click here to view the page directly.</a>
  </iframe>
  <iframe
    v-else
    :id="service.id"
    :title="service.label"
    allow="fullscreen"
    frameborder="0"
    :src="dashboardUrl"
    class="iframe"
  >
  Your browser does not support iframes<a href="{{ serviceUrl }}"> click here to view the page directly.</a>
  </iframe>
</template>

<style scoped>
.iframe {
  width: 100%;
  min-height: calc(100vh - 6rem)
}
</style>