import { createRouter, createWebHistory } from 'vue-router';
import TournamentsView from '@/views/TournamentsView.vue';
import TeamsView from '@/views/TeamsView.vue';
import PlayersView from '@/views/PlayersView.vue';
import TeamParticipationsView from '@/views/TeamParticipationsView.vue';
import MatchesView from '@/views/MatchesView.vue';
import LoginView from '@/views/LoginView.vue';
import { useUserStore } from '../stores/user_store';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      redirect: "/tournaments"
    },
    {
      path: "/tournaments",
      name: "TournamentsView",
      component: TournamentsView
    },
    {
      path: "/teams",
      name: "TeamsView",
      component: TeamsView
    },
    {
      path: "/players",
      name: "PlayersView",
      component: PlayersView
    },
    {
      path: "/teamparticipations",
      name: "TeamParticipationsView",
      component: TeamParticipationsView
    },
    {
      path: "/matches",
      name: "MatchesView",
      component: MatchesView
    },
    {
      path: "/login",
      name: "LoginView",
      component: LoginView
    }
  ],
})

router.beforeEach(async (to, from) => {
  const userStore = useUserStore();
  await userStore.fetchUser();

  if (!userStore.is_authenticated && to.name != 'LoginView') {
    return { name: 'LoginView' }
  }

  if (userStore.is_authenticated && to.name == 'LoginView') {
    return { name: 'TournamentsView' }
  }
})

export default router
