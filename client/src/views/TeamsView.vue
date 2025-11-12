<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

const teams = ref([]);
const teamToAdd = ref({});
const teamToEdit = ref({});

const loading = ref(false);

onBeforeMount(async () => {
    await fetchTeams();
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

async function fetchTeams() {
    loading.value = true;
    const r = await axios.get("/api/teams/");
    console.log(r.data);
    teams.value = r.data;
    loading.value = false;
}

async function onLoadCLickTeams() {
    await fetchTeams();
}

async function onTeamAdd() {
    await axios.post("/api/teams/", {
        ...teamToAdd.value,
    });
    await fetchTeams();
    teamToAdd.value = {};
}

async function onRemoveClickTeam(team) {
    await axios.delete(`/api/teams/${team.id}/`);
    await fetchTeams();
}

async function onUpdateTeam() {
    await axios.put(`/api/teams/${teamToEdit.value.id}/`, {
        ...teamToEdit.value,
    });
    await fetchTeams();
}

async function onTeamEditClick(team) {
    teamToEdit.value = { ...team };
}

</script>

<template>
    <!-- редактирование в модальном окне-->
        <div class="modal" id="editTeamModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">
                        Редактирование команды
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="row mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="teamToEdit.name" />
                                <label>Название</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="teamToEdit.country" />
                                <label>Страна</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Закрыть
                    </button>
                    <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateTeam">
                        Сохранить
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- добавление -->
    <form @submit.prevent.stop="onTeamAdd">
        <div class="row m-2 ">
            <div class="col">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="teamToAdd.name" />
                    <label for="floatingInput">Название</label>
                </div>
            </div>
            <div class="col">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="teamToAdd.country" />
                    <label for="floatingInput">Страна</label>
                </div>
            </div>
            <div class="col-auto">
                <button class="btn btn-primary">
                    Добавить
                </button>
            </div>
        </div>
    </form>

    <!-- вывод и кнопки -->
    <div v-for="t in teams" class="output-item">
        <div>
            {{ t.id }} {{ t.name }} {{ t.country }}
        </div>
        <div>
            <button class="btn btn-success" @click="onTeamEditClick(t)" data-bs-toggle="modal"
                data-bs-target="#editTeamModal">
                <i class="bi bi-pen-fill">Редактировать</i>
            </button>
        </div>
        <div>
            <button class="btn btn-danger" @click="onRemoveClickTeam(t)">
                <i class="bi bi-x">Удалить</i>
            </button>
        </div>
    </div>

    <div class="row m-2">
        <button class="btn btn-outline-primary" @click="onLoadCLickTeams">Загрузить команды</button>
    </div>
</template>

<style scoped>
.output-item {
    padding: 0.5rem;
    margin: 0.5rem;
    border: 2px solid silver;
    border-radius: 10px;
    display: grid;
    grid-template-columns: 1fr auto auto;
    gap: 8px;
    justify-content: center;
}
</style>
