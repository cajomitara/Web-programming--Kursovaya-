<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

const matches = ref([]);
const matchToAdd = ref({});
const matchToEdit = ref({});

const tournaments = ref([]);
const teams = ref([]);

const loading = ref(false);

onBeforeMount(async () => {
    await fetchItems();
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

async function fetchItems() {
    loading.value = true;
    const r = await axios.get("/api/matches/");
    console.log(r.data);
    matches.value = r.data;

    const r1 = await axios.get("/api/tournaments/");
    console.log(r1.data);
    tournaments.value = r1.data;

    const r2 = await axios.get("/api/teams/");
    console.log(r2.data);
    teams.value = r2.data;

    loading.value = false;
}

async function onLoadCLickMatches() {
    await fetchItems();
}

async function onMatchAdd() {
    await axios.post("/api/matches/", {
        ...matchToAdd.value,
    });
    await fetchItems();
    matchToAdd.value = {};
}

async function onRemoveClickMatch(match) {
    await axios.delete(`/api/matches/${match.id}/`);
    await fetchItems();
}

async function onUpdateMatch() {
    await axios.put(`/api/matches/${matchToEdit.value.id}/`, {
        ...matchToEdit.value,
    });
    await fetchItems();
}

async function onMatchEditClick(match) {
    matchToEdit.value = {
        ...match,
        tournament_id: match.tournament?.id,
        radiant_id: match.radiant?.id,
        dire_id: match.dire?.id,
        winner_id: match.winner?.id
    };
}

</script>

<template>
    <!-- редактирование в модальном окне-->
    <div class="modal" id="editMatchModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">
                        Редактирование
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="row mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <select class="form-select" v-model="matchToEdit.tournament_id" required>
                                    <option :value="t.id" v-for="t in tournaments">{{ t.name }}</option>
                                </select>
                                <label>Турнир</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <select class="form-select" v-model="matchToEdit.radiant_id" required>
                                    <option :value="team.id" v-for="team in teams">{{ team.name }}</option>
                                </select>
                                <label>Силы Света</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <select class="form-select" v-model="matchToEdit.dire_id" required>
                                    <option :value="team.id" v-for="team in teams">{{ team.name }}</option>
                                </select>
                                <label>Силы Тьмы</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <input type="datetime-local" class="form-control" v-model="matchToEdit.start_date" />
                                <label>Дата и время начала</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <select class="form-select" v-model="matchToEdit.winner_id">
                                    <option :value="null">Не определен</option>
                                    <option :value="team.id" v-for="team in teams">{{ team.name }}</option>
                                </select>
                                <label>Победитель</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Закрыть
                    </button>
                    <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateMatch">
                        Сохранить
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- добавление -->
    <form @submit.prevent.stop="onMatchAdd">
        <div class="row m-1">
            <div class="col-2">
                <div class="form-floating">
                    <select class="form-select" v-model="matchToAdd.tournament_id" required>
                        <option :value="t.id" v-for="t in tournaments">{{ t.name }}</option>
                    </select>
                    <label>Турнир</label>
                </div>
            </div>
            <div class="col-2">
                <div class="form-floating">
                    <select class="form-select" v-model="matchToAdd.radiant_id" required>
                        <option :value="team.id" v-for="team in teams">{{ team.name }}</option>
                    </select>
                    <label>Силы Света</label>
                </div>
            </div>
            <div class="col-2">
                <div class="form-floating">
                    <select class="form-select" v-model="matchToAdd.dire_id" required>
                        <option :value="team.id" v-for="team in teams">{{ team.name }}</option>
                    </select>
                    <label>Силы Тьмы</label>
                </div>
            </div>
            <div class="col-3">
                <div class="form-floating">
                    <input type="datetime-local" class="form-control" v-model="matchToAdd.start_date" required/>
                    <label>Дата и время начала</label>
                </div>
            </div>
            <div class="col-2">
                <div class="form-floating">
                    <select class="form-select" v-model="matchToAdd.winner_id">
                        <option :value="null">Не определён</option>
                        <option :value="team.id" v-for="team in teams">{{ team.name }}</option>
                    </select>
                    <label>Победитель</label>
                </div>
            </div>
            <div class="col-1">
                <button class="btn btn-primary">
                    Добавить
                </button>
            </div>
        </div>
    </form>


    <!-- вывод и кнопки -->
    <div v-for="m in matches" class="output-item">
        <div>
            {{ m.tournament?.name }} {{ m.radiant?.name }} {{ m.dire?.name }} {{ m.start_date }} {{ m.winner?.name ||
            "Не определён" }}
        </div>
        <div>
            <button class="btn btn-success" @click="onMatchEditClick(m)" data-bs-toggle="modal"
                data-bs-target="#editMatchModal">
                <i class="bi bi-pen-fill">Редактировать</i>
            </button>
        </div>
        <div>
            <button class="btn btn-danger" @click="onRemoveClickMatch(m)">
                <i class="bi bi-x">Удалить</i>
            </button>
        </div>
    </div>

    <div class="row m-2">
        <button class="btn btn-outline-primary" @click="onLoadCLickMatches">Загрузить матчи</button>
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
