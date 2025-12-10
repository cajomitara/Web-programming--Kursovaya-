<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';
import { useUserStore } from '../stores/user_store';
import { storeToRefs } from 'pinia';

const userStore = useUserStore();
const {
    userInfo
} = storeToRefs(userStore)

const tournaments = ref([]);
const tournamentToAdd = ref({});
const tournamentToAddImageUrl = ref();
const tournamentToEdit = ref({});
const tournamentToEditImageUrl = ref();
const tournamentsPictureRef = ref();
const tournamentsEditPictureRef = ref();

const previewImageUrl = ref('');
const deleteLogo = ref(false);
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
    const formData = new FormData();

    if (tournamentsPictureRef.value.files[0]) {
        formData.append('logo', tournamentsPictureRef.value.files[0]);
    }

    formData.set('name', tournamentToAdd.value.name)
    formData.set('start_date', tournamentToAdd.value.start_date)
    formData.set('end_date', tournamentToAdd.value.end_date)
    formData.set('status', tournamentToAdd.value.status)

    await axios.post("/api/tournaments/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchTournaments();
    tournamentToAdd.value = {};
    tournamentToAddImageUrl.value = null;
    tournamentsPictureRef.value.value = '';
}

async function onRemoveClickTournament(tournament) {
    await axios.delete(`/api/tournaments/${tournament.id}/`);
    await fetchTournaments();
}

async function onUpdateTournament() {
    const formData = new FormData();

    formData.set('name', tournamentToEdit.value.name)
    formData.set('start_date', tournamentToEdit.value.start_date)
    formData.set('end_date', tournamentToEdit.value.end_date)
    formData.set('status', tournamentToEdit.value.status)

    if (deleteLogo.value) {
        formData.set('logo', '');
    }
    else if (tournamentsEditPictureRef.value.files[0]) {
        formData.append('logo', tournamentsEditPictureRef.value.files[0]);
    }

    await axios.put(`/api/tournaments/${tournamentToEdit.value.id}/`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchTournaments();
    tournamentToEditImageUrl.value = null;
    tournamentsEditPictureRef.value.value = '';
    deleteLogo.value = false;
}

async function tournamentsAddPictureChange() {
    if (tournamentsPictureRef.value.files[0]) {
        tournamentToAddImageUrl.value = URL.createObjectURL(tournamentsPictureRef.value.files[0])
    } else {
        tournamentToAddImageUrl.value = null;
    }
}

async function tournamentsEditPictureChange() {
    if (tournamentsEditPictureRef.value.files[0]) {
        tournamentToEditImageUrl.value = URL.createObjectURL(tournamentsEditPictureRef.value.files[0])
        deleteLogo.value = false;
    } else {
        tournamentToEditImageUrl.value = null;
    }
}

async function onTournamentEditClick(tournament) {
    tournamentToEdit.value = { ...tournament };
    tournamentToEditImageUrl.value = null;
    deleteLogo.value = false;
    if (tournamentsEditPictureRef.value) {
        tournamentsEditPictureRef.value.value = '';
    }
}

function onDeleteLogoClick() {
    deleteLogo.value = true;
    tournamentToEditImageUrl.value = null;
    if (tournamentsEditPictureRef.value) {
        tournamentsEditPictureRef.value.value = '';
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
                            <input type="date" class="form-control" v-model="tournamentToEdit.start_date" required />
                            <label for="floatingInput">Дата начала</label>
                        </div>
                    </div>
                    <div class="col-auto m-1">
                        <div class="form-floating">
                            <input type="date" class="form-control" v-model="tournamentToEdit.end_date" required/>
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
                    <div class="col-auto m-1">
                        <label>Логотип турнира</label>
                        <input class="form-control" type="file" ref="tournamentsEditPictureRef"
                            @change="tournamentsEditPictureChange" />
                    </div>
                    <div class="col-auto m-1">
                        <div v-if="tournamentToEditImageUrl">
                            <div class="text-muted small">Новое лого</div>
                            <img :src="tournamentToEditImageUrl" style="max-height:150px;" alt="" class="mt-2">
                        </div>
                        <div v-else-if="tournamentToEdit.logo && !deleteLogo">
                            <div class="text-muted small">Текущее лого</div>
                            <img :src="tournamentToEdit.logo" style="max-height:150px;" alt="" class="mt-2">
                        </div>
                        <div v-else class="text-muted mt-2">Нет логотипа</div>
                    </div>
                    <div class="col-auto m-1" v-if="tournamentToEdit.logo && !deleteLogo">
                        <button type="button" class="btn btn-danger" @click="onDeleteLogoClick">
                            Удалить логотип
                        </button>
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
                    <input type="date" class="form-control" v-model="tournamentToAdd.start_date" required/>
                    <label for="floatingInput">Дата начала</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <input type="date" class="form-control" v-model="tournamentToAdd.end_date" required/>
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
                <input class="form-control" type="file" ref="tournamentsPictureRef" @change="tournamentsAddPictureChange" />
            </div>
            <div class="col-auto">
                <img :src="tournamentToAddImageUrl" style="max-height:150px; cursor: pointer;" alt=""
                    @click="openImagePreview(tournamentToAddImageUrl)" data-bs-toggle="modal"
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
    <div v-for="t in tournaments" class="output-item">
        <div>
            {{ t.id }} {{ t.name }}  {{ t.start_date }} {{ t.end_date }} {{ t.status }}
            <div v-show="t.logo">
                <img :src="t.logo" style="max-height: 150px; cursor: pointer;" :alt="`Логотип турнира ${t.name}`"
                    @click="openImagePreview(t.logo)" data-bs-toggle="modal" data-bs-target="#imagePreviewModal">
            </div>
        </div>
        <div>
            <button class="btn btn-success" @click="onTournamentEditClick(t)" data-bs-toggle="modal"
                data-bs-target="#editTournamentModal">
                Редактировать
            </button>
        </div>
        <div>
            <button class="btn btn-danger" @click="onRemoveClickTournament(t)">
                Удалить
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