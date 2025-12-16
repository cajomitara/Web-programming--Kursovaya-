<script setup>
import axios from "axios";
import { useUserStore } from './stores/user_store';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';

const userStore = useUserStore();
const {
    username,
    is_authenticated,
    is_staff
} = storeToRefs(userStore)

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
                            <a v-if="is_staff" class="nav-link" aria-current="page" href="/tournaments">Турниры</a>
                            <a v-if="!is_staff" class="nav-link" aria-current="page" href="/tournaments">Мои турниры</a>
                        </li>
                        <li class="nav-item">
                            <a v-if="is_staff" class="nav-link" aria-current="page" href="/teams">Команды</a>
                            <a v-if="!is_staff" class="nav-link" aria-current="page" href="/teams">Моя команда</a>
                        </li>
                        <li class="nav-item">
                            <a v-if="is_staff" class="nav-link" aria-current="page" href="/players">Игроки</a>
                            <a v-if="!is_staff" class="nav-link" aria-current="page" href="/players">Игроки моей команды</a>
                        </li>
                        <li class="nav-item">
                            <a v-if="is_staff" class="nav-link" aria-current="page" href="/teamparticipations">Участия команд в турнирах</a>
                            <a v-if="!is_staff" class="nav-link" aria-current="page" href="/teamparticipations">Участия моей команды в турнирах</a>
                        </li>
                        <li class="nav-item">
                            <a v-if="is_staff" class="nav-link" aria-current="page" href="/matches">Матчи</a>
                            <a v-if="!is_staff" class="nav-link" aria-current="page" href="/matches">Матчи моей команды</a>
                        </li>
                    </ul>

                    <ul class="navbar-nav">
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                {{ username }}
                            </a>
                            <ul class="dropdown-menu">
                                <li>
                                    <a v-if="is_staff" class="dropdown-item" href="/admin">Админка</a>
                                </li>
                                <li>
                                    <a class="dropdown-item" style="cursor: pointer;" @click="onLogout">Выйти</a>
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

<style scoped>

</style>