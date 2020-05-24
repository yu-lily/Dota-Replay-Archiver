from django.db import models
from django.utils import timezone


class Replay(models.Model):
    id = models.IntegerField(primary_key=True)
    added_to_site_time = models.DateTimeField(default=timezone.now, db_index=True)

    replay_cluster = models.IntegerField()  # Initial location on Valve's CDN
    replay_salt = models.IntegerField()

    good_guys_win = models.BooleanField()
    duration = models.IntegerField()
    start_time = models.IntegerField()
    first_blood_time = models.IntegerField()
    human_players = models.IntegerField()

    radiant_tower_status = models.IntegerField()
    dire_tower_status = models.IntegerField()
    radiant_barracks_status = models.IntegerField()
    dire_barracks_status = models.IntegerField()

    players = models.ForeignKey(
        'ReplayPlayer',
        on_delete=models.CASCADE
    )


class ReplayPlayer(models.Model):
    id = models.IntegerField(primary_key=True)
    replay_id = models.ForeignKey(
        "Replay",
        on_delete=models.CASCADE
    )

    # GC data
    #account_id = models.ForeignKey(
    #"users.id",
    #index=True
    #)
    player_slot = models.IntegerField()
    #hero_id =
    item_0 = models.IntegerField()
    item_1 = models.IntegerField()
    item_2 = models.IntegerField()
    item_3 = models.IntegerField()
    item_4 = models.IntegerField()
    item_5 = models.IntegerField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()
    leaver_status = models.SmallIntegerField()
    gold = models.IntegerField()
    last_hits = models.IntegerField()
    denies = models.IntegerField()
    gold_per_min = models.IntegerField()
    xp_per_min = models.IntegerField()
    gold_spent = models.IntegerField()
    hero_damage = models.IntegerField()
    tower_damage = models.IntegerField()
    hero_healing = models.IntegerField()
    level = models.SmallIntegerField()
