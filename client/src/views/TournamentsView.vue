<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from "axios";
import { useUserStore } from '../stores/user_store';
import { storeToRefs } from 'pinia';

const userStore = useUserStore();
const {
    is_staff
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

const selectedStatus = ref("")

const tournamentTeamCount = ref(0);
const selectedTournament = ref(null);

onBeforeMount(async () => {
    await fetchTournaments();
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
    formData.set('prize_pool', tournamentToAdd.value.prize_pool)

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
    formData.set('prize_pool', tournamentToEdit.value.prize_pool)

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

function filterTournaments() {
    if (selectedStatus.value == "") {
        return tournaments.value;
    }

    return tournaments.value.filter(t => t.status == this.selectedStatus);
}

async function exportTournamentsToExcel() {
    const response = await axios.get('/api/tournaments/export-excel/', {
        responseType: 'blob'
    });

    const date = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    const filename = `tournaments_${date}.xlsx`;

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
}

async function openTournamentStatsModal(tournament) {
    selectedTournament.value = tournament;
    const response = await axios.get(`/api/tournaments/${tournament.id}/team_count_stats/`);
    tournamentTeamCount.value = response.data.count;
}
</script>

<template>
    <!-- вывод статистики -->
    <div class="modal fade" id="tournamentStatsModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Команды в турнире {{ selectedTournament?.name }}</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body text-center">
                    <div>Команд всего участвует: {{ tournamentTeamCount }} </div>
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
                        Редактирование
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="col-auto mb-2">
                        <div class="col">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="tournamentToEdit.name" required />
                                <label for="floatingInput">Название</label>
                            </div>
                        </div>
                    </div>
                    <div class="col-auto mb-2">
                        <div class="form-floating">
                            <input type="date" class="form-control" v-model="tournamentToEdit.start_date" required />
                            <label for="floatingInput">Дата начала</label>
                        </div>
                    </div>
                    <div class="col-auto mb-2">
                        <div class="form-floating">
                            <input type="date" class="form-control" v-model="tournamentToEdit.end_date" required />
                            <label for="floatingInput">Дата конца</label>
                        </div>
                    </div>
                    <div class="col-auto mb-2">
                        <div class="form-floating">
                            <select class="form-control" v-model="tournamentToEdit.status" required>
                                <option value="TBA">Неизвестно</option>
                                <option value="Coming">Скоро начнётся</option>
                                <option value="Live">Идёт</option>
                                <option value="Ended">Закончен</option>
                            </select>
                            <label>Статус</label>
                        </div>
                    </div>
                    <div class="col-auto mb-2">
                        <div class="col-12">
                            <div class="form-floating">
                                <input type="number" class="form-control" v-model="tournamentToEdit.prize_pool" />
                                <label>Призовой фонд (в рублях)</label>
                            </div>
                        </div>
                    </div>
                    <div class="col-auto mb-2">
                        <label>Логотип турнира</label>
                        <input class="form-control" type="file" ref="tournamentsEditPictureRef"
                            @change="tournamentsEditPictureChange" />
                    </div>
                    <div class="col-auto mb-2">
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
                    <div class="col-auto mb-2" v-if="tournamentToEdit.logo && !deleteLogo">
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
    <form v-if="is_staff" @submit.prevent.stop="onTournamentAdd">
        <div class="row m-2 ">
            <div class="col">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="tournamentToAdd.name" required />
                    <label for="floatingInput">Название</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <input type="date" class="form-control" v-model="tournamentToAdd.start_date" required />
                    <label for="floatingInput">Дата начала</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <input type="date" class="form-control" v-model="tournamentToAdd.end_date" required />
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
                <input class="form-control" type="file" ref="tournamentsPictureRef"
                    @change="tournamentsAddPictureChange" />
            </div>
            <div class="col-auto">
                <img :src="tournamentToAddImageUrl" style="max-height:150px; cursor: pointer;" alt=""
                    @click="openImagePreview(tournamentToAddImageUrl)" data-bs-toggle="modal"
                    data-bs-target="#imagePreviewModal">
            </div>
            <div class="col">
                <div class="form-floating">
                    <input type="number" class="form-control" v-model="tournamentToAdd.prize_pool" />
                    <label for="floatingInput">Призовой фонд (в рублях)</label>
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
        <h6>Фильтр по статусу</h6>
        <div class="row">
            <div class="col-auto">
                <div class="form-floating">
                    <select value="" class="form-select" v-model="selectedStatus">
                        <option value="">С любым статусом</option>
                        <option value="TBA">Неизвестно</option>
                        <option value="Coming">Скоро начнётся</option>
                        <option value="Live">Идёт</option>
                        <option value="Ended">Закончен</option>
                    </select>
                    <label for="floatingInput">Выберите статус</label>
                </div>
            </div>
        </div>
    </div>

    <!-- экспорт в excel -->
    <div class="row m-2" style="justify-content: end;">
        <div v-if="is_staff" class="col-auto">
            <div class="btn-group" role="group">
                <button class="btn btn-outline-success" @click="exportTournamentsToExcel">
                    Экспорт всех турниров в Excel-таблицу
                </button>
            </div>
        </div>
    </div>

    <!-- вывод и кнопки -->
    <div v-if="filterTournaments().length == 0 && !loading" style="text-align: center;">
        <h4>Турниров не найдено</h4>
    </div>
    <div v-else-if="filterTournaments.length == 0 && loading" style="text-align: center; margin: 1rem;">
        <h4>Загрузка турниров...</h4>
    </div>
    <div v-for="t in filterTournaments()" class="output-item">
        <div>
            <div>{{ t.name }}</div>
            <div>{{ t.start_date }}</div>
            <div>{{ t.end_date }}</div>
            <div>{{ t.status }}</div>
            <div><b>Призовой фонд (в рублях): </b>{{ t.prize_pool || "не определён" }}</div>
            <div v-show="t.logo">
                <img :src="t.logo" style="max-height: 150px; cursor: pointer;" :alt="`Логотип турнира ${t.name}`"
                    @click="openImagePreview(t.logo)" data-bs-toggle="modal" data-bs-target="#imagePreviewModal">
            </div>
        </div>
        <div>
            <button class="btn btn-secondary" @click="openTournamentStatsModal(t)" data-bs-toggle="modal"
                data-bs-target="#tournamentStatsModal">
                Количество команд в турнире
            </button>
        </div>
        <div>
            <button v-if="is_staff" class="btn btn-success" @click="onTournamentEditClick(t)" data-bs-toggle="modal"
                data-bs-target="#editTournamentModal">
                Редактировать
            </button>
        </div>
        <div>
            <button v-if="is_staff" class="btn btn-danger" @click="onRemoveClickTournament(t)">
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
    grid-template-columns: 1fr auto auto auto;
    gap: 8px;
    justify-content: center;
}
</style>