<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

const team_parts = ref([]);
const team_partToAdd = ref({});
const team_partToEdit = ref({});

const tournaments = ref([]);
const teams = ref([]);

const loading = ref(false);

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

</script>

<template>
    <!-- редактирование в модальном окне-->
    <div class="modal" id="editTeamPartModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">
                        Редактирование
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="modal-body">
                        <div class="row mb-3">
                            <div class="col-12">
                                <div class="form-floating">
                                    <select class="form-select" v-model="team_partToEdit.tournament_id" required>
                                        <option :value="to.id" v-for="to in tournaments">{{ to.name }}</option>
                                    </select>
                                    <label>Турнир</label>
                                </div>
                            </div>
                        </div>
                        <div class="row mb-3">
                            <div class="col-12">
                                <div class="form-floating">
                                    <select class="form-select" v-model="team_partToEdit.team_id" required>
                                        <option :value="te.id" v-for="te in teams">{{ te.name }}</option>
                                    </select>
                                    <label>Команда</label>
                                </div>
                            </div>
                        </div>
                        <div class="row mb-3">
                            <div class="col-12">
                                <div class="form-floating">
                                    <input type="number" class="form-control" v-model="team_partToEdit.place" />
                                    <label>Занятое место</label>
                                </div>
                            </div>
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
    <form @submit.prevent.stop="onTeamPartsAdd">
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


    <!-- вывод и кнопки -->
    <div v-for="tp in team_parts" class="output-item">
        <div>
            {{ tp.tournament?.name }} {{ tp.team?.name }} {{ tp.place }}
        </div>
        <div>
            <button class="btn btn-success" @click="onTeamPartEditClick(tp)" data-bs-toggle="modal"
                data-bs-target="#editTeamPartModal">
                <i class="bi bi-pen-fill">Редактировать</i>
            </button>
        </div>
        <div>
            <button class="btn btn-danger" @click="onRemoveClickTeamParts(tp)">
                <i class="bi bi-x">Удалить</i>
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
