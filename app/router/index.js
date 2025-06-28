import { createRouter, createWebHistory } from 'vue-router'

import TeamDashboard from '@/views/TeamDashboard.vue'
import IndexView from '@/views/IndexView.vue'

import { useAppStore } from '@/stores/app'

const router = createRouter({
  history: createWebHistory('/app'),
  routes: [
    {
      path: '/',
      name: 'index',
      component: IndexView,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/health',
      name: 'health',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('@/views/HealthView.vue'),
    },
    {
      path: '/team/:teamId',
      component: TeamDashboard,
      meta: {
        requiresAuth: true,
      },
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/views/team/HomeView.vue'),
        },
        {
          path: 'issues',
          name: 'issues',
          component: () => import('@/views/team/IssuesView.vue'),
        },
      ],
    },
  ],
})

router.beforeEach((to, from, next) => {
  const appStore = useAppStore()
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // this route requires auth, check if logged in
    if (!appStore.isLoggedIn) {
      // not logged in, redirect to login page.
      window.location.href = '/accounts/login/?redirect=' + encodeURIComponent(to.fullPath)
    } else {
      // logged in, proceed to route
      next()
    }
  } else {
    // does not require auth, proceed to route
    next()
  }
})

export default router
