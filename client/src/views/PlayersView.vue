<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios";
import { useUserStore } from '../stores/user_store';
import { storeToRefs } from 'pinia';

const userStore = useUserStore();
const {
    is_staff,
    username
} = storeToRefs(userStore)

const players = ref([]);
const playerToAdd = ref({});
const playerToAddImageUrl = ref();
const playerToEdit = ref({});
const playerToEditImageUrl = ref();
const playersPictureRef = ref();
const playersEditPictureRef = ref();

const previewImageUrl = ref('');

const teams = ref([]);

const deletePhoto = ref(false);
const loading = ref(false);

const selectedRole = ref("")
const selectedTeam = ref("")

const playerHistory = ref([]);
const selectedPlayer = ref(null);

onBeforeMount(async () => {
    await fetchItems();
})

async function fetchItems() {
    loading.value = true;
    const r = await axios.get("/api/players/");
    console.log(r.data);
    players.value = r.data;

    const r1 = await axios.get("/api/teams/");
    console.log(r1.data);
    teams.value = r1.data;

    loading.value = false;
}



async function onLoadCLickPlayers() {
    await fetchItems();
}

async function onPlayerAdd() {
    const formData = new FormData();

    if (playersPictureRef.value.files[0]) {
        formData.append('photo', playersPictureRef.value.files[0]);
    }

    formData.set('nickname', playerToAdd.value.nickname)
    formData.set('real_name', playerToAdd.value.real_name)
    formData.set('role', playerToAdd.value.role)
    formData.set('team_id', playerToAdd.value.team_id)

    await axios.post("/api/players/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchItems();
    playerToAdd.value = {};
    playerToAddImageUrl.value = null;
    playersPictureRef.value.value = '';
}

async function onRemoveClickPlayer(player) {
    await axios.delete(`/api/players/${player.id}/`);
    await fetchItems();
}

async function onUpdatePlayer() {
    const haveToUpdate = ref(false)

    if (username.value == playerToEdit.value.original_nickname) {
        haveToUpdate.value = true
    }

    const formData = new FormData();

    formData.set('nickname', playerToEdit.value.nickname)
    formData.set('real_name', playerToEdit.value.real_name)
    formData.set('role', playerToEdit.value.role)
    formData.set('team_id', playerToEdit.value.team_id)

    if (deletePhoto.value) {
        formData.set('photo', '');
    }
    else if (playersEditPictureRef.value.files[0]) {
        formData.append('photo', playersEditPictureRef.value.files[0]);
    }

    await axios.put(`/api/players/${playerToEdit.value.id}/`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchItems();
    playerToEditImageUrl.value = null;
    playersEditPictureRef.value.value = '';
    deletePhoto.value = false;

    if (haveToUpdate.value) {
        window.location.reload();
    }
}

async function playersAddPictureChange() {
    if (playersPictureRef.value.files[0]) {
        playerToAddImageUrl.value = URL.createObjectURL(playersPictureRef.value.files[0])
    } else {
        playerToAddImageUrl.value = null;
    }
}

async function playersEditPictureChange() {
    if (playersEditPictureRef.value.files[0]) {
        playerToEditImageUrl.value = URL.createObjectURL(playersEditPictureRef.value.files[0])
        deletePhoto.value = false;
    } else {
        playerToEditImageUrl.value = null;
    }
}

async function onPlayerEditClick(player) {
    playerToEdit.value = {
        ...player,
        original_nickname: player.nickname,
        team_id: player.team?.id
    };

    playerToEditImageUrl.value = null;
    deletePhoto.value = false;
    if (playersEditPictureRef.value) {
        playersEditPictureRef.value.value = '';
    }
}

function onDeletePhotoClick() {
    deletePhoto.value = true;
    playerToEditImageUrl.value = null;
    if (playersEditPictureRef.value) {
        playersEditPictureRef.value.value = '';
    }
}

function openImagePreview(imageUrl) {
    previewImageUrl.value = imageUrl;
}

function filterPlayers() {
    let filtered = players.value;

    if (selectedRole.value) {
        filtered = filtered.filter(p => p.role === selectedRole.value);
    }

    if (selectedTeam.value) {
        filtered = filtered.filter(p => p.team?.id == selectedTeam.value);
    }

    return filtered;
}

async function exportPlayersToExcel() {
    const response = await axios.get('/api/players/export-excel/', {
        responseType: 'blob'
    });

    const date = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    const filename = `players_${date}.xlsx`;

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
}

async function openPlayerHistory(player) {
    selectedPlayer.value = player;
    const response = await axios.get(`/api/players/${player.id}/team_history/`);
    playerHistory.value = response.data;
}
</script>

<template>
    <!-- статистика -->
    <div class="modal fade" id="playerHistoryModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">История переходов игрока {{ selectedPlayer?.nickname }}</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div v-if="playerHistory.length == 0">
                        Нет истории переходов
                    </div>
                    <div v-else>
                        <div v-for="(record, index) in playerHistory" :key="index">
                            <div>{{ index + 1 }}:</div>
                            <div>Команда: {{ record.team }}</div>
                            <div>Дата: {{ record.date }}</div>
                            <div>Менеджер: {{ record.manager }}</div>
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
                    <img :src="previewImageUrl" style="max-width: 100%; max-height: 80vh;" alt="картинка">
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                </div>
            </div>
        </div>
    </div>

    <!-- редактирование в модальном окне-->
    <div class="modal fade" id="editTournamentModal" tabindex="-1">
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
                                <input type="text" class="form-control" v-model="playerToEdit.nickname" required />
                                <label>Никнейм</label>
                            </div>
                        </div>
                    </div>

                    <div class="row mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="playerToEdit.real_name" required />
                                <label>Настоящее имя</label>
                            </div>
                        </div>
                    </div>

                    <div class="row mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <select class="form-select" v-model="playerToEdit.role" required>
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
                    <div v-if="is_staff" class="row mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <select class="form-select" v-model="playerToEdit.team_id" required>
                                    <option :value="t.id" v-for="t in teams">{{ t.name }}</option>
                                </select>
                                <label>Команда</label>
                            </div>
                        </div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-12">
                            <label>Фото игрока</label>
                            <input class="form-control" type="file" ref="playersEditPictureRef"
                                @change="playersEditPictureChange" />
                        </div>
                    </div>
                    <div class="row mb-2">
                        <div class="col-12">
                            <div v-if="playerToEditImageUrl">
                                <div class="text-muted small">Новое фото</div>
                                <img :src="playerToEditImageUrl" style="max-height:150px;" alt="" class="mt-2">
                            </div>
                            <div v-else-if="playerToEdit.photo && !deletePhoto">
                                <div class="text-muted small">Текущее фото</div>
                                <img :src="playerToEdit.photo" style="max-height:150px;" alt="" class="mt-2">
                            </div>
                            <div v-else class="text-muted mt-2">Нет фото</div>
                        </div>
                    </div>
                    <div class="row mb-2" v-if="playerToEdit.photo && !deletePhoto">
                        <div class="col-12">
                            <button type="button" class="btn btn-danger" @click="onDeletePhotoClick">
                                Удалить фото
                            </button>
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
    <form v-if="is_staff" @submit.prevent.stop="onPlayerAdd">
        <div class="row m-2">
            <div class="col-auto">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="playerToAdd.nickname" required />
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
                    <select class="form-control" v-model="playerToAdd.role" required>
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
                <input class="form-control" type="file" ref="playersPictureRef" @change="playersAddPictureChange" />
                <img :src="playerToAddImageUrl" style="max-height:150px; margin-top: 1rem; cursor: pointer;" alt=""
                    @click="openImagePreview(playerToAddImageUrl)" data-bs-toggle="modal"
                    data-bs-target="#imagePreviewModal">
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
                    <select class="form-select" v-model="selectedRole">
                        <option value="">Любая роль</option>
                        <option value="CARRY">Керри</option>
                        <option value="MIDLANER">Мидлейнер</option>
                        <option value="HARDLINER">Тройка</option>
                        <option value="SEMISUPPORT">Четвёрка</option>
                        <option value="FULLSUPPORT">Пятёрка</option>
                    </select>
                    <label>Роль</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <select class="form-select" v-model="selectedTeam">
                        <option value="">Любая команда</option>
                        <option :value="t.id" v-for="t in teams">{{ t.name }}</option>
                    </select>
                    <label>Команда</label>
                </div>
            </div>
        </div>
    </div>

    <!-- экспорт в excel -->
    <div class="row m-2" style="justify-content: end;">
        <div v-if="is_staff" class="col-auto">
            <div class="btn-group" role="group">
                <button class="btn btn-outline-success" @click="exportPlayersToExcel">
                    Экспорт всех игроков в Excel-таблицу
                </button>
            </div>
        </div>
    </div>

    <!-- вывод и кнопки -->
    <div v-if="filterPlayers().length == 0 && !loading" style="text-align: center;">
        <h4>Игроков не найдено</h4>
    </div>
    <div v-else-if="filterPlayers().length == 0 && loading" style="text-align: center; margin: 1rem;">
        <h4>Загрузка игроков...</h4>
    </div>
    <div v-for="p in filterPlayers()" class="output-item">
        <div>
            <b v-if="p.nickname == username">Это вы!</b>
            <div>{{ p.nickname }}</div>
            <div>{{ p.real_name }}</div>
            <div>{{ p.role }}</div>
            <div v-if="is_staff">{{ p.team?.name }}</div>
            <div v-show="p.photo">
                <img :src="p.photo" style="max-height: 150px; cursor: pointer;" :alt="`Фото игрока ${p.nickname}`"
                    @click="openImagePreview(p.photo)" data-bs-toggle="modal" data-bs-target="#imagePreviewModal">
            </div>
        </div>
        <div>
            <button class="btn btn-secondary" @click="openPlayerHistory(p)" data-bs-toggle="modal"
                data-bs-target="#playerHistoryModal">
                История переходов
            </button>
        </div>
        <div>
            <button class="btn btn-success" @click="onPlayerEditClick(p)" data-bs-toggle="modal"
                data-bs-target="#editTournamentModal">
                Редактировать
            </button>
        </div>
        <div>
            <button v-if="p.nickname != username" class="btn btn-danger" @click="onRemoveClickPlayer(p)">
                Удалить
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
    grid-template-columns: 1fr auto auto auto;
    gap: 8px;
    justify-content: center;
}
</style>
