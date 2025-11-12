<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

const players = ref([]);
const playerToAdd = ref({});
const playerToEdit = ref({});

const teams = ref([]);
const users = ref([]);

const loading = ref(false);

onBeforeMount(async () => {
    await fetchItems();
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

async function fetchItems() {
    loading.value = true;
    const r = await axios.get("/api/players/");
    console.log(r.data);
    players.value = r.data;

    const r1 = await axios.get("/api/teams/");
    console.log(r1.data);
    teams.value = r1.data;

    const r2 = await axios.get("/api/users/");
    console.log(r2.data);
    users.value = r2.data;
    loading.value = false;
}



async function onLoadCLickPlayers() {
    await fetchItems();
}

async function onPlayerAdd() {
    await axios.post("/api/players/", {
        ...playerToAdd.value,
    });
    await fetchItems();
    playerToAdd.value = {};
}

async function onRemoveClickPlayer(player) {
    await axios.delete(`/api/players/${player.id}/`);
    await fetchItems();
}

async function onUpdatePlayer() {
    await axios.put(`/api/players/${playerToEdit.value.id}/`, {
        ...playerToEdit.value,
    });
    await fetchItems();
}

async function onPlayerEditClick(player) {
    playerToEdit.value = {
        ...player,
        user_id: player.user?.id,
        team_id: player.team?.id
    };
}
</script>

<template>
    <!-- редактирование в модальном окне-->
    <div class="modal" id="editTournamentModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">
                        Редактирование игрока
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="row mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <select class="form-select" v-model="playerToEdit.user_id" required>
                                    <option :value="u.id" v-for="u in users">{{ u.username }}</option>
                                </select>
                                <label>Привязка к пользователю</label>
                            </div>
                        </div>
                    </div>

                    <div class="row mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="playerToEdit.nickname" />
                                <label>Никнейм</label>
                            </div>
                        </div>
                    </div>

                    <div class="row mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="playerToEdit.real_name" />
                                <label>Настоящее имя</label>
                            </div>
                        </div>
                    </div>

                    <div class="row mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <select class="form-select" v-model="playerToEdit.role">
                                    <option value="CARRY">Керри</option>
                                    <option value="MIDLANER">Мидлейнер</option>
                                    <option value="HARDLINER">Тройка</option>
                                    <option value="SEMISUPPORT">Четвёрка</option>
                                    <option value="FULLSUPPORT">Пятёрка</option>
                                </select>
                                <label>Роль</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <select class="form-select" v-model="playerToEdit.team_id" required>
                                    <option :value="t.id" v-for="t in teams">{{ t.name }}</option>
                                </select>
                                <label>Команда</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Закрыть
                    </button>
                    <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdatePlayer">
                        Сохранить
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- добавление -->
    <form @submit.prevent.stop="onPlayerAdd">
        <div class="row m-2 ">
            <div class="col-3">
                <div class="form-floating">
                    <select class="form-select" v-model="playerToAdd.user_id" required>
                        <option :value="u.id" v-for="u in users">{{ u.username }}</option>
                    </select>
                    <label for="floatingInput">Привязка к пользователю</label>
                </div>
            </div>
            <div class="col">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="playerToAdd.nickname" />
                    <label for="floatingInput">Никнейм</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="playerToAdd.real_name" />
                    <label for="floatingInput">Настоящее имя</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <select class="form-control" v-model="playerToAdd.role">
                        <option value="CARRY">Керри</option>
                        <option value="MIDLANER">Мидлейнер</option>
                        <option value="HARDLINER">Тройка</option>
                        <option value="SEMISUPPORT">Четвёрка</option>
                        <option value="FULLSUPPORT">Пятёрка</option>
                    </select>
                    <label>Роль</label>
                </div>
            </div>
            <div class="col-2">
                <div class="form-floating">
                    <select class="form-select" v-model="playerToAdd.team_id" required>
                        <option :value="t.id" v-for="t in teams">{{ t.name }}</option>
                    </select>
                    <label for="floatingInput">Команда</label>
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
    <div v-for="p in players" class="output-item">
        <div>
            {{ p.user?.username }} {{ p.nickname }} {{ p.real_name }} {{ p.role }} {{ p.team?.name }}
        </div>
        <div>
            <button class="btn btn-success" @click="onPlayerEditClick(p)" data-bs-toggle="modal"
                data-bs-target="#editTournamentModal">
                <i class="bi bi-pen-fill">Редактировать</i>
            </button>
        </div>
        <div>
            <button class="btn btn-danger" @click="onRemoveClickPlayer(p)">
                <i class="bi bi-x">Удалить</i>
            </button>
        </div>
    </div>

    <div class="row m-2">
        <button class="btn btn-outline-primary" @click="onLoadCLickPlayers">Загрузить игроков</button>
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
