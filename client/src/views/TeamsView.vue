<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';
import { useUserStore } from '../stores/user_store';
import { storeToRefs } from 'pinia';

const userStore = useUserStore();
const {
    is_staff
} = storeToRefs(userStore)

const teams = ref([]);
const players = ref([]);
const teamToAdd = ref({});
const teamToAddImageUrl = ref();
const teamToEdit = ref({});
const teamToEditImageUrl = ref();
const teamsPictureRef = ref();
const teamsEditPictureRef = ref();

const previewImageUrl = ref();
const deleteLogo = ref(false);
const loading = ref(false);

const currentTeamForModal = ref(null);
const newPlayer = ref({});
const transferPlayerData = ref({
    player_id: null,
    team_id: null
});

const teamStats = ref({});
const selectedTeam = ref(null);

onBeforeMount(async () => {
    await fetchTeams();
    await fetchPlayers();
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

async function fetchTeams() {
    loading.value = true;
    const r = await axios.get("/api/teams/");
    console.log(r.data);
    teams.value = r.data;
    loading.value = false;
}

async function fetchPlayers() {
    const r = await axios.get("/api/players/");
    players.value = r.data;
}

async function onLoadCLickTeams() {
    await fetchTeams();
}

async function onTeamAdd() {
    const formData = new FormData();

    if (teamsPictureRef.value.files[0]) {
        formData.append('logo', teamsPictureRef.value.files[0]);
    }

    formData.set('name', teamToAdd.value.name)
    formData.set('country', teamToAdd.value.country)

    await axios.post("/api/teams/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchTeams();
    teamToAdd.value = {};
    teamToAddImageUrl.value = null;
    teamsPictureRef.value.value = '';
}

async function teamsAddPictureChange(params) {
    if (teamsPictureRef.value.files[0]) {
        teamToAddImageUrl.value = URL.createObjectURL(teamsPictureRef.value.files[0])
    } else {
        teamToAddImageUrl.value = null;
    }
}

async function teamsEditPictureChange() {
    if (teamsEditPictureRef.value.files[0]) {
        teamToEditImageUrl.value = URL.createObjectURL(teamsEditPictureRef.value.files[0])
        deleteLogo.value = false;
    } else {
        teamToEditImageUrl.value = null;
    }
}

async function onRemoveClickTeam(team) {
    await axios.delete(`/api/teams/${team.id}/`);
    await fetchTeams();
}

async function onUpdateTeam() {
    const formData = new FormData();

    formData.set('name', teamToEdit.value.name)
    formData.set('country', teamToEdit.value.country)

    if (deleteLogo.value) {
        formData.set('logo', '');
    }
    else if (teamsEditPictureRef.value.files[0]) {
        formData.append('logo', teamsEditPictureRef.value.files[0]);
    }

    await axios.put(`/api/teams/${teamToEdit.value.id}/`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchTeams();
    teamToEditImageUrl.value = null;
    teamsEditPictureRef.value.value = '';
    deleteLogo.value = false;
}

async function onTeamEditClick(team) {
    teamToEdit.value = { ...team };
    teamToEditImageUrl.value = null;
    deleteLogo.value = false;
    if (teamsEditPictureRef.value) {
        teamsEditPictureRef.value.value = '';
    }
}

function onDeleteLogoClick() {
    deleteLogo.value = true;
    teamToEditImageUrl.value = null;
    if (teamsEditPictureRef.value) {
        teamsEditPictureRef.value.value = '';
    }
}

function openImagePreview(imageUrl) {
    previewImageUrl.value = imageUrl;
}

function prepareAddPlayerModal(team) {
    currentTeamForModal.value = team;
    newPlayer.value = {
        nickname: '',
        real_name: '',
        role: 'CARRY',
        team_id: team.id
    };
}

function prepareTransferPlayerModal(team) {
    currentTeamForModal.value = team;
    transferPlayerData.value = {
        player_id: null,
        team_id: team.id
    };
}

async function onCreatePlayer() {
    await axios.post("/api/players/", newPlayer.value);
    await fetchPlayers();

    newPlayer.value = {
        nickname: '',
        real_name: '',
        role: 'CARRY',
        team_id: currentTeamForModal.value.id
    };
}

async function onTransferPlayer() {
    if (!transferPlayerData.value.player_id) {
        return;
    }


    await axios.patch(`/api/players/${transferPlayerData.value.player_id}/`, {
        team_id: transferPlayerData.value.team_id
    });

    await fetchPlayers();

    transferPlayerData.value.player_id = null;
}

function getPlayersNotInTeam() {
    if (!currentTeamForModal.value) return [];

    return players.value.filter(player => {
        return !player.team || player.team.id != currentTeamForModal.value.id;
    });
}

function getPlayersInTeam() {
    if (!currentTeamForModal.value) return [];

    return players.value.filter(player => {
        return player.team && player.team.id == currentTeamForModal.value.id;
    });
}

async function openTeamStats(team) {
    selectedTeam.value = team;
    const response = await axios.get(`/api/teams/${team.id}/prize_stats/`);
    teamStats.value = response.data;
}
</script>

<template>
    <!-- статистика -->
    <div class="modal fade" id="teamStatsModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Призовые места команды {{ selectedTeam?.name }}</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body text-center">
                    <div class="row">
                        <div class="col-4">
                            1-е места: {{ teamStats.first || 0 }}
                        </div>
                        <div class="col-4">
                            2-е места: {{ teamStats.second || 0 }}
                        </div>
                        <div class="col-4">
                            3-и места: {{ teamStats.third || 0 }}
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                </div>
            </div>
        </div>
    </div>

    <!-- просмотр картинок в модальном окне -->
    <div class="modal fade" id="imagePreviewModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-body text-center">
                    <img :src="previewImageUrl" style="max-width: 100%; max-height: 80vh;" alt="картинка kekw">
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                </div>
            </div>
        </div>
    </div>

    <!-- модальное окно добавления игрока в команду -->
    <div class="modal fade" id="addPlayerModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">
                        Добавить игрока в {{ currentTeamForModal?.name }}
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="row mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="newPlayer.nickname" required>
                                <label>Никнейм</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="newPlayer.real_name">
                                <label>Настоящее имя</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <select class="form-select" v-model="newPlayer.role">
                                    <option value="CARRY">Керри</option>
                                    <option value="MIDLANER">Мидлейнер</option>
                                    <option value="OFFLANER">Оффлейнер</option>
                                    <option value="SEMISUPPORT">Четвёрка</option>
                                    <option value="FULLSUPPORT">Пятёрка</option>
                                </select>
                                <label>Роль</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Закрыть
                    </button>
                    <button type="button" class="btn btn-primary" @click="onCreatePlayer"
                        :disabled="!newPlayer.nickname" data-bs-dismiss="modal">
                        Добавить игрока
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- модальное окно перевода игрока -->
    <div class="modal fade" id="transferPlayerModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">
                        Перевести игрока в {{ currentTeamForModal?.name }}
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="row mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <select class="form-select" v-model="transferPlayerData.player_id">
                                    <option v-for="player in getPlayersNotInTeam()" :value="player.id">
                                        {{ player.nickname }}
                                        <template v-if="player.team"> - {{ player.team.name }}</template>
                                        <template v-else> - Без команды</template>
                                    </option>
                                </select>
                                <label>Выберите игрока для перевода</label>
                            </div>
                        </div>
                    </div>

                    <div v-if="getPlayersInTeam().length > 0" class="col-auto m-1">
                        <label>Текущие игроки в команде:</label>
                        <ul class="list-group">
                            <li v-for="player in getPlayersInTeam()" class="list-group-item">
                                {{ player.nickname }} ({{ player.role }})
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Закрыть
                    </button>
                    <button type="button" class="btn btn-primary" @click="onTransferPlayer"
                        :disabled="!transferPlayerData.player_id" data-bs-dismiss="modal">
                        Перевести игрока
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- редактирование в модальном окне-->
    <div class="modal fade" id="editTeamModal" tabindex="-1">
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
                    <div class="row mb-2">
                        <div class="col-12">
                            <label>Изображение команды</label>
                            <input class="form-control" type="file" ref="teamsEditPictureRef"
                                @change="teamsEditPictureChange" />
                        </div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-12">
                            <div v-if="teamToEditImageUrl">
                                <div class="text-muted small">Новое изображение</div>
                                <img :src="teamToEditImageUrl" style="max-height:150px;" alt="" class="mt-2">
                            </div>
                            <div v-else-if="teamToEdit.logo && !deleteLogo">
                                <div class="text-muted small">Текущее изображение</div>
                                <img :src="teamToEdit.logo" style="max-height:150px;" alt="" class="mt-2">

                            </div>
                            <div v-else class="text-muted mt-2">Нет изображения</div>
                        </div>
                    </div>
                    <div class="row mb-2" v-if="teamToEdit.logo && !deleteLogo">
                        <div class="col-12">
                            <button type="button" class="btn btn-danger" @click="onDeleteLogoClick">
                                Удалить изображение
                            </button>
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
    <form v-if="is_staff" @submit.prevent.stop="onTeamAdd">
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
                <input class="form-control" type="file" ref="teamsPictureRef" @change="teamsAddPictureChange" />
                <img :src="teamToAddImageUrl" style="max-height:150px; margin-top: 1rem; cursor: pointer;" alt=""
                    @click="openImagePreview(teamToAddImageUrl)" data-bs-toggle="modal"
                    data-bs-target="#imagePreviewModal">
            </div>
            <div class="col-auto">
                <button class="btn btn-primary">
                    Добавить
                </button>
            </div>
        </div>
    </form>

    <!-- вывод и кнопки -->
    <div v-if="teams.length == 0 && !loading" style="text-align: center;">
        <h4>Команд не найдено</h4>
    </div>
    <div v-else-if="teams.length == 0 && loading" style="text-align: center; margin: 1rem;">
        <h4>Загрузка команд...</h4>
    </div>
    <div v-for="t in teams" class="output-item">
        <div>
            <div>{{ t.name }}</div>
            <div>{{ t.country }}</div>
            <div v-show="t.logo"><img :src="t.logo" style="max-height: 150px; cursor: pointer;"
                    :alt="'Логотип команды ' + t.name" @click="openImagePreview(t.logo)" data-bs-toggle="modal"
                    data-bs-target="#imagePreviewModal"></div>
        </div>
        <div>
            <button class="btn btn-warning m-1" @click="openTeamStats(t)" data-bs-toggle="modal"
                data-bs-target="#teamStatsModal">
                Призовые места
            </button>
            <button class="btn btn-primary m-1" @click="prepareAddPlayerModal(t)" data-bs-toggle="modal"
                data-bs-target="#addPlayerModal">
                Добавить игрока
            </button>
            <button v-if="is_staff" class="btn btn-secondary m-1" @click="prepareTransferPlayerModal(t)"
                data-bs-toggle="modal" data-bs-target="#transferPlayerModal">
                Перевести игрока
            </button>
            <button class="btn btn-success m-1" @click="onTeamEditClick(t)" data-bs-toggle="modal"
                data-bs-target="#editTeamModal">
                Редактировать
            </button>
            <button v-if="is_staff" class="btn btn-danger m-1" @click="onRemoveClickTeam(t)">
                Удалить
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
    grid-template-columns: 1fr auto;
    gap: 8px;
    justify-content: center;
}
</style>