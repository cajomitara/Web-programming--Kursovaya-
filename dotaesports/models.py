from django.db import models

# Create your models here.
class Tournament(models.Model):
    name = models.TextField('Название турнира', null=True)

    start_date = models.DateField('Дата начала', null=True)
    end_date = models.DateField('Дата окончания', null=True)

    logo = models.ImageField("Изображение", null=True, upload_to="tournaments")

    class Status(models.TextChoices):
        TBA = "TBA", ("Неизвестно")
        COMING = "Coming", ("Скоро начнётся")
        LIVE = "Live", ("Идёт")
        ENDED = "Ended", ("Закончен")
    status = models.CharField(
        max_length = 6,
        choices = Status,
        default = Status.TBA,
        null=True
    )

    prize_pool = models.IntegerField("Призовой фонд (в рублях)", null=True)

    class Meta:
        verbose_name = "Турнир"
        verbose_name_plural = "Турниры"

    def __str__(self) -> str:
        return self.name

class Team(models.Model):
    name = models.TextField('Название', null=True)
    country = models.TextField('Страна происхождения', null=True)

    logo = models.ImageField("Изображение", null=True, upload_to="teams")

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    def __str__(self) -> str:
        return self.name

class Player(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, verbose_name="Пользователь")

    nickname = models.TextField('Псевдоним', null=True)
    real_name = models.TextField('Настоящее имя', null=True)

    photo = models.ImageField("Изображение", null=True, upload_to="players")

    class Role(models.TextChoices):
        CARRY = "CARRY", ("Керри")
        MIDLANER = "MIDLANER", ("Мидлейнер")
        HARDLINER = "HARDLINER", ("Тройка")
        SEMISUPPORT = "SEMISUPPORT", ("Четвёрка")
        FULLSUPPORT = "FULLSUPPORT", ("Пятёрка")
    role = models.CharField(
        max_length = 11,
        choices = Role,
        verbose_name = "Роль",
        null=True
    )

    team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True, verbose_name="Команда")

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"

    def __str__(self) -> str:
        return self.nickname

class TournamentTeamParticipation(models.Model):
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, null=True, verbose_name="Турнир")
    team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True, verbose_name="Команда")

    place = models.IntegerField("Место", default=0, null=True)
    
    class Meta:
        verbose_name = "Участие команды"
        verbose_name_plural = "Участия команды"

class Match(models.Model):
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, null=True, verbose_name="Турнир")
    
    radiant = models.ForeignKey('Team', on_delete=models.CASCADE, null=True, related_name='radiant_matches', verbose_name="Силы Света")
    dire = models.ForeignKey('Team', on_delete=models.CASCADE, null=True, related_name='dire_matches', verbose_name="Силы Тьмы")

    start_date = models.DateTimeField('Дата начала', null=True)

    winner = models.ForeignKey('Team', on_delete=models.CASCADE, null=True, related_name='winner', verbose_name="Победитель")

    class Meta:
        verbose_name = "Матч"
        verbose_name_plural = "Матчи"