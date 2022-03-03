<script setup>
import { ref } from 'vue'
import IFrame from '@/components/IFrame.vue'

import Menubar from 'primevue/menubar'

const items = ref([
  { label: 'Dashboard',
    icon: 'pi pi-chart-pie',
    id: 'dashboard',
    items: [
      { label: 'Dashboard one', id: '2343643643139', command: () => { activeIndex.value = 0; activeChildIndex.value = 0 } }
    ],
  },
  { label: 'Dashboard builder', icon: 'pi pi-cog', id: 'metadata', command: () => { activeIndex.value = 1 } },
  { label: 'Apps', icon: 'pi pi-box', id: 'apps', command: () => { activeIndex.value = 2 } },
  { label: 'Spacy Demo', icon: 'pi pi-eye', id: 'spacy_app', command: () => { activeIndex.value = 3 } },
  { label: 'Data Pipeline', icon: 'pi pi-sync', id: 'dagit', command: () => { activeIndex.value = 4 } },
  { label: 'MLOps', icon: 'pi pi-tags', id: 'rubrix', command: () => { activeIndex.value = 5 } }
])

const activeIndex = ref(0)
const activeChildIndex = ref(0)

</script>

<template>
  <Menubar :model="items" v-model:activeIndex="activeIndex">
    <template #start>
      <img alt="Vue logo" src="@/assets/logo.svg" width="30" class="mr-10"/>
    </template>
  </Menubar>  
  
  <IFrame v-model:service="items[activeIndex]" v-model:dashboard="activeChildIndex" ></IFrame>
</template>
