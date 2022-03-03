<script setup>
import { computed } from 'vue'
/**
 * INITIALIZATION
 */

const props = defineProps({
  service: Object,
  dashboard: Number
})

const dashboardUrl = computed( () => {
  if (!props.service.items) return ''
  return ('/' + props.service.items[props.dashboard].id)
})

const serviceUrl = computed( () => 'http://' + props.service.id + '.' + import.meta.env.VITE_DOMAIN + dashboardUrl.value)

</script>

<template>
  <iframe
    :id="service.id"
    :title="service.label"
    width="100%"
    height="100%"
    frameborder="0"
    :src="serviceUrl"
  >
  Your browser does not support iframes<a href="{{ serviceUrl }}"> click here to view the page directly.</a>
  </iframe>
</template>

<style lang="scss" scoped>

</style>