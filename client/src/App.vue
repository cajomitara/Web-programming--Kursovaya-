<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';
import { useUserStore } from './stores/user_store';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';

const userStore = useUserStore();
const {
    username,
    is_authenticated
} = storeToRefs(userStore)

// const user = ref([])
// const username = ref();

const router = useRouter();

async function onLogout() {
    const r = await axios.post("/api/users/logout/");
    userStore.fetchUser();
    router.go(0);
}
</script>

<template>
    <div v-if="is_authenticated" class="container">
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
            <div class="container-fluid">
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                    aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse justify-content-between" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link" aria-current="page" href="/tournaments">Турниры</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/teams">Команды</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/players">Игроки</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/teamparticipations">Участия команд в турнирах</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/matches">Матчи</a>
                        </li>
                    </ul>

                    <ul class="navbar-nav">
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                                aria-expanded="false">
                                {{ username }}
                            </a>
                            <ul class="dropdown-menu">
                                <li>
                                    <a class="dropdown-item" href="/admin">Админка</a>
                                </li>
                                <li>
                                    <a class="dropdown-item" @click="onLogout">Выйти</a>
                                </li>
                            </ul>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </div>

    <div class="container">
        <router-view />
    </div>
</template>

<style scoped></style>