<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

const teams = ref([]);
const teamToAdd = ref({});
const teamToAddImageUrl = ref();
const teamToEdit = ref({});
const teamToEditImageUrl = ref();
const teamsPictureRef = ref();
const teamsEditPictureRef = ref();

const previewImageUrl = ref('');

const deleteLogo = ref(false);

const loading = ref(false);

onBeforeMount(async () => {
    await fetchTeams();
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

async function fetchTeams() {
    loading.value = true;
    const r = await axios.get("/api/teams/");
    console.log(r.data);
    teams.value = r.data;
    loading.value = false;
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

</script>

<template>
    <!-- просмотр картинок в модальном окне -->
    <div class="modal" id="imagePreviewModal" tabindex="-1">
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

    <!-- редактирование в модальном окне-->
    <div class="modal" id="editTeamModal" tabindex="-1">
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
    <form @submit.prevent.stop="onTeamAdd">
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
            </div>
            <div class="col-auto">
                <img :src="teamToAddImageUrl" style="max-height:150px; cursor: pointer;" alt=""
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
    <div v-for="t in teams" class="output-item">
        <div>
            {{ t.id }} {{ t.name }} {{ t.country }}
            <div v-show="t.logo"><img :src="t.logo" style="max-height: 150px; cursor: pointer;" alt="Логотип команды {{ t.name }}"
                    @click="openImagePreview(t.logo)" data-bs-toggle="modal" data-bs-target="#imagePreviewModal"></div>
        </div>
        <div>
            <button class=" btn btn-success" @click="onTeamEditClick(t)" data-bs-toggle="modal"
                data-bs-target="#editTeamModal">
                <i class="bi bi-pen-fill">Редактировать</i>
            </button>
        </div>
        <div>
            <button class="btn btn-danger" @click="onRemoveClickTeam(t)">
                <i class="bi bi-x">Удалить</i>
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
    grid-template-columns: 1fr auto auto;
    gap: 8px;
    justify-content: center;
}
</style>
