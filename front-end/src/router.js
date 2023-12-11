import Vue from 'vue'
import Router from 'vue-router'
import ExecutePage from './components/ExecutePage.vue'
import RecordPage from './components/RecordPage.vue'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'executePage',
      component: ExecutePage
    },
    {
      path: '/record',
      name: 'recordPage',
      component: RecordPage
    }
  ]
})