<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';
import { useUserStore } from '../stores/user_store';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';

const userStore = useUserStore();
const {
    username,
    is_authenticated
} = storeToRefs(userStore)

const router = useRouter();

const formUsername = ref();
const formPassword = ref();

async function onLoginFormSubmit() {
    const r = await axios.post("/api/users/login/", {
        username: formUsername.value,
        password: formPassword.value
    });

    formPassword.value = '';
    formUsername.value = '';

    userStore.fetchUser();

    router.push('/tournaments')
}
</script>

<template>
    <div class="container" style="display: flex; justify-content: center; align-items: center;">
        <form @submit.prevent.stop="onLoginFormSubmit" class="form d-flex flex-column" style="gap: 8px; padding: 3px">
            <div>
                <label class="form-label">Имя пользователя</label>
                <input placeholder="Имя пользователя" type="formUsername" class="form-control" v-model="formUsername" />
                <label class="form-label">Пароль</label>
                <input placeholder="Пароль" type="formPassword" class="form-control" v-model="formPassword" />
            </div>

            <div style="display: flex; justify-content: center; align-items: center;">
                <button type="submit" class="btn btn-primary">Войти</button>
            </div>
        </form>
    </div>
</template>