<script setup>
import { ref } from 'vue'
import IFrame from '@/components/IFrame.vue'

import Markdown from 'vue3-markdown-it'

// Markdown File
import home from './home.md?raw'
import home2 from './home2.md?raw'
import home3 from '../../README.md?raw'

//PRIMEVUE COMPONENTS
import Menubar from 'primevue/menubar'

const items = ref([
  {
    label: 'Home',
    icon: 'pi pi-home',
    id: 'home',
    command: () => {
      activeIndex.value = 0
    },
  },
  {
    label: 'Dashboard',
    icon: 'pi pi-chart-pie',
    id: 'metabase',
    items: [
      {
        label: 'Posts',
        id: '46070920-be02-4948-814b-bca59cddc17a',
        command: () => {
          activeIndex.value = 1
          activeChildIndex.value = 0
        },
      },
      {
        label: 'Comments',
        id: '5143530b-5313-4f40-91e4-eb7868a44782',
        command: () => {
          activeIndex.value = 1
          activeChildIndex.value = 1
        },
      },
      {
        label: 'Model Performances',
        id: '408b49c6-0622-4c4a-af6b-0ce372061de4',
        command: () => {
          activeIndex.value = 1
          activeChildIndex.value = 2
        },
      },
      {
        label: 'Subreddit Classif.',
        id: 'b8cc283b-d364-4d7f-a173-9ddf0fa5fdb0',
        command: () => {
          activeIndex.value = 1
          activeChildIndex.value = 3
        },
      },
    ],
  },
  {
    label: 'Apps',
    icon: 'pi pi-box',
    id: 'apps',
    command: () => {
      activeIndex.value = 2
    },
  },
  {
    label: 'Spacy Demo',
    icon: 'pi pi-eye',
    id: 'spacy_app',
    command: () => {
      activeIndex.value = 3
    },
  },
  {
    label: 'Data Pipeline',
    icon: 'pi pi-sync',
    id: 'dagit',
    command: () => {
      activeIndex.value = 4
    },
  },
  {
    label: 'MLOps',
    icon: 'pi pi-tags',
    id: 'rubrix',
    command: () => {
      activeIndex.value = 5
    },
  },
  {
    icon: 'pi pi-cog',
    id: 'settings',
    items: [
      {
        label: 'Data Pipeline',
        icon: 'pi pi-sync',
        id: 'dagit',
        command: () => {
          activeIndex.value = 4
        },
      },
      {
        separator: true,
      },
      {
        label: 'Metabase',
        icon: 'pi pi-chart-pie',
        id: 'metabase',
        to: '/metabase',
      },
    ],
  },
])

const activeIndex = ref(0)
const activeChildIndex = ref(0)

// Markdown file to parse
const source = home
const source2 = home2
const source3 = home3
</script>

<template>
  <!-- MENU -->
  <Menubar :model="items" v-model:activeIndex="activeIndex">
    <template #start>
      <img
        alt="Palo DevOps"
        src="@/assets/palo_infinity.png"
        width="50"
        class="mr-10"
      />
    </template>
    <template #end>
      <a href="https://github.com/ycouble/myreddit" target="_blank">
        <i class="pi pi-github font-bold mr-5" style="font-size: 1.25rem"></i>
      </a>
      <a href="https://palo-it.com" target="_blank">
        <i
          class="pi pi-globe text-green-600 mr-5"
          style="font-size: 1.25rem"
        ></i>
      </a>
    </template>
  </Menubar>

  <!-- HOME -->
  <div v-if="activeIndex === 0">
    <div class="container mx-auto mt-10 text-left">
      <div
        class="flex mx-10 justify-around flex-wrap 2xl:space-x-20 space-y-20 sm:space-y-0"
      >
        <div class="prose lg:w-1/3">
          <Markdown :source="source"></Markdown>
        </div>
        <div class="prose lg:w-2/3">
          <Markdown :source="source2"></Markdown>
        </div>
        <div class="prose">
          <Markdown :source="source3"></Markdown>
        </div>
      </div>
    </div>
  </div>
  <!-- IFRAME -->
  <IFrame
    v-else
    v-model:service="items[activeIndex]"
    v-model:dashboard="activeChildIndex"
  ></IFrame>
</template>
