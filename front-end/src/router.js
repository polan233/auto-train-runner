import Vue from 'vue'
import Router from 'vue-router'
import PresetPage from './components/PresetPage.vue'
import RecordPage from './components/RecordPage.vue'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'presetPage',
      component: PresetPage
    },
    {
      path: '/record',
      name: 'recordPage',
      component: RecordPage
    }
  ]
})