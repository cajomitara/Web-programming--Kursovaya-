import { defineStore } from "pinia";
import { ref, onBeforeMount } from "vue";
import axios from "axios";
import Cookies from 'js-cookie';

export const useUserStore = defineStore("userStore", () => {
    const username = ref();
    const is_authenticated = ref(false);
    const is_staff = ref(false);

    async function fetchUser() {
        const r = await axios.get("/api/users/my/");

        username.value = r.data.username
        is_authenticated.value = r.data.is_authenticated
        is_staff.value = r.data.is_staff

        console.log(r.data);

        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
    }

    onBeforeMount(async () => {
        fetchUser();
    })

    return {
        username,
        is_authenticated,
        is_staff,
        fetchUser
    }
});