from django.db import models
from django.utils import timezone
import json
import requests


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

    def __init__(self, id, skip_webapi=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        self.players = []

        if not skip_webapi:
            self._populate_from_webapi()

    def _populate_from_webapi(self, match_data=None):
        url = "https://api.opendota.com/api/matches/{}".format(self.id)
        raw_json = requests.get(url)
        api_info = json.loads(raw_json.text)

        self.replay_cluster = api_info['cluster']
        self.replay_salt = api_info['replay_salt']

        self.good_guys_win = api_info['radiant_win']
        self.duration = api_info['duration']
        self.start_time = api_info['start_time']
        self.first_blood_time = api_info['first_blood_time']
        self.human_players = api_info['human_players']

        self.radiant_tower_status = api_info['tower_status_radiant']
        self.dire_tower_status = api_info['tower_status_dire']
        self.radiant_barracks_status = api_info['barracks_status_radiant']
        self.dire_barracks_status = api_info['barracks_status_dire']

        for player in api_info['players']:
            self.players.append(player)

    def save(self):
        super().save()
        for player in self.players:
            new_player = ReplayPlayer(player_info=player, replay=self)
            new_player.save()


# Specifies a single player in a match, and is associated explicitly with that match. Does not represent a player
# across matches.
class ReplayPlayer(models.Model):
    player_id = models.IntegerField(db_index=True, default=0)
    match_id = models.IntegerField()
    replay = models.ForeignKey(
        Replay,
        on_delete=models.CASCADE
    )


    # GC data
    # account_id = models.ForeignKey(
    # "users.id",
    # index=True
    # )
    player_slot = models.IntegerField()
    hero_id = models.IntegerField()
    item_0 = models.IntegerField()
    item_1 = models.IntegerField()
    item_2 = models.IntegerField()
    item_3 = models.IntegerField()
    item_4 = models.IntegerField()
    item_5 = models.IntegerField()
    backpack_0 = models.IntegerField()
    backpack_1 = models.IntegerField()
    backpack_2 = models.IntegerField()
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

    def __init__(self, player_info=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if player_info:
            self._populate_from_webapi(api_info=player_info)

    def _populate_from_webapi(self, api_info=None):

        if api_info['account_id']: #If account not private
            self.player_id = api_info['account_id']
        self.match_id = api_info['match_id']

        self.player_slot = api_info['player_slot']
        self.hero_id = api_info['hero_id']
        self.item_0 = api_info['item_0']
        self.item_1 = api_info['item_1']
        self.item_2 = api_info['item_2']
        self.item_3 = api_info['item_3']
        self.item_4 = api_info['item_4']
        self.item_5 = api_info['item_5']
        self.backpack_0 = api_info['backpack_0']
        self.backpack_1 = api_info['backpack_1']
        self.backpack_2 = api_info['backpack_2']
        self.kills = api_info['kills']
        self.deaths = api_info['deaths']
        self.assists = api_info['assists']
        self.leaver_status = api_info['leaver_status']
        self.gold = api_info['gold']
        self.last_hits = api_info['last_hits']
        self.denies = api_info['denies']
        self.gold_per_min = api_info['gold_per_min']
        self.xp_per_min = api_info['xp_per_min']
        self.gold_spent = api_info['gold_spent']
        self.hero_damage = api_info['hero_damage']
        self.tower_damage = api_info['tower_damage']
        self.hero_healing = api_info['hero_healing']
        self.level = api_info['level']
