<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';
import { useUserStore } from '../stores/user_store';
import { storeToRefs } from 'pinia';

const userStore = useUserStore();
const {
    is_staff
} = storeToRefs(userStore)

const team_parts = ref([]);
const team_partToAdd = ref({});
const team_partToEdit = ref({});

const tournaments = ref([]);
const teams = ref([]);

const loading = ref(false);

const selectedTournament = ref("")
const selectedTeam = ref("")

onBeforeMount(async () => {
    await fetchItems();
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

async function fetchItems() {
    loading.value = true;
    const r = await axios.get("/api/tournamentsteamsparticipations/");
    console.log(r.data);
    team_parts.value = r.data;

    const r1 = await axios.get("/api/tournaments/");
    console.log(r1.data);
    tournaments.value = r1.data;

    const r2 = await axios.get("/api/teams/");
    console.log(r2.data);
    teams.value = r2.data;
    loading.value = false;
}

async function onLoadCLickTeamParts() {
    await fetchItems();
}

async function onTeamPartsAdd() {
    await axios.post("/api/tournamentsteamsparticipations/", {
        ...team_partToAdd.value,
    });
    await fetchItems();
    team_partToAdd.value = {};
}

async function onRemoveClickTeamParts(team_part) {
    await axios.delete(`/api/tournamentsteamsparticipations/${team_part.id}/`);
    await fetchItems();
}

async function onUpdateTeamParts() {
    await axios.put(`/api/tournamentsteamsparticipations/${team_partToEdit.value.id}/`, {
        ...team_partToEdit.value,
    });
    await fetchItems();
}

async function onTeamPartEditClick(team_part) {
    team_partToEdit.value = {
        ...team_part,
        tournament_id: team_part.tournament?.id,
        team_id: team_part.team?.id
    };
}

function filterTeamParts() {
    let filtered = team_parts.value;

    if (selectedTournament.value) {
        filtered = filtered.filter(tp => tp.tournament?.id == selectedTournament.value);
    }

    if (selectedTeam.value) {
        filtered = filtered.filter(tp => tp.team?.id == selectedTeam.value);
    }

    return filtered;
}
</script>

<template>
    <!-- редактирование в модальном окне-->
    <div class="modal fade" id="editTeamPartModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">
                        Редактирование
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">

                    <div class="col-auto mb-2">
                        <div class="form-floating">
                            <select class="form-select" v-model="team_partToEdit.tournament_id" required>
                                <option :value="to.id" v-for="to in tournaments">{{ to.name }}</option>
                            </select>
                            <label>Турнир</label>
                        </div>
                    </div>
                    <div class="col-auto mb-2">
                        <div class="form-floating">
                            <select class="form-select" v-model="team_partToEdit.team_id" required>
                                <option :value="te.id" v-for="te in teams">{{ te.name }}</option>
                            </select>
                            <label>Команда</label>
                        </div>
                    </div>
                    <div class="col-auto mb-2">
                        <div class="form-floating">
                            <input type="number" class="form-control" v-model="team_partToEdit.place" />
                            <label>Занятое место</label>
                        </div>
                    </div>

                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Закрыть
                    </button>
                    <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateTeamParts">
                        Сохранить
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- добавление -->
    <form v-if='is_staff' @submit.prevent.stop="onTeamPartsAdd">
        <div class="row m-2 ">
            <div class="col-3">
                <div class="form-floating">
                    <select class="form-select" v-model="team_partToAdd.tournament_id" required>
                        <option :value="to.id" v-for="to in tournaments">{{ to.name }}</option>
                    </select>
                    <label for="floatingInput">Турнир</label>
                </div>
            </div>
            <div class="col-3">
                <div class="form-floating">
                    <select class="form-select" v-model="team_partToAdd.team_id" required>
                        <option :value="te.id" v-for="te in teams">{{ te.name }}</option>
                    </select>
                    <label for="floatingInput">Команда</label>
                </div>
            </div>
            <div class="col">
                <div class="form-floating">
                    <input type="number" class="form-control" v-model="team_partToAdd.place" />
                    <label for="floatingInput">Занятое место</label>
                </div>
            </div>

            <div class="col-auto">
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
                        <option :value="to.id" v-for="to in tournaments">{{ to.name }}</option>
                    </select>
                    <label>Турнир</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <select class="form-select" v-model="selectedTeam">
                        <option value="">Все команды</option>
                        <option :value="te.id" v-for="te in teams">{{ te.name }}</option>
                    </select>
                    <label>Команда</label>
                </div>
            </div>
        </div>
    </div>

    <!-- вывод и кнопки -->
    <div v-if="filterTeamParts().length == 0 && !loading" style="text-align: center;">
        <h4>Участий команд в турнирах не найдено</h4>
    </div>
    <div v-else-if="filterTeamParts().length == 0 && loading" style="text-align: center; margin: 1rem;">
        <h4>Загрузка участий команд в турнирах...</h4>
    </div>
    <div v-for="tp in filterTeamParts()" class="output-item">
        <div>
            <div>{{ tp.tournament?.name }}</div>
            <div v-if="is_staff">{{ tp.team?.name }}</div>
            <div><b>Место: </b>{{ tp.place }}</div>
        </div>
        <div>
            <button v-if="is_staff" class="btn btn-success" @click="onTeamPartEditClick(tp)" data-bs-toggle="modal"
                data-bs-target="#editTeamPartModal">
                Редактировать
            </button>
        </div>
        <div>
            <button v-if="is_staff" class="btn btn-danger" @click="onRemoveClickTeamParts(tp)">
                Удалить
            </button>
        </div>
    </div>

    <div class="row m-2">
        <button class="btn btn-outline-primary" @click="onLoadCLickTeamParts">Загрузить участия команд в
            турнирах</button>
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
