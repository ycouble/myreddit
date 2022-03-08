<script setup>
import { ref } from 'vue'
import IFrame from '@/components/IFrame.vue'

//PRIMEVUE COMPONENTS
import Menubar from 'primevue/menubar'
import Card from 'primevue/card'

const items = ref([
  { label: 'Home', icon: 'pi pi-home', id: 'home', command: () => { activeIndex.value = 0 } },
  { label: 'Dashboard',
    icon: 'pi pi-chart-pie',
    id: 'metabase',
    items: [
<<<<<<< HEAD
      { label: 'Posts', id: '46070920-be02-4948-814b-bca59cddc17a', command: () => { activeIndex.value = 0; activeChildIndex.value = 0 } },
      { label: 'Comments', id: '5143530b-5313-4f40-91e4-eb7868a44782', command: () => { activeIndex.value = 0; activeChildIndex.value = 1 } },
      { label: 'Model Performances', id: '408b49c6-0622-4c4a-af6b-0ce372061de4', command: () => { activeIndex.value = 0; activeChildIndex.value = 2 } },
      { label: 'Subreddit Classif.', id: 'b8cc283b-d364-4d7f-a173-9ddf0fa5fdb0', command: () => { activeIndex.value = 0; activeChildIndex.value = 3 } }
=======
      { label: 'Dashboard one', id: '9a5351a9-c0c8-4f26-8d96-7b007949f7cc', command: () => { activeIndex.value = 1; activeChildIndex.value = 0 } }
>>>>>>> e75bb74 (Change Home to reflect the dictatorship of the author)
    ],
  },
  { label: 'Apps', icon: 'pi pi-box', id: 'apps', command: () => { activeIndex.value = 2 } },
  { label: 'Spacy Demo', icon: 'pi pi-eye', id: 'spacy_app', command: () => { activeIndex.value = 3 } },
  { label: 'Data Pipeline', icon: 'pi pi-sync', id: 'dagit', command: () => { activeIndex.value = 4 } },
  { label: 'MLOps', icon: 'pi pi-tags', id: 'rubrix', command: () => { activeIndex.value = 5 } }
])

const activeIndex = ref(0)
const activeChildIndex = ref(0)

</script>

<template>

  <!-- MENU -->
  <Menubar :model="items" v-model:activeIndex="activeIndex">
    <template #start>
      <img alt="Palo DevOps" src="@/assets/palo_infinity.png" width="50" class="mr-10"/>
    </template>
    <template #end>
      <a href="https://github.com/ycouble/myreddit" target="_blank"><i class="pi pi-github font-bold mr-5" style="font-size: 1.25rem"></i></a>
      <a href="https://palo-it.com" target="_blank"><i class="pi pi-globe text-green-600 mr-5" style="font-size: 1.25rem"></i></a>
      <a href="/metabase" target="_blank"><i class="pi pi-cog" style="font-size: 1.25rem"></i></a>
    </template>
  </Menubar>

<<<<<<< HEAD
  <IFrame v-model:service="items[activeIndex]" v-model:dashboard="activeChildIndex" ></IFrame>
=======
  <!-- HOME -->
  <div v-if="activeIndex === 0">
    <h1>WELCOME HOME</h1>

    <a href="https://www.primefaces.org/primevue/#/card">Components</a>

    <div class="container m-auto">
      <Card class="md:w-1/4 bg-gray-100">
        <template #header>
          <img alt="user header" src="@/assets/palo_infinity.png">
        </template>
        <template #title>
          Advanced Card
        </template>
        <template #content>
          Lorem ipsum dolor sit amet, consectetur adipisicing elit. Inventore sed consequuntur error repudiandae numquam deserunt
          quisquam repellat libero asperiores earum nam nobis, culpa ratione quam perferendis esse, cupiditate neque quas!
        </template>
        <template #footer>
          <Button icon="pi pi-check" label="Save" />
          <Button icon="pi pi-times" label="Cancel" class="p-button-secondary" style="margin-left: .5em" />
        </template>
      </Card>
    </div>

  </div>

  <!-- IFRAME -->
  <IFrame v-else v-model:service="items[activeIndex]" v-model:dashboard="activeChildIndex" ></IFrame>

>>>>>>> e75bb74 (Change Home to reflect the dictatorship of the author)
</template>
