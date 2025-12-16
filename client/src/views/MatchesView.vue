<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios";
import { useUserStore } from '../stores/user_store';
import { storeToRefs } from 'pinia';

const userStore = useUserStore();
const {
    is_staff
} = storeToRefs(userStore)

const matches = ref([]);
const matchToAdd = ref({});
const matchToEdit = ref({});

const tournaments = ref([]);
const teams = ref([]);

const loading = ref(false);

const selectedTournament = ref("")
const selectedRadiant = ref("")
const selectedDire = ref("")
const selectedWinner = ref("")

onBeforeMount(async () => {
    await fetchItems();
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

function filterMatches() {
    let filtered = matches.value;

    if (selectedTournament.value) {
        filtered = filtered.filter(m => m.tournament?.id == selectedTournament.value);
    }

    if (selectedRadiant.value) {
        filtered = filtered.filter(m => m.radiant?.id == selectedRadiant.value);
    }

    if (selectedDire.value) {
        filtered = filtered.filter(m => m.dire?.id == selectedDire.value);
    }

    if (selectedWinner.value) {
        if (selectedWinner.value === "null") {
            filtered = filtered.filter(m => !m.winner);
        } else {
            filtered = filtered.filter(m => m.winner?.id == selectedWinner.value);
        }
    }

    return filtered;
}
</script>

<template>
    <!-- редактирование в модальном окне-->
    <div class="modal fade" id="editMatchModal" tabindex="-1">
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
                                <input type="datetime-local" class="form-control" v-model="matchToEdit.start_date"
                                    required />
                                <label>Дата и время начала</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <select class="form-select" v-model="matchToEdit.winner_id" required>
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
    <form v-if="is_staff" @submit.prevent.stop="onMatchAdd">
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
                    <input type="datetime-local" class="form-control" v-model="matchToAdd.start_date" required />
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

    <!-- фильтрация -->
    <div class="row m-2">
        <h6>Фильтры</h6>
        <div class="row">
            <div class="col-auto">
                <div class="form-floating">
                    <select class="form-select" v-model="selectedTournament">
                        <option value="">Все турниры</option>
                        <option :value="t.id" v-for="t in tournaments">{{ t.name }}</option>
                    </select>
                    <label>Турнир</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <select class="form-select" v-model="selectedRadiant">
                        <option value="">Любые силы света</option>
                        <option :value="team.id" v-for="team in teams">{{ team.name }}</option>
                    </select>
                    <label>Силы света</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <select class="form-select" v-model="selectedDire">
                        <option value="">Любые силы тьмы</option>
                        <option :value="team.id" v-for="team in teams">{{ team.name }}</option>
                    </select>
                    <label>Силы тьмы</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <select class="form-select" v-model="selectedWinner">
                        <option value="">Любой победитель</option>
                        <option value="null">Не определён</option>
                        <option :value="team.id" v-for="team in teams">{{ team.name }}</option>
                    </select>
                    <label>Победитель</label>
                </div>
            </div>
        </div>
    </div>

    <!-- вывод и кнопки -->
    <div v-if="filterMatches().length == 0 && !loading" style="text-align: center; margin: 1rem;">
        <h4>Матчей не найдено</h4>
    </div>
    <div v-else-if="filterMatches().length == 0 && loading" style="text-align: center; margin: 1rem;">
        <h4>Загрузка матчей...</h4>
    </div>
    <div v-for="m in filterMatches()" class="output-item">
        <div>
            <div>{{ m.tournament?.name }}</div>
            <div><b>Силы света: </b>{{ m.radiant?.name }}</div>
            <div><b>Силы тьмы: </b>{{ m.dire?.name }}</div>
            <div>{{ m.start_date }}</div>
            <div><b>Победитель: </b>{{ m.winner?.name || "Не определён" }}</div>
        </div>
        <div>
            <button v-if="is_staff" class="btn btn-success" @click="onMatchEditClick(m)" data-bs-toggle="modal"
                data-bs-target="#editMatchModal">
                Редактировать
            </button>
        </div>
        <div>
            <button v-if="is_staff" class="btn btn-danger" @click="onRemoveClickMatch(m)">
                Удалить
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
