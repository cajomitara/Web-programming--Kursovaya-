<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

const players = ref([]);
const playerToAdd = ref({});
const playerToAddImageUrl = ref();
const playerToEdit = ref({});
const playerToEditImageUrl = ref();
const playersPictureRef = ref();
const playersEditPictureRef = ref();

const previewImageUrl = ref('');

const teams = ref([]);
const users = ref([]);

const deletePhoto = ref(false);
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
    const formData = new FormData();

    if (playersPictureRef.value.files[0]) {
        formData.append('photo', playersPictureRef.value.files[0]);
    }

    formData.set('user_id', playerToAdd.value.user_id)
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
    const formData = new FormData();

    formData.set('user_id', playerToEdit.value.user_id)
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
        user_id: player.user?.id,
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
</script>

<template>
    <!-- просмотр картинок в модальном окне -->
    <div class="modal" id="imagePreviewModal" tabindex="-1">
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
    <form @submit.prevent.stop="onPlayerAdd">
        <div class="row m-2">
            <div class="col-auto">
                <div class="form-floating">
                    <select class="form-select" v-model="playerToAdd.user_id" required>
                        <option :value="u.id" v-for="u in users">{{ u.username }}</option>
                    </select>
                    <label for="floatingInput">Привязка к пользователю</label>
                </div>
            </div>
            <div class="col-2">
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
            <div class="col-1">
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
            <div class="col-auto">
                <div class="form-floating">
                    <select class="form-select" v-model="playerToAdd.team_id" required>
                        <option :value="t.id" v-for="t in teams">{{ t.name }}</option>
                    </select>
                    <label for="floatingInput">Команда</label>
                </div>
            </div>
            <div class="col-3">
                <input class="form-control" type="file" ref="playersPictureRef" @change="playersAddPictureChange" />
            </div>
            <div class="col-auto">
                <img :src="playerToAddImageUrl" style="max-height:150px; cursor: pointer;" alt=""
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


    <!-- вывод и кнопки -->
    <div v-for="p in players" class="output-item">
        <div>
            {{ p.user?.username }} {{ p.nickname }} {{ p.real_name }} {{ p.role }} {{ p.team?.name }}
            <div v-show="p.photo">
                <img :src="p.photo" style="max-height: 150px; cursor: pointer;" :alt="`Фото игрока ${p.nickname}`"
                    @click="openImagePreview(p.photo)" data-bs-toggle="modal" data-bs-target="#imagePreviewModal">
            </div>
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
