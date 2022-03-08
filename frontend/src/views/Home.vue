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
      { label: 'Posts', id: '46070920-be02-4948-814b-bca59cddc17a', command: () => { activeIndex.value = 1; activeChildIndex.value = 0 } },
      { label: 'Comments', id: '5143530b-5313-4f40-91e4-eb7868a44782', command: () => { activeIndex.value = 1; activeChildIndex.value = 1 } },
      { label: 'Model Performances', id: '408b49c6-0622-4c4a-af6b-0ce372061de4', command: () => { activeIndex.value = 1; activeChildIndex.value = 2 } },
      { label: 'Subreddit Classif.', id: 'b8cc283b-d364-4d7f-a173-9ddf0fa5fdb0', command: () => { activeIndex.value = 1; activeChildIndex.value = 3 } }
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

  <!-- HOME -->
  <div v-if="activeIndex === 0">
    <!-- <h1>WELCOME HOME</h1>

    <a href="https://www.primefaces.org/primevue/#/card">Components</a> -->

    <div class="container mx-auto m-8 flex">
      <Card class="bg-gray-100 m-8 p-4 sm:w-full lg:w-1/3">
        <template #header>
          <!-- <img alt="user header" src="@/assets/palo_infinity.png" style="width:30px"> -->
        </template>
        <template #title>
          PALO IT NLP Demonstrator
        </template>
        <template #content>
          <p class="prose text-left">
          This website is a fully featured demonstrator of a Natural Language Processing (NLP) application:
          from data extraction to end user application, we've covered the whole lifecycle of a NLP application with a modern and open-source NLP data stack. <br>
          <ul>
          <li>The data is extracted from Reddit API, loaded into a <a href="https://cloud.google.com/bigquery">BigQuery</a> DB.</li>
          <li>It is then locally transformed using <a href="https://www.getdbt.com/">DBT</a></li>
          <li>The texts are cleaned and preprocessed using <a href="https://github.com/chartbeat-labs/textacy">textacy</a></li>
          <li>Models are trained using <a href="https://spacy.io">spaCy</a></li>
          <li>Models are served using <a href="https://fastapi.tiangolo.com/">FastAPI</a></li>
          <li>Models are monitored and new unknown data is annotated through <a href="https://www.rubrix.ml/">Rubrix</a></li>
          <li>Model performance and data are monitored through dashboard made with <a href="https://www.metabase.com/">Metabase</a></li>
          <li>End user applications are demonstrated using <a href="https://streamlit.io">Streamlit</a></li>
          </ul>
          </p>
        </template>
        <template #footer>
        </template>
      </Card>

      <Card class="bg-gray-100 m-8 p-4 md:w-full w-2/3">
        <template #header>
          <!-- <img alt="user header" src="@/assets/palo_infinity.png" style="width:30px"> -->
        </template>
        <template #title>
          System Architecture
        </template>
        <template #content>
          <img alt="architecture" src="@/assets/architecture.png">
        </template>
        <template #footer>
        </template>
      </Card>

    </div>

  </div>

  <!-- IFRAME -->
  <IFrame v-else v-model:service="items[activeIndex]" v-model:dashboard="activeChildIndex" ></IFrame>

</template>
