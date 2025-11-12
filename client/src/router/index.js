import { createRouter, createWebHistory } from 'vue-router';
import TournamentsView from '@/views/TournamentsView.vue';
import TeamsView from '@/views/TeamsView.vue';
import PlayersView from '@/views/PlayersView.vue';
import TeamParticipationsView from '@/views/TeamParticipationsView.vue';
import MatchesView from '@/views/MatchesView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/tournaments",
      name: "TournamentsView.vue",
      component: TournamentsView
    },
    {
      path: "/teams",
      name: "TeamsView.vue",
      component: TeamsView
    },
    {
      path: "/players",
      name: "PlayersView.vue",
      component: PlayersView
    },
    {
      path: "/teamparticipations",
      name: "TeamParticipationsView.vue",
      component: TeamParticipationsView
    },
    {
      path: "/matches",
      name: "MatchesView.vue",
      component: MatchesView
    }
  ],
})

export default router
