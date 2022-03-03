<script setup>
import { ref } from 'vue'
import IFrame from '@/components/IFrame.vue'

import Menubar from 'primevue/menubar'

const items = ref([
  { label: 'Dashboard',
    icon: 'pi pi-chart-pie',
    id: 'metabase',
    items: [
      { label: 'Dashboard one', id: '9a5351a9-c0c8-4f26-8d96-7b007949f7cc', command: () => { activeIndex.value = 0; activeChildIndex.value = 0 } }
    ],
  },
  { label: 'Apps', icon: 'pi pi-box', id: 'apps', command: () => { activeIndex.value = 1 } },
  { label: 'Spacy Demo', icon: 'pi pi-eye', id: 'spacy_app', command: () => { activeIndex.value = 2 } },
  { label: 'Data Pipeline', icon: 'pi pi-sync', id: 'dagit', command: () => { activeIndex.value = 3 } },
  { label: 'MLOps', icon: 'pi pi-tags', id: 'rubrix', command: () => { activeIndex.value = 4 } }
])

const activeIndex = ref(0)
const activeChildIndex = ref(0)

</script>

<template>
  <Menubar :model="items" v-model:activeIndex="activeIndex">
    <template #start>
      <img alt="Vue logo" src="@/assets/logo.svg" width="30" class="mr-10"/>
    </template>
    <template #end>
      <a href="/metabase" target="_blank"><i class="pi pi-cog" style="font-size: 1.25rem"></i></a>
    </template>
  </Menubar>  
  
  <IFrame v-model:service="items[activeIndex]" v-model:dashboard="activeChildIndex" ></IFrame>
</template>
