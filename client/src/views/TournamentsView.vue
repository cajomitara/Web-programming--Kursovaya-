<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

const tournaments = ref([]);
const tournamentToAdd = ref({});
const tournamentToEdit = ref({});

const loading = ref(false);

onBeforeMount(async () => {
    await fetchTournaments();
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

async function fetchTournaments() {
    loading.value = true;
    const r = await axios.get("/api/tournaments/");
    console.log(r.data);
    tournaments.value = r.data;
    loading.value = false;
}

async function onLoadCLickTournaments() {
    await fetchTournaments();
}

async function onTournamentAdd() {
    await axios.post("/api/tournaments/", {
        ...tournamentToAdd.value,
    });
    await fetchTournaments();
    tournamentToAdd.value = {};
}

async function onRemoveClickTournament(tournament) {
    await axios.delete(`/api/tournaments/${tournament.id}/`);
    await fetchTournaments();
}

async function onUpdateTournament() {
    await axios.put(`/api/tournaments/${tournamentToEdit.value.id}/`, {
        ...tournamentToEdit.value,
    });
    await fetchTournaments();
}

async function onTournamentEditClick(tournament) {
    tournamentToEdit.value = { ...tournament };
}

</script>

<template>
    <!-- редактирование в модальном окне-->
    <div class="modal" id="editTournamentModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">
                        Редактирование
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="col-auto m-1">
                        <div class="col">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="tournamentToEdit.name" />
                                <label for="floatingInput">Название</label>
                            </div>
                        </div>
                    </div>
                    <div class="col-auto m-1">
                        <div class="form-floating">
                            <input type="date" class="form-control" v-model="tournamentToEdit.start_date" />
                            <label for="floatingInput">Дата начала</label>
                        </div>
                    </div>
                    <div class="col-auto m-1">
                        <div class="form-floating">
                            <input type="date" class="form-control" v-model="tournamentToEdit.end_date" />
                            <label for="floatingInput">Дата конца</label>
                        </div>
                    </div>
                    <div class="col-auto m-1">
                        <div class="form-floating">
                            <select class="form-control" v-model="tournamentToEdit.status">
                                <option value="TBA">Неизвестно</option>
                                <option value="Coming">Скоро начнётся</option>
                                <option value="Live">Идёт</option>
                                <option value="Ended">Закончен</option>
                            </select>
                            <label>Статус</label>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Закрыть
                    </button>
                    <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateTournament">
                        Сохранить
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- добавление -->
    <form @submit.prevent.stop="onTournamentAdd">
        <div class="row m-2 ">
            <div class="col">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="tournamentToAdd.name" required/>
                    <label for="floatingInput">Название</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <input type="date" class="form-control" v-model="tournamentToAdd.start_date" />
                    <label for="floatingInput">Дата начала</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <input type="date" class="form-control" v-model="tournamentToAdd.end_date" />
                    <label for="floatingInput">Дата конца</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <select class="form-control" v-model="tournamentToAdd.status" required>
                        <option value="TBA">Неизвестно</option>
                        <option value="Coming">Скоро начнётся</option>
                        <option value="Live">Идёт</option>
                        <option value="Ended">Закончен</option>
                    </select>
                    <label>Статус</label>
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
    <div v-for="t in tournaments" class="output-item">
        <div>
            {{ t.id }} {{ t.name }}  {{ t.start_date }} {{ t.end_date }} {{ t.status }}
        </div>
        <div>
            <button class="btn btn-success" @click="onTournamentEditClick(t)" data-bs-toggle="modal"
                data-bs-target="#editTournamentModal">
                <i class="bi bi-pen-fill">Редактировать</i>
            </button>
        </div>
        <div>
            <button class="btn btn-danger" @click="onRemoveClickTournament(t)">
                <i class="bi bi-x">Удалить</i>
            </button>
        </div>
    </div>

    <div class="row m-2">
        <button class="btn btn-outline-primary" @click="onLoadCLickTournaments">Загрузить турниры</button>
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
