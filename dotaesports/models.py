from django.db import models

# Create your models here.
class Tournament(models.Model):
    name = models.TextField('Название турнира')

    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания')

    class Status(models.TextChoices):
        TBA = "TBA", ("Неизвестно")
        COMING = "Coming", ("Скоро начнётся")
        LIVE = "Live", ("Идёт")
        ENDED = "Ended", ("Закончен")
    status = models.CharField(
        max_length = 6,
        choices = Status,
        default = Status.TBA,
    )

    prize_pool = models.IntegerField("Призовой фонд (в рублях)")

    class Meta:
        verbose_name = "Турнир"
        verbose_name_plural = "Турниры"

    def __str__(self) -> str:
        return self.name

class Team(models.Model):
    name = models.TextField('Название')
    country = models.TextField('Страна происхождения')

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    def __str__(self) -> str:
        return self.name

class Player(models.Model):
    nickname = models.TextField('Псевдоним')
    real_name = models.TextField('Настоящее имя')

    class Role(models.TextChoices):
        CARRY = "CARRY", ("Керри")
        MIDLANER = "MIDLANER", ("Мидлейнер")
        HARDLINER = "HARDLINER", ("Тройка")
        SEMISUPPORT = "SEMISUPPORT", ("Четвёрка")
        FULLSUPPORT = "FULLSUPPORT", ("Пятёрка")
    role = models.CharField(
        max_length = 11,
        choices = Role,
        verbose_name = "Роль"
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

    place = models.IntegerField("Место", default=0)
    
    class Meta:
        verbose_name = "Участие команды"
        verbose_name_plural = "Участия команды"

class Match(models.Model):
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, null=True, verbose_name="Турнир")
    
    radiant = models.ForeignKey('Team', on_delete=models.CASCADE, null=True, related_name='radiant_matches', verbose_name="Силы Света")
    dire = models.ForeignKey('Team', on_delete=models.CASCADE, null=True, related_name='dire_matches', verbose_name="Силы Тьмы")

    start_date = models.DateTimeField('Дата начала')

    class Winner(models.TextChoices):
        TBA = "TBA", ("Неизвестно")
        RADIANT = "RADIANT", ("Силы Света")
        DIRE = "DIRE", ("Силы Тьмы")
    winner = models.CharField(
        max_length = 7,
        choices = Winner,
        default = Winner.TBA,
        verbose_name = "Победитель"
    )

    class Meta:
        verbose_name = "Матч"
        verbose_name_plural = "Матчи"